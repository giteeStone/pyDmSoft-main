import json
import random
import time
import requests as rq
import asyncio,aiofiles,aiohttp
from PIL import Image   #压缩图片用 pip install Pillow
import os
from io import BytesIO  #读取图片IO

    
FW_TID = ""           #记录最近一次发送的任务流水号
FW_COUNT = 0          #记录发送次数，超过100会重置
FW_HOST = ""          #记录蜂玩上传图片的服务器地址
FW_TIMESTAMP = 0      #记录上次获取HOST的时间戳
FW_VER = "202305"     #代码版本号

def makeurl(url):
    '''
    自动处理URL，添加随机值，避免缓存
    '''
    if url[:4].upper()!="HTTP" :
        url="http://"+url
    if url.find("?")==-1:
        url+="?"+ str(random.random())
    else:
        url+="&"+ str(random.random())
    return url

async def ahttp(url,method="get",data={},header={},timeout=10,retry=3): #timeout 不可用元组
    '''
    http异步携程发包函数
    '''
    url2=makeurl(url)
    if "Connection" in header.keys()==False:header["Connection"]='close'
    if retry<1:retry=1
    while retry>=1:
        try:
            retry-=1
            if method.upper()=="GET":
                async with aiohttp.ClientSession() as session:
                    async with session.get(url2,headers=header,timeout=timeout) as resp:
                        if resp.status==200:
                            return await resp.text()
                        else:
                            return f"#{resp.status} error"
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url2, data=data, headers=header,timeout=timeout) as resp:
                        if resp.status==200:
                            return await resp.text()
                        else:
                            return f"#{resp.status} error"
        except:
            if retry<=0: return "#timeout error"

async def fwgethost():
    '''
    获取蜂玩服务器，写入全局变量FW_HOST
    '''
    global FW_HOST,FW_TIMESTAMP,FW_COUNT
    
    if FW_HOST!="" and FW_COUNT<100 and time.time()-FW_TIMESTAMP<3600*3:
        return FW_HOST

    for retry in range(100):    #如果网络有问题，最大重试100次
        ret = await ahttp("http://fapi.suanst.com:8009/gethost.html")
        if len(ret)>0 and ret[0]=="{":
            jsobj=json.loads(ret)
            FW_HOST= jsobj.get("host","")
            print("FW_HOST",FW_HOST)
            FW_COUNT=0
            FW_TIMESTAMP=time.time()
            return FW_HOST
        asyncio.sleep(1)
    return ""

async def areadbytes(path0):
    if os.path.exists(path0)==False:
        return b''
    async with aiofiles.open(path0, "rb") as f:
        btyes = await f.read()
        await f.close()
        return btyes
    
async def fwsendfile(imgfilepath,userstr,gameid,timeout,beizhu,softkey,kou=0,tojpeg=True):
    '''
    ************蜂玩发送文件************【非同步功能】
    
    imgfilepath 图片路径
    
    userstr 密码串，在用户中心获取  https://feng.suanst.com/main.sa
    
    gameid 题目类型，在官网获取 https://feng.suanst.com/gameid.htm
    
    timeout 超时时间，20~300s
    
    beizhu  图片备注，新型验证码 需要按需求 填写备注内容 才能正常使用
    
    softkey 软件KEY，需要在开发者信息中创建软件
    
    kou 自定义扣分，0~100   默认0
    
    tojpeg 利用pollow（PIL）转换为JPG格式压缩图片，默认转换
    '''
    global FW_HOST,FW_TID
    await fwgethost()     #获取HOST
        
    boundary = "fengwanfieldboundary"
    data="--"+boundary +"\r\n"
    data+=f"Content-Disposition: form-data; name=\"ver\"\r\n\r\n{FW_VER}\r\n"
    data+="--"+boundary +"\r\n"
    data+=f"Content-Disposition: form-data; name=\"userstr\"\r\n\r\n{userstr}\r\n"
    data+="--"+boundary +"\r\n"
    data+=f"Content-Disposition: form-data; name=\"gameid\"\r\n\r\n{gameid}\r\n"
    data+="--"+boundary +"\r\n"
    data+=f"Content-Disposition: form-data; name=\"timeout\"\r\n\r\n{timeout}\r\n"
    data+="--"+boundary +"\r\n"
    data+=f"Content-Disposition: form-data; name=\"beizhu\"\r\n\r\n{beizhu}\r\n"
    data+="--"+boundary +"\r\n"
    data+=f"Content-Disposition: form-data; name=\"softkey\"\r\n\r\n{softkey}\r\n"
    data+="--"+boundary +"\r\n"
    data+=f"Content-Disposition: form-data; name=\"kou\"\r\n\r\n{kou}\r\n"
    data+="--"+boundary +"\r\n"
    data+=f"Content-Disposition: form-data; name=\"img\"; filename=\"c:\\yzm.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n"
    
    byte=str.encode(data,"utf-8")
    imgbyte=await areadbytes(imgfilepath)
    img_pil=Image.open(BytesIO(imgbyte))
    if tojpeg:
        img_pil = img_pil.convert("RGB")
    with BytesIO() as output:
        if tojpeg:
            img_pil.save(output, 'jpeg')
        else:
            img_pil.save(output, img_pil.format)
        imgbyte = output.getvalue()
    byte+=imgbyte   #添加图片数据
    byte+= str.encode(f"\r\n--{boundary}--","utf-8")    #数据包结尾
    
    for retry in range(3):
        ret = await ahttp(FW_HOST + "/upload.sa","POST",byte,{"Content-Type":"multipart/form-data; boundary=fengwanfieldboundary; charset=utf-8"},30)
        print("sendfile",ret)
        if len(ret)>0 and ret[0]=="{":
            jsobj=json.loads(ret)
            FW_TID= jsobj.get("tid","")
            return ret
        else:
            FW_HOST=""
            FW_TID=""
            await fwgethost()
            asyncio.sleep(1)
    return ""
    
async def fwgetanswer(tid=""):
    '''
    ******蜂玩获取答案（不会轮询获取到有答案返回）******
    
    tid 任务流水号，留空时读取全局变量 FW_TID 的值
    '''
    
    global FW_TID
    if tid=="": tid = FW_TID
    ret = await ahttp ("http://fapi.suanst.com:8009/getanswer.sa","POST",{"tid":tid})
    
    for retry in range(20):     #重试20次
        print("getanswer",ret)
        if len(ret)>0 and ret[0]=="{":
            return ret
        else:
            asyncio.sleep(1)
    return ""

async def fwsendfileex(imgfilepath,userstr,gameid,timeout,beizhu,softkey,kou=0,tojpeg=True):
    '''
    ************蜂玩发送文件************【同步】
    
    imgfilepath 图片路径
    
    userstr 密码串，在用户中心获取  https://feng.suanst.com/main.sa
    
    gameid 题目类型，在官网获取 https://feng.suanst.com/gameid.htm
    
    timeout 超时时间，20~300s
    
    beizhu  图片备注，新型验证码 需要按需求 填写备注内容 才能正常使用
    
    softkey 软件KEY，需要在开发者信息中创建软件
    
    kou 自定义扣分，0~100   默认0
    
    tojpeg 利用pollow（PIL）转换为JPG格式压缩图片，默认转换
    '''
    
    ret1 =  await fwsendfile(imgfilepath,userstr,gameid,timeout,beizhu,softkey,kou,tojpeg)
    if len(ret1)>0 and ret1[0]=="{":
        jsobj = json.loads(ret1)
        tid = jsobj.get("tid","")
        if tid !="":
            answer=""
            while answer=="":
                asyncio.sleep(1)
                ret2 = await fwgetanswer(tid)
                if len(ret2)>0 and ret2[0]=="{":
                    jsobj = json.loads(ret2)
                    errmsg = jsobj.get('errmsg','')
                    warnmsg = jsobj.get('warnmsg','')
                    answer = jsobj.get('answer','')
                    if errmsg!="" or (warnmsg !="" and warnmsg!="回答中") or answer!="":
                        jsobj['tid']= tid   #把任务流水号添加进来
                        return json.dumps(jsobj)    #编译新的 json 字符串，并返回    
        else:
            return ret1
        
async def fwsenderror(tid=""):
    '''
    **************蜂玩申诉错题**************
    
    tid 任务流水号，默认获取 FW_TID 全局变量
    '''
    
    global FW_TID
    if tid=="": tid = FW_TID
    ret =  await ahttp("http://fapi.suanst.com:8009/senderror.sa","POST",{"tid":tid})
    
    for retry in range(20):     #重试20次
        print("senderror",ret)
        if len(ret)>0 and ret[0]=="{":
            jsobj=json.loads(ret)
            errmsg=jsobj.get('errmsg','')
            if errmsg!="":return "#"+errmsg
            warnmsg=jsobj.get('warnmsg','')
            if warnmsg!="":return "#"+warnmsg
            msg=jsobj.get('msg','')
            return msg
        else:
            asyncio.sleep(1)
    return ""

async def fwsgetpoint(userstr):
    '''
    **************蜂玩获取题分**************
    
    userstr 密码串
    '''
    
    ret =  await ahttp("http://fapi.suanst.com:8009/getpoint.sa","POST",{"userstr":userstr})
    
    for retry in range(20):     #重试20次
        print("getpoint",ret)
        if len(ret)>0 and ret[0]=="{":
            jsobj=json.loads(ret)
            errmsg=jsobj.get('errmsg','')
            if errmsg!="":return "#"+errmsg
            warnmsg=jsobj.get('warnmsg','')
            if warnmsg!="":return "#"+warnmsg
            point=jsobj.get('point',-12345)
            return point
        else:
            asyncio.sleep(1)
    return -12345


async def test():
    ret =  await fwsendfileex(r"C:\Users\Administrator\Desktop\12.png","密码串","1001",60,"你好世界","1001|9A42B0F1BD994C75")
    if len(ret)>0 and ret[0]=="{":
        jsobj=json.loads(ret)
        
        errmsg=jsobj.get('errmsg','')   # 错误返回值的示例请看 接口说明，同步函数需要同时看 “上传图片” 和 “获取答案”
        if errmsg!="":print ("#"+errmsg)    # https://www.showdoc.com.cn/fengwan/10258903646810375
        
        warnmsg=jsobj.get('warnmsg','')     # 提醒信息，也需要看 接口说明，根据不同的返回值 修改答题流程逻辑
        if warnmsg!="":print ("#"+warnmsg)  # 提醒信息在一些情况下也应该结束本次的流程
                                            # 如："答案不确定"    "图片有误"    "超时"
        
        tid=jsobj.get('tid','')         # 任务流水号
        if tid!="":print ("tid",tid)
        
        answer=jsobj.get('answer','')   #返回的答案，如果↑有异常，则答案为空字符串
        if answer!="":print ("answer",answer)
        
        # 选择题格式："1"、"2"、"3"、"4"
        # 双坐标格式："12,34|56,78"
        # 特殊题目格式看 题目类型
        
        # ~~~~~ 以下为伪代码：~~~~~~
        #   1、输入答案到应用
        #   2、sleep 5 秒
        #   3、判断是否有 回答错误的 标识，如果有-->> 需调用 fwsenderror(tid) 进行错题申诉
    else:
        print("异常返回值：",ret)
            
if __name__=="__main__":

    loop = asyncio.new_event_loop() #创建事件循环
    loop.run_until_complete(test())   #异步调用def