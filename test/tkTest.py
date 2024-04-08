from tkinter import *
#from ttk import *
import time


class GUI():

    def __init__(self, root):
        self.initGUIf(root)

    def initGUI(self, root):
        root.title("test")
        root.geometry("400x200+700+500")
        root.resizable = False

        self.button_1 = Button(root, text="run A", width=10, command=self.A)
        self.button_1.pack(side="top")

        self.button_2 = Button(root, text="run B", width=10, command=self.B)
        self.button_2.pack(side="top")

        root.mainloop()

    def A(self):
        print        ("start to run proc A")
        time.sleep(3)
        print       ( "proc A finished")

    def B(self):
        print         ("start to run proc B")
        time.sleep(3)
        print       ("proc B finished")


if __name__ == "__main__":
    root = Tk()
    myGUI = GUI(root)
