# ! /usr/bin/env python
# -*- coding: utf-8 -*-
from win32gui import IsWindow, IsWindowEnabled, IsWindowVisible, EnumWindows, GetClassName
from win32gui import GetWindowText


def get_class_winds(class_name=None):
    if (class_name == None):  return -1

    titles = set()

    def foo(hwnd, mouse):
        # 去掉下面这句就所有都输出了，但是我不需要那么多
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            if (GetClassName(hwnd) == class_name):     titles.add(hwnd)

    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    lt.sort()
    # for t in lt:
    #     print(t)
    return lt


def get_title_winds(title_name=None, subset=1):
    if (title_name == None):  return -1

    titles = set()

    def foo(hwnd, mouse):
        # 去掉下面这句就所有都输出了，但是我不需要那么多
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            if (subset):
                if (title_name in GetWindowText(hwnd)):
                    titles.add(hwnd)

            if (GetWindowText(hwnd) == title_name):     titles.add(hwnd)

    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    lt.sort()
    return lt


if __name__ == '__main__':
    # class_name = "新倩女幽魂"
    # title_wind = get_class_winds(class_name)
    # print(title_wind)
    title_name = '44191210292'
    titles = get_title_winds(title_name)
    print(titles,type(titles[0]))
