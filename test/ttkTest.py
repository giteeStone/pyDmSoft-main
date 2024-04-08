from tkinter import *

from tkinter import ttk
from ComBoPicker import Combopicker  # 导入自定义下拉多选框
from ComBoPicker1 import Combopicker as Combopicker1  # 导入自定义下拉多选框

if __name__ == "__main__":
    root = Tk()
    root.geometry("300x300")

    F = Frame(root)
    F.pack(expand=False, fill="both", padx=10, pady=10)
    Label(F, text='全选、可滚动：').pack(side='left')
    COMBOPICKER = Combopicker(F,
                              values=['全选', '项目1', '项目2', '项目3', '项目4', '项目5', '项目11', '项目22', '项目33', '项目44', '项目55'])
    COMBOPICKER.pack(anchor="w")

    F2 = Frame(root)
    F2.pack(expand=False, fill="both", padx=10, pady=10)
    Label(F2, text='普通：').pack(side='left')
    COMBOPICKER1 = Combopicker1(F2, values=[f'项目{i}' for i in range(5)])
    COMBOPICKER1.pack(anchor="w")

    root.mainloop()

