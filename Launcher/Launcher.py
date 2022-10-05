from cgitb import text
from copy import copy
from shutil import copyfile
from PIL import Image, ImageTk
from tkinter import END, messagebox, font
import tkinter as tk
from PIL import Image, ImageTk
import os
import configparser
from Downloard_src import download

VERSION = "1.1.0-Pre"
AUTHOR = "Moxiner"
url_bg = "https://github.com/Moxiner/YuanShenEx_Launcher/blob/main/src/background.png"
url_ico = "https://github.com/Moxiner/YuanShenEx_Launcher/blob/main/src/ico.ico"
url_PCGameSDK = "https://wwu.lanzouy.com/iQE6V0cvyd2d"
url_config = ""


def readConfig():
    '''读取配置文件'''
    try:
        global NOTE
        global VERSION
        config = configparser.ConfigParser()
        config.read("Config.ini")
        GAME_VERSON = config.get("General", "game_version")
        NOTE = f"欢迎使用原神启动器EX    游戏版本 {GAME_VERSON}    作者 {AUTHOR}"
    except:
        messagebox.showerror(title="找不到配置文件", message="找不到配置文件\n请将启动器移动至游戏目录\n并确保目录里有 Config.ini")
        NOTE = "读取配置文件失败 , 未找到游戏文件"


def mihoyo():
    '''将配置文件改成官服配置并启动游戏'''
    try:
        global NOTE
        config = configparser.ConfigParser()
        config.read("Config.ini")
        config.set("General", "channel", "1")
        config.set("General", "cps", "mihoyo")
        config.set("General", "sub_channel", "1")
        config.write(open("Config.ini", "w"))
        try:
            os.system("start yuanshen.exe")
        except:
            messagebox.showerror(title="找不到配置文件", message="找不到游戏本体\n请将启动器移动至游戏目录\n并确保目录里有 yuanshen.exe 文件")
    except:
        messagebox.showerror(title="找不到配置文件", message="找不到配置文件\n请将启动器移动至游戏目录\n并确保目录里有 Config.ini 文件")


def bilibili():
    '''将配置文件改成B服配置并启动游戏'''
    try:
        global NOTE
        config = configparser.ConfigParser()
        config.read("Config.ini")
        config.set("General", "channel", "14")
        config.set("General", "cps", "bilibili")
        config.set("General", "sub_channel", "0")
        config.write(open("Config.ini", "w"))
        try:
            os.system("start yuanshen.exe")
        except:
            messagebox.showerror(title="找不到配置文件", message="找不到游戏本体\n请将启动器移动至游戏目录\n并确保目录里有 yuanshen.exe 文件")
    except:
        messagebox.showerror(title="找不到配置文件", message="找不到配置文件\n请将启动器移动至游戏目录\n并确保目录里有 Config.ini 文件")


def fixbug():
    '''一键修复'''
    try:
        copyfile("../installer/src/PCGameSDK.dll", "YuanShen_Data/Plugins/PCGameSDK.dll")
        copyfile("installer/src/config.ini", "config.ini")
        messagebox.showinfo(title="修复完成", message="修复完成，请选择启动服务器")
    except FileNotFoundError:
        download(url_PCGameSDK, "../installer/src/PCGameSDK.dll")
        copyfile("../installer/src/PCGameSDK.dll", "YuanShen_Data/Plugins/PCGameSDK.dll")
        download(url_config, "installer/src/config.ini")
        copyfile("installer/src/config.ini", "config.ini")


def main():
    '''主函数'''
    # 创造窗口
    global Note
    global Window
    Window = tk.Tk()
    Window.title(f"原神启动器 {VERSION}")
    try:
        Window.iconbitmap("./src/ico.ico")
    except:
        messagebox.showerror(title="缺少文件", message="缺少资源文件 src\\ico.ico \n请重新解压压缩包内所有文件！")
    canvas = tk.Canvas(Window, width=1280, height=720, bd=0, highlightthickness=0)
    Window_frame1 = tk.Frame(canvas)
    Window_frame2 = tk.Frame(canvas)

    # 加载背景图片
    try:
        bg_load = Image.open("../installer/src/background.png")
        bg_img = ImageTk.PhotoImage(bg_load)
    except:
        # messagebox.showerror(title="缺少文件" , message="缺少资源文件 src\\background.png \n请重新解压压缩包内所有文件！")
        download(url_bg, "../installer/src/background.png")
        download(url_ico, "../installer/src/background.png")
    canvas.create_image(640, 360, image=bg_img)
    # 绘制控件
    mihoyo_button = tk.Button(Window_frame1, text="启动官服", width=23, command=mihoyo, height=40, background="#FFCB20",
                              bd=0, activebackground="#d2a617", font=("微软雅黑", 12, "bold"), fg="#89601A")
    bilibili_button = tk.Button(Window_frame1, text="启动B服", width=23, command=bilibili, height=40, background="#FFCB20",
                                bd=0, activebackground="#d2a617", font=("微软雅黑", 12, "bold"), fg="#89601A")
    fixbug_button = tk.Button(Window_frame2, text="一键修复", width=47, command=fixbug, height=40, background="#efefef",
                              bd=0, activebackground="#9d9d9d", font=("微软雅黑", 12, "bold"))
    Window_frame1.pack(side="left")
    Window_frame2.pack(side="left")
    mihoyo_button.pack(side="left")
    bilibili_button.pack(side="left")
    fixbug_button.pack(side="top")
    canvas.create_window(1000, 560, width=470, height=60, window=Window_frame1)
    canvas.create_window(1000, 630, width=470, height=45, window=Window_frame2)
    Note = canvas.create_text(1260, 710, text=NOTE, anchor="se", font=("微软雅黑", 10,), fill="white")
    canvas.pack()

    # 绘制窗口属性
    Window.resizable(width=False, height=False)
    x_cordinate = int((Window.winfo_screenwidth() / 2) - (1280 / 2))
    y_cordinate = int((Window.winfo_screenheight() / 2) - (720 / 2))
    Window.geometry("1280x720+{}+{}".format(x_cordinate, y_cordinate - 20))
    Window.mainloop()


if __name__ == "__main__":
    try:
        readConfig()
        main()
    except Exception as Error:
        messagebox.showerror(title="致命错误", message=str(Error))