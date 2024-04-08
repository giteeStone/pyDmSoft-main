import sys
import time

from pydmsoft import DM, TimeOutException
from pydmsoft.enum_wind import get_title_winds

green_mapName = "66ff00-101010"
green_underline = "00ff00-101010"  #一条色素下化线(导航线）
green_arm ="00ff00-101010"
green_shuilao = "66ff00-202020"

red_mapName= "ff2d2d-101010"
red_mapMonster = "ff1c29-303030"
red_notPickable = "ff0000-101010"
red_blood = "c33839-353535"         #角色血条
red_lightArm = "ff5050-101010"
red_darkArm = "ff0000-101010"

blue_magic = "29bbe4-303030"
blue_darkArm = "0c5bc8-101010"
blue_lightArm = "519fff-101010"

yellow_blood = "edb206-202020"
yellow_lightArm = "fffe91-101010"
yellow_darkArm ="fa800a-101010"

white_money = "ffffff-202020"
white_jobFollow = "ffffc5-202020"
white_yanzhen = "ffffff-202020"

# = "ffffff-202020"      #请输入验证码

map_pujiacun = [[286,400],]
map_lanruoDG = [[266,134],]
map_fengdu = [[217,210],]
map_cangjinDG = [[278,291],]
map_foshenDG = [[167,440],]
map_zhenjiaoHY = [[446,311],]
#验证码的定位
yanzhen_lt =[-343,-438]  #左上角
yanzhen_rb =[76,34]   #右下角
yanzhen_kw = [-335,-103]  ##选找关键字左上角 判断题型
yanzhen_kwEnd = [61,-50]  ##关键字右下角结束
yanzhen_yes = [-275,-25]  #选择题
yanzhen_no = [-195,-25]  #选择题
yanzhen_calc = [-300,5]        #填空位置


if __name__ == '__main__':

    title_name = '459110736'
    hwnds = get_title_winds(title_name)
    print(hwnds, type(hwnds[0]))
    dm = DM(r"D:\\damo\\7.2410\\RegDll.dll", r"D:\\damo\\7.2410\\dm.dll")
    # print(m_dm,type(m_dm))
    try:
        print("注册结果", dm.Reg(r'jv965720b239b8396b1b7df8b768c919e86e10f', r'jn5gun14k4ep1y7'))
        m_ret = dm.BindWindowEx(hwnds[0], "gdi", "windows", "windows","dx.mouse.position.lock.api|dx.mouse.position.lock.message", 0)
        #m_ret = dm.BindWindow(199608, "gdi", "windows", "windows" , 0)
        print("绑定结果m_ret:", m_ret)
        if (m_ret != 1):
            print("绑定失败:name:")
        else:
            print("绑定成功")

    except TimeOutException as e:
        print(e)
        sys.exit()

    dm.SetPath(r"D:\QnSources")

    # ret = dm.SetWindowState(hwnds[0],1)
    # dm.delay(1000)
    # dm.MoveTo(665,229)
    # dm.delay(1000)
    # dm.LeftClick()

    # dm.delay(1000)
    # _,posx,posy= dm.GetCursorPos()
    # print("posx,posy",posx,posy)
    #
    # dm.RightClick()
    # print("激活窗体",ret)  ####！！
    #dm.KeyDownChar("alt")
    # dm.delay(3000)
    # dm.CaptureJpg(0,0,800,600,"test11.jpg",60)
    # dm.delay(1000)

    ###############################找图找图找图找图找图找图找图找图找图找图找图1111111111
    # ret = dm.FindPicE(0,0,800,800,r"2.bmp","303030",0.9,0)  #qualify\login
    # print("FindPicE：", ret)        #FindPicE： 0|410|563
    # dm.delay(1000)
    # ret = ret.split("|")
    # red1 = dm.MoveTo(ret[1], ret[2])
    # dm.delay(1000)
    # dm.LeftDown()
    # dm.delay(1000)
    # red1 = dm.MoveTo(566, 566)
    # dm.delay(1000)
    # dm.LeftUp()
    ############################################## 找图找图找图找图找图找图找图找图找图找图找图22222222222

    ret = dm.FindPicE(0, 0, 800, 800, r"drug.bmp", "303030", 0.9, 0)
    print("FindPicE：", ret)  # FindPicE： 0|410|563
    dm.delay(1000)
    ret = ret.split("|")
    red1 = dm.MoveTo(ret[1], ret[2])
    dm.delay(1000)
    _, posx, posy = dm.GetCursorPos()
    print("posx,posy",posx,posy)
    dm.LeftClick()
    dm.delay(1000)
    #red1 = dm.MoveTo(566, 566)
    dm.SendString(199608,"Wj123456789")
    dm.delay(1000)
    dm.MoveTo(365,403)
    dm.delay(1000)
    dm.LeftClick()
    #dm.LeftUp()
    #sys.exit()
    #############################################


    #################
    #找字找字找字找字找字找字找字找字找字找字找字,还有fast系列
    dm.SetDict(0, "dict\yinzi.txt")
    ret = dm.UseDict(0)
    ret = dm.FindStr(0, 0, 800, 600, "水牢|任务追踪", white_jobFollow, 0.9)
    print("FindStr：__str__()", ret.__str__())  #FindStr： (0, 663, 5),建议用下面的
    ret = dm.FindStrE(0,0,800,600,"水牢|任务追踪",green_shuilao,0.9)   #find str '0|663|5'
    print("FindStrE：",ret)    #FindStr： (0, 663, 5)    FindStrE： '0|663|5'
    ret = dm.FindStrEx(0, 0, 800, 600, "任务追踪|水牢", green_shuilao,0.9)  #"id,x0,y0|id,x1,y1|......|id,xn,yn"
    print("FindStrEx：", ret)    #FindStrEx： 1,663,5
    ret = ret.split("|")[0].split(",")


    #按键和鼠标按键和鼠标按键和鼠标按键和鼠标按键和鼠标   组合键alt+E，鼠标移动与定位
    #dm.KeyPressChar("tab")
    # _,posx,posy= dm.GetCursorPos()
    # print("pos1",posx,posy)
    # time.sleep(1)
    # dm.delay(300)
    # dm.KeyPressChar("N")
    # ret3 = dm.MoveTo(299,356)
    # dm.CaptureJpg(0,0,800,600,"test.jpg",90)
    #dm.LeftClick()
    # ret = ret.split("|")
    red1 = dm.MoveTo(ret[1], ret[2])

    dm.delay(2000)

    ret = dm.GetCursorPos()
    print("鼠标移动后的位置", ret)
    # dm.delay(300)
    #red1 = dm.MoveTo(366, 388)
    dm.delay(2000)
    #red1 = dm.LeftUp()
    # #print("ret2", ret2)
    # dm.UnBindWindow()
    #ret = dm.FindPic(0, 0, 800, 800, r"cache\3.bmp|cache\2.bmp", "101010", 0.9, 0)
    #ret1 = dm.FindPicEx(0, 0, 800, 800, r"cache\2.bmp", "000000-000000", 0.9, 0)
    #print(ret.__str__(), ret1, type(ret), type(ret1))
    pass

