import json
import sys
import threading
import time
import random

from pydmsoft import DM, TimeOutException
from pydmsoft.dict_clr import *
from pydmsoft.enum_wind import get_title_winds
from qualify.fengwan import fwsendfileex


class Player(threading.Thread):
    def __init__(self,id,name="none",job="none",buffs_num=3,buff_seconds="400*400*400",*args):  # buff_seconds 列表每一项都为20秒的整数倍秒数
        # 线程初始化
        super().__init__(args=args) #target=func,
        self.args = args
        self.wait_flag = threading.Event()  # 用于暂停线程的标识
        self.wait_flag.set()  #fing.Event()  # 用于停止线程的标识
        self.__running = threading.Event()
        self.__running.set()  # 将running设置为True
        #角色信息
        self.id = id
        self.name = name
        self.job = job
        #self.level = level
        self.buffs_num = buffs_num
        self.buff_seconds = [int(i) for i in buff_seconds.split("*")]
        self.buff_funcs = [self.buff1,self.buff2,self.buff3,self.buff4,self.buff5,self.buff6]
        self.teamLeader = False
        self.map = map_lanruoDG
        self.tick_inter = 20 # tick一次10秒
        self.tick_max = 180  #最打tick到180次=3600秒=1h,最大tick次数
        self.ticks_now = 0    #当前tick值
        # 开始执行
        self.thread_run()
        # 打包进线程（耗时的操作）防止tkinter单线程阻塞

    def thread_run(self):
        title_name = self.id
        titles = get_title_winds(title_name)
        self.hWnd = titles[0]
        #self.hWnd = 1184244     #TODO
        print("self.hWnd:",self.hWnd)
        self.dm = DM(r"D:\\damo\\7.2410\\RegDll.dll",r"D:\\damo\\7.2410\\dm.dll")
        #print(m_dm,type(m_dm))
        try:
            print("注册结果",self.dm.Reg(r'jv965720b239b8396b1b7df8b768c919e86e10f',r'jn5gun14k4ep1y7'))
            m_ret = self.dm.BindWindowEx(self.hWnd, "gdi", "windows", "windows","dx.mouse.position.lock.api|dx.mouse.position.lock.message", 0) #dx.mouse.position.lock.api|dx.mouse.position.lock.message
            print("绑定结果m_ret:",m_ret)
            if (m_ret != 1 ):
                print(f"绑定失败:name:{self.name}")
            else:
                print("绑定成功")
            self.dm.SetPath(r"D:\\QnSources")
        except TimeOutException as e:
            print(e)
            sys.exit()
        self.dm.SetDict(0,"dict\yinzi.txt")
        self.dm.UseDict(0)
        self.wait_flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
        self.setDaemon(True)    # 守护--主界面关闭,孤儿线程也结束
        self.start()  # 在这里开始


    def findAndPick(self,files='hello'):
        self.dm.SetWindowState(self.hWnd,1)
        self.dm.delay(100)
        find_money = self.dm.FindStrEx(0, 0, 1400, 1000, "银票|银两", white_money,0.85)
        if find_money == "":
            print("没有发现银两银票：", find_money)
            for i in range(2):
                self.dm.KeyPressChar("tab")
                self.dm.delay(200)
                dst = self.dm.FindPicE(0,0,1500, 900,r"dst\findRoadBtn.bmp","101010",0.9,0)  #0|410|563  #dm.FindPicE(0,0,800,800,r"2.bmp","303030",0.9,0)  #qualify\login
                print("dst",dst)
                dst = dst.split("|")
                self.dm.MoveTo(int(dst[1])+self.map[0][0],int(dst[2])+self.map[0][1])     #map!
                self.dm.delay(200)
                self.dm.LeftClick()
                self.dm.delay(200)
                self.dm.KeyPressChar("tab")
                self.dm.delay(200)
                break
            self.timer1= threading.Timer(4, self.findAndPick)  # 20秒后重复此操作
            self.timer1.start()

            # self.dm.delay(10000)
            self.dm.KeyPressChar("esc")
            self.qualify()
            #self.findAndPick()
            return
        print("所有发现的银两银票：", find_money)

        ret = self.dm.FindStrEx(0, 0, 1500, 900, "红色不拾", red_notPickable, 0.85)  # "id,x0,y0|id,x1,y1|......|id,xn,yn"
        self.dm.delay(100)
        if not ret == "":
            ret = ret.split("|")
            print("发现不可拾取银两银票",ret)
            for i in range(len(ret)):
                loc = ret[i].split(",")
                loc = [int(loc[s]) for s in range(3)]
                find_money = self.dm.ExcludePos(find_money,0,loc[1],loc[2]-18,loc[1]+56,loc[2])       #  除去红色不可拾取的钱

        #print("除去不可拾取剩余的银两银票：", find_money)
        """
            string ExcludePos(all_pos,type,x1,y1,x2,y2)
            参数定义:
            all_pos 字符串: 坐标描述串。  一般是FindStrEx,FindStrFastEx,FindStrWithFontEx, FindColorEx, FindMultiColorEx,和FindPicEx的返回值.
            type 整形数:  取值为0或者1
                 如果all_pos的内容是由FindPicEx,FindPicMemEx,FindStrEx,FindStrFastEx,FindStrWithFontEx返回，那么取值为0
                 如果all_pos的内容是由FindColorEx, FindMultiColorEx,FindColorBlockEx,FindShapeEx返回，那么取值为1
                 如果all_pos的内容是由OcrEx返回，那么取值为2
                 如果all_pos的内容是由FindPicExS,FindStrExS,FindStrFastExS返回，那么取值为3
        """
        #如果all_pos的内容是由FindPicEx,FindStrEx,FindStrFastEx,FindStrWithFontEx返回，那么取值为0
        dst = self.dm.FindNearestPos(find_money,0,600,500)  #"id,x,y"

        #ret = dm.FindStrEx(0, 0, 800, 600, "任务追踪|水牢", green_shuilao,0.9)  #"id,x0,y0|id,x1,y1|......|id,xn,yn"
        print("发现最近的银两银票：", dst)
        if not dst == "":
            moneyPos = dst.split(",")       #[id,x0,y0]
            for i in range(1): #len(moneyPos)
                posix= int(moneyPos[1])
                posiy= int(moneyPos[2])
                print("所有发现的银两银票：", posix,posiy)
                print("点击前鼠标位置", self.dm.GetCursorPos())
                self.dm.MoveTo(posix+10,posiy+5)
                self.dm.delay(100)
                self.dm.LeftClick()
                self.dm.delay(1200)
                self.dm.delay(100)

        self.findAndPick()
        #print("test!!!")
        """
            string FindNearestPos(all_pos,type,x,y)
            参数定义:
            all_pos 字符串: 坐标描述串。  一般是FindStrEx,FindStrFastEx,FindStrWithFontEx, FindColorEx, FindMultiColorEx,和FindPicEx的返回值.
            type 整形数:  取值为0或者1
                 如果all_pos的内容是由FindPicEx,FindStrEx,FindStrFastEx,FindStrWithFontEx返回，那么取值为0
                 如果all_pos的内容是由FindColorEx, FindMultiColorEx,FindColorBlockEx返回，那么取值为1
            如果all_pos的内容是由OcrEx返回，那么取值为2
                 如果all_pos的内容是由FindPicExS,FindStrExS,FindStrFastExS返回，那么取值为3
            x 整形数: 横坐标
            y 整形数: 纵坐标
        """

    def buff1(self):
        self.dm.KeyPressChar("F3")
        self.dm.delay(300)
        #self.dm.KeyUpChar("alt")
        #print(f"{self.name},{self.id}::buff1-ok")
        pass

    def buff2(self):
        self.dm.KeyPressChar("F4")
        self.dm.delay(300)
        #print(f"{self.name},{self.id}:buff2-ok")
        pass

    def buff3(self):
        self.dm.KeyPressChar("F5")
        self.dm.delay(300)


        #print(f"{self.name},{self.id}:buff3-ok")
        #print("buff3")
        pass

    def buff4(self):
        print("buff4")
        pass
    def buff5(self):
        print("buff5")
        pass
    def buff6(self):
        print("buff6")
        pass

    def chgCloth(self,ctrl="alt"):
        self.dm.KeyPressChar(ctrl)
        self.dm.delay(100)
        self.dm.KeyPressChar("E")
        self.dm.KeyPressChar(ctrl)

    def func(self,str="test"):
        print("ticks_now:",self.ticks_now,str)
        if self.ticks_now>self.tick_max:
            print("over tick max")
            #self.pause()
            #self.__flag.wait()
            self.ticks_now = self.ticks_now - self.tick_max
        else:
            self.ticks_now += 1
        #坐骑
        fly = False

        for i in range(len(self.buff_seconds)):
            if self.ticks_now * self.tick_inter % self.buff_seconds[i] == 0:
                fly = True
                print(f"{self.name},{self.id}:buff[{i+1}]到时间了")
                self.buff_funcs[i]()
                self.dm.Delays(100,150)
        if fly:
            self.dm.KeyPressChar("F10")
            self.dm.Delays(3500, 3800)

        # if self.ticks_now % (100//10) == 0:
        #     print("达到buff时间ticks_now",self.ticks_now)

        self.timer = threading.Timer(self.tick_inter, self.func)  #20秒后重复此操作
        self.timer.start()

    def run(self):
        self.func("typec") #启动一次非循环
        print("runing---")
        pass

    def pause(self):
        self.wait_flag.clear()  # 设置为False，让线程阻塞
        print(f'阻塞线程ID：{self.id}:名字：{self.name}')
        self.wait_flag.wait()

    def resume(self):
        self.wait_flag.set()  # 设置为True，让线程停止阻塞
        self.wait_flag.wait()
        print('已恢复线程')

    def stop(self):
        self.wait_flag.set()  # 将线程从暂停状态恢复, 如果已经暂停的话
        self.__running.clear()  # 设置为False

        # 图色字符查找带单击右击或不点击+点击随机坐标和延时delay
        # return  [-1,-1,-1]   [0，100，200]
    def findPicStrE(self, pic, x, y, xend, yend, picStr2find, clr, sim=0.85, left="none", xrand=0, yrand=0,
                    delay=100):  # 最后3个参数，鼠标左右击/不单击，+x随机值，+y随机值
        if (pic == "pic"):
            dst1 = self.dm.FindPicE(x, y, xend, yend, picStr2find, clr, sim,
                                    0)  # 0|410|563  返回值:字符串:返回找到的图片序号(从0开始索引)以及X和Y坐标 形式如"index|x|y", 比如"3|100|200"
        else:
            dst1 = self.dm.FindStrE(x, y, xend, yend, picStr2find, clr,
                                    sim)  # 0|410|563  字符串:返回字符串序号以及X和Y坐标,形式如"id|x|y", 比如"0|100|200",没找到时，id和X以及Y均为-1，"-1|-1|-1"
        dst1 = dst1.__str__()[1:-1].split("|")
        dst1 = [int(i) for i in dst1]
        if (dst1[0] == -1):
            # print(f"没发现:{picStr2find}",dst1)
            self.dm.delay(delay)
            return [-1, -1, -1]
        else:
            # print(f"发现目标dst{picStr2find}",dst1,type(dst1))
            pass
            # print("dst", dst)
        if left == "none":
            pass
        else:
            # dst1 = [int(i) for i in dst1]  #坐标转整数
            # print("dst转为整数坐标",dst1)
            # self.dm.delay(100)
            self.dm.MoveTo(dst1[1] + xrand, dst1[2] + yrand)
            self.dm.delay(100)
            if left == "left":
                self.dm.LeftClick()
            else:
                self.dm.RightClick()
        self.dm.delay(delay)
        return dst1  # 【0，100，200】

    def qualify(self):
        if (self.findPicStrE("str",0, 0, 1500, 900, "请输入验证码", white_yanzhen, 0.85,left = "left",xrand = 44,yrand = 42)[0]== -1):
            #print("未发现——请输入验证码")
            return
        print("请跳入题目》》》》")
        #self.dm.delay(5000)       #TODO

        loc_submit = self.findPicStrE("str",0, 0, 1500, 900, "提交", white_yanzhen, 0.85)     #【0，100，200】

        if loc_submit[0] == -1:    #【0，100，200】
            return

        ques_type = self.findPicStrE("str",loc_submit[1]+yanzhen_kw[0],loc_submit[2]+yanzhen_kw[1],loc_submit[1]+yanzhen_kwEnd[0],
                             loc_submit[2]+yanzhen_kwEnd[1],"参考图|站在水中|白天|是否有",white_yanzhen,0.85)

        answer = 0  #1是yes，，2是no

        if  ques_type[0]==3:                  #伞琴自己答，直接答否
            #print("发现题型分类", ques_type)
            ques_type = "5001"
            answer = 2
        else:
            pic_cut = [loc_submit[1], loc_submit[2], loc_submit[1], loc_submit[2]]
            pic_add = [yanzhen_lt[0], yanzhen_lt[1], yanzhen_rb[0], yanzhen_rb[1]]
            pic_send = [pic_cut[i]+pic_add[i] for i in range(4)]

            if (ques_type[0]==-1):
            #print("未发现题型分类",ques_type)      #计算数目
                ques_type = "5021"
            elif  ques_type[0]==0:
                #print("发现题型分类", ques_type)      #坐标点
                ques_type = "6001"
                pic_add = [-350,-440,420,30]
                pic_send = [pic_cut[i]+pic_add[i] for i in range(4)]
            else:                                   #白天#TODO可以改成自己答！
                ques_type = "5001"    #2选1
                #题型为计数题
            file_dir = r"qualify\\" + str(self.hWnd) + "yanzhen.jpg"
            self.dm.CaptureJpg(pic_send[0], pic_send[1], pic_send[2], pic_send[3],file_dir, 100)
            self.dm.delay(200)
            #sys.exit()
            ret = fwsendfileex(r"D:\\QnSources\\"+file_dir, r"x371794554|C1B1C06152C827B4", ques_type, 50,
                               "头顶紫名者为NPC", "1001|9A42B0F1BD994C75")
            if len(ret) > 0 and ret[0] == "{":
                jsobj = json.loads(ret)
                errmsg = jsobj.get('errmsg', '')  # 错误返回值的示例请看 接口说明，同步函数需要同时看 “上传图片” 和 “获取答案”
                if errmsg != "":
                    print("#" + errmsg)  # https://www.showdoc.com.cn/fengwan/10258903646810375
                warnmsg = jsobj.get('warnmsg', '')  # 提醒信息，也需要看 接口说明，根据不同的返回值 修改答题流程逻辑
                if warnmsg != "":
                    print("#" + warnmsg)  # 提醒信息在一些情况下也应该结束本次的流程
                    # 如："答案不确定"    "图片有误"    "超时"
                tid = jsobj.get('tid', '')  # 任务流水号
                if tid != "": print("tid", tid)
                answer = jsobj.get('answer', '')  # 返回的答案，如果↑有异常，则答案为空字符串
                if answer != "":
                    print("answer", answer)
                    if (ques_type == "5001"):  #是否点击
                        answer = int(answer)
                    elif (ques_type == "5021"):#保留文本，keyPressChar用上
                        pass
                    else:   #单坐标“6001”     ret = "12,34"
                        #answer = "11,12"
                        answer = answer.split(",")
                        answer = [int(answer[i]) for i in range(2)]
            else:
                print("异常返回值：", ret)
        if(ques_type == "5001"):
            self.dm.MoveTo(loc_submit[1]+80*answer-355,loc_submit[2]+yanzhen_no[1])  #移动到□是，□否
            self.dm.delay(250)
            self.dm.LeftClick()
            self.dm.delay(250)
        elif(ques_type == "5021"):
            self.dm.MoveTo(loc_submit[1] + yanzhen_calc[0], loc_submit[2] ++ yanzhen_calc[1])  # 移动到□是，□否
            self.dm.delay(250)
            self.dm.LeftClick()
            self.dm.delay(250)
            self.dm.KeyPressChar(answer)
        else:
            self.dm.MoveTo(pic_send[0] + answer[0], pic_send[1] + answer[1])  # 移动到□是，□否
            self.dm.delay(250)
            self.dm.LeftClick()
        #提交按钮
        self.dm.MoveTo(loc_submit[1] + 20, loc_submit[2] + 6)
        self.dm.delay(250)
        self.dm.LeftClick()

if __name__ == '__main__':
    #id,name,job,level,buffs,*args  789388
    title_name = '547550304'
    p = Player(id = title_name,name = "郭小志",job="ny",buffs_num=3,buff_seconds="600*600*600")
    p.dm.KeyPressChar("F10")
    time.sleep(3)
    p.findAndPick("hello")
    #p.qualify()
    p.dm.UnBindWindow()
