from tkinter import *

# coding=utf-8
from tkinter import *
#from ttk import *
import threading
import time
import sys
from queue import Queue

def fmtTime(timeStamp):
    timeArray = time.localtime(timeStamp)
    dateTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return dateTime


# 自定义re_Text,用于将stdout映射到Queue
class re_Text():
    def __init__(self, queue):
        self.queue = queue
    def write(self, content):
        self.queue.put(content)

class QNGUI():
    def __init__(self, root):
        # new 一个Quue用于保存输出内容
        self.msg_queue = Queue()
        self.frms = []
        self.initGUI(root)

    # 在show_msg方法里，从Queue取出元素，输出到Text
    def show_msg(self):

        while not self.msg_queue.empty():
            content = self.msg_queue.get()
            self.text.insert(INSERT, content)
            self.text.see(END)

        # after方法再次调用show_msg
        self.root.after(100, self.show_msg)

    def initGUI(self, root):

        self.root = root
        self.root.title("倩女主控中心")
        self.root.geometry("800x1000+700+500")
        self.root.resizable = False

        for i in range (8):
            frm = Frame(root,name="team"+str(i+1),relief = "sunken",bd =2,padx=15,pady = 15)

            self.frms.append(frm)
            self.frms[i].grid(row=i//2,column=i%2)
            label1 = Label(frm,text ="增删队伍成员",padx=5)
            label2 = Label(frm, text="捡钱",padx=5)
            label3 =Label(frm, text="加buff",padx=5)
            label4 =Label(frm, text="公共任务",padx=5)
            label1.grid(row = 0,column=0,columnspan=2)
            label2.grid(row=0, column=2)
            label3.grid(row=0, column=3)
            label4.grid(row=0, column=4)

            button = Button(frm,text ="+")
            button.grid(row=1, column=0)



        # 启动after方法
        self.root.after(100, self.show_msg)

        root.mainloop()

    def __show(self):

        i = 0
        while i < 3:
            print  (fmtTime(time.time()) )
            time.sleep(1)
            i += 1

    def show(self):
        T = threading.Thread(target=self.__show, args=())
        T.start()


if __name__ == "__main__":
    root = Tk()
    myGUI = QNGUI(root)
