import sys
import tkinter
from tkinter import *
from tkinter import messagebox

from tkinter import ttk

from pydmsoft.play import Player


class Team(Frame):
    def __init__(self, master=None,name = None):
        super().__init__(master)  # super()代表的是父类的定义，而不是父类对象
        self.master = master
        self.name = name
        self.pack()
        self.createWidget()

    def createWidget(self):
        """创建登录界面的组件"""
        self.label00 = Label(self, text="序号")
        self.label00.grid(row=0,column=0)


        self.entry01 = Entry(self, text="",width=12)
        #self.entry01.insert(0, "队伍序号:")
        self.entry01.grid(row=0, column=1)


        self.button02 = Button(self,text = "队序全加",command = lambda : self.loadAccount("test"))
        self.button02.grid(row=0,column=2)

        self.var03 = tkinter.StringVar()
        self.var03.set("全体buff")
        self.button03 = Button(self,textvariable =self.var03,command=lambda: self.buffAll("全员buff"))
        self.button03.grid(row=0,column=3)

        self.var04= tkinter.StringVar()
        self.var04.set("拾取物品")
        self.button04 = Button(self, textvariable=self.var04, command=lambda: self.pickFloor("拾取物品"))
        self.button04.grid(row=0,column=4)

        self.var05 = tkinter.StringVar()
        self.var05.set("野外采集")
        self.button05 = Button(self, textvariable=self.var05,command=lambda: self.collOutDoor("野外拾取"))
        self.button05.grid(row=0,column=5)

        self.button06 = Button(self, text="添加任务》")
        self.button06.grid(row=0,column=6)

        self.button07 = Button(self, text="《删除任务")
        self.button07.grid(row=0,column=7)

        self.column0_orderLabs = []       #序号label
        self.column1_menberEtrs = []      #队员ID输入框
        self.column1_entryVar = []
        self.column2_loadBtns = []        #单独加载按钮
        self.column3_buffChes = []        #加buff的check状态
        self.column4_pickChes = []        #拾取物品check状态
        self.column5_collChes = []        #野外采集check状态
        self.playersDict = {}             #队伍里的玩家列表

        for i in range(6):
            label = Label(self,text=str(i+1))
            label.grid(row=i+1,column=0)

            textV= tkinter.StringVar()
            textV.set("")
            entry = Entry(self,textvariable=textV,width=12)
            entry.grid(row=i+1,column=1)

            # textAdd = tkinter.StringVar()
            # textAdd.set("手动添加")
            button = Button(self,text="手动添加",command= lambda :self.addManually(i))          #同一个回调函数，传参变为最后一个

            button.grid(row = i+1,column=2)

            buff = Checkbutton(self)
            buff.grid(row = i+1,column = 3)

            pick = Checkbutton(self)
            pick.grid(row = i+1,column = 4)

            coll = Checkbutton(self)
            coll.grid(row = i+1,column = 5)
            #print("buff",buff)
            self.column1_entryVar.append(textV)
            self.column0_orderLabs.append(label)
            self.column1_menberEtrs.append(entry)
            self.column2_loadBtns.append(button)
            self.column3_buffChes.append(buff)
            self.column4_pickChes.append(pick)
            self.column5_collChes.append(coll)

        # for i in range(6):
        #     print(self.column2_loadBtns[i])

        var2 = StringVar()
        self.list06 = Listbox(self, listvariable=var2, width=12).grid(row=1, column=6, rowspan=6)
        var2.set(("秋江", "桃花", "青蛙", "兔子"))

        var3 = StringVar()
        self.list07 = Listbox(self, listvariable=var3, width=12).grid(row=1, column=7, rowspan=6)
        var3.set(("三环", "大盗宝藏", "河伯", "布袋"))

        # # StringVar变量绑定到指定的组件。
        # # StringVar变量的值发生变化，组件内容也变化；
        # # 组件内容发生变化，StringVar变量的值也发生变化。
        #
        # v1 = StringVar()
        # self.entry01 = Entry(self, textvariable=v1)
        # self.entry01.pack()
        # v1.set("admin")
        # print(v1.get());
        # print(self.entry01.get())
        #
        # # 创建密码框
        # self.label02 = Label(self, text="密码")
        # self.label02.pack()
        #
        # v2 = StringVar()
        # self.entry02 = Entry(self, textvariable=v2, show="*")
        # self.entry02.pack()
        # Button(self, text="登陆", command=self.login).pack()


    def addManually(self,order):
        self.column1_entryVar[3].get()
        print("order",order)
        print("self.column1_menberEtrs",self.column1_menberEtrs)
        print(self.column1_menberEtrs[3])
        id = self.column1_entryVar[3].get().strip()       #只有最后一个有ID
        print("ididididid:",id)
        if id == "":
            print("没有id")
            sys.exit()

        with open(r'D:\QnSources\account\accounts.txt', 'r', encoding='utf-8') as f:
            count = 0  # 下一个#结束
            lineList = []
            while (count < 2 ):
                line = f.readline().strip()
                if line.startswith(id):
                    line = line.split(",")

                    break

            print(lineList)
        self.playersDict[id] = Player(id)
        print(self.playersDict)
        pass


    def loadAccount(self,str):
        print("read files",str)
        order = self.entry01.get().strip()
        if  order == "":
            print ("队伍序号为空")
        else:
            with open(r'D:\QnSources\account\accounts.txt', 'r', encoding='utf-8') as f:
                count = 0  #下一个#结束
                lineList = []
                while(count<2):
                    line = f.readline().strip()
                    if count == 1:
                        #print(line)
                        if line.startswith("#"):
                            pass
                        else:
                            lineList.append(line.split(","))
                    if line.startswith("#"+order):
                        count += 1
                    elif line.startswith("#")  and count == 1:
                        count = 2
                print(lineList)
                #sys.exit()
                for i in range(len(lineList)):
                    id = lineList[i][0].strip()
                    self.column1_menberEtrs[i].delete(0, "end")
                    self.column1_menberEtrs[i].insert(0, id)
                    print("lineList[i][4].strip():",lineList[i][4].strip())
                    self.playersDict[id] = Player(id,lineList[i][1].strip(),lineList[i][2].strip(),lineList[i][3].strip(),lineList[i][4].strip())
                    print(self.playersDict)
                while(i < 5):
                    i+=1
                    self.column1_menberEtrs[i].delete(0, "end")




    def buffAll(self,str):
        if self.var03.get() == "全体buff":
            for i in range(6):
                #print(self.column3_buffChes[i])
                self.column3_buffChes[i].select()
                self.var03.set("全去buff")
        else:
            for i in range(6):
                #print(self.column3_buffChes[i])
                self.column3_buffChes[i].deselect()
                self.var03.set("全体buff")

    def pickFloor(self,str):
        if self.var04.get() == "拾取物品":
            for i in range(6):
                #print(self.column4_buffChes[i])
                self.column4_pickChes[i].select()
                self.var04.set("不拾物品")
        else:
            for i in range(6):
                #print(self.column4_buffChes[i])
                self.column4_pickChes[i].deselect()
                self.var04.set("拾取物品")

    def collOutDoor(self,str):
        if self.var05.get() == "野外采集":
            for i in range(6):
                #print(self.column4_buffChes[i])
                self.column5_collChes[i].select()
                self.var05.set("野花不采")
        else:
            for i in range(6):
                #print(self.column4_buffChes[i])
                self.column5_collChes[i].deselect()
                self.var05.set("野外采集")

    def login(self):
        username = self.entry01.get()
        pwd = self.entry02.get()

        print("去数据库比对用户名和密码！")
        print("用户名：" + username)
        print("密码：" + pwd)

        if username == "gaoqi" and pwd == "123456":
            messagebox.showinfo("学习系统", "登录成功！欢迎开始学习！")
        else:
            messagebox.showinfo("学习系统", "登录失败！用户名或密码错误！")


if __name__ == '__main__':
    root = Tk()
    root.geometry("800x600+200+300")
    app = Team(master=root)
    root.mainloop()