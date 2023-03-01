from shutil import copyfile
import traceback
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
from win32api import ShellExecute
import configparser
from Downloard_src import download
import os

VERSION = "1.1.6"
AUTHOR = "Moxiner"
url_background = "http://www.moxiner.fun:8888/down/PGLZPZNTCwlA"
url_ico = "http://www.moxiner.fun:8888/down/mV6jhjXZfacB"
url_config = "http://www.moxiner.fun:8888/down/bevt6xtAstDZ"
url_pcgameSDK = "http://www.moxiner.fun:8888/down/rnlsPtzNKAXi"
Error = []

def ErrorMessage(Error = "未知错误，请联系开发者！"):
    ErrorInfo = f'''
==========================================
原神启动器Ex遇到了一些错误   版本 {VERSION}
==========================================
{Error}
==========================================
报错代码 
==========================================
{traceback.format_exc()}       
'''
    messagebox.showerror(title="错误", message=str(ErrorInfo))


def readConfig():
    '''读取配置文件'''
    try:
        global NOTE
        global VERSION
        global GamePath
        config = configparser.ConfigParser()
        config.read("YuanShenEx.ini", encoding="utf8")
        GamePath = config.get("url" , "gamepath") 
        config.read(GamePath + "/config.ini", encoding="utf8")
        GAME_VERSON = config.get("General", "game_version")
        NOTE = f"欢迎使用原神启动器EX    游戏版本 {GAME_VERSON}    作者 {AUTHOR}"
    except:
        Error.append("\n找不到配置文件\n请将启动器移动至游戏目录\n并确保目录里有 config.ini")
        NOTE = "读取配置文件失败 , 未找到游戏文件" 


def mihoyo():
    '''将配置文件改成官服配置并启动游戏'''
    try:
        global NOTE
        config = configparser.ConfigParser()

        config.read(GamePath + "/config.ini" , encoding="utf8")
        config.set("General", "channel", "1")
        config.set("General", "cps", "mihoyo")
        config.set("General", "sub_channel", "1")
        config.write(open(GamePath + "/config.ini", "w"))
        try:
            ShellExecute(0, 'open', GamePath  + "/YuanShen.exe" , '' ,GamePath , 1)
        except:
            ErrorMessage("\n找不到游戏本体\n请将启动器移动至游戏目录\n并确保目录里有 yuanshen.exe 文件")
    except:
        ErrorMessage("\n找不到配置文件\n请将启动器移动至游戏目录\n并确保目录里有 config.ini 文件")


def bilibili():
    '''将配置文件改成B服配置并启动游戏'''
    try:
        global NOTE
        config = configparser.ConfigParser()
        config.read(GamePath + "/config.ini", encoding="utf8")
        config.set("General", "channel", "14")
        config.set("General", "cps", "bilibili")
        config.set("General", "sub_channel", "0")
        config.write(open(GamePath + "/config.ini", "w"))
        try:
            ShellExecute(0, 'open', GamePath + "/YuanShen.exe"  , '', GamePath, 1)
        except:
            ErrorMessage("\n找不到游戏本体\n请将启动器移动至游戏目录\n并确保目录里有 yuanshen.exe 文件")
    except:
        ErrorMessage("\n找不到配置文件\n请将启动器移动至游戏目录\n并确保目录里有 config.ini 文件")


def fixbug():
    '''一键修复'''
    try:
        download(url_pcgameSDK, "src/PCGameSDK.dll")
        download(url_config, "src/config.ini")
        download(url_background, "src/background.png")
        copyfile("src/PCGameSDK.dll", GamePath + "/YuanShen_Data/Plugins/PCGameSDK.dll")
        copyfile("src/config.ini", GamePath + "/config.ini")
        copyfile("src/background.png", GamePath + "/background.png")
        messagebox.showinfo(title="修复完成", message="修复完成，请选择启动服务器")
    except FileNotFoundError:        
        messagebox.showinfo(title="修复失败", message="修复失败，无法连接至服务器")
    except:
        ErrorMessage("\n找不到游戏本体\n请将启动器移动至游戏目录\n并确保目录里有 PCGameSDK.dll 文件")
    # 删除游戏目录多余文件
    try:
        if os.path.exists(GamePath + "/src"):
            os.removedirs(GamePath + "/src")
        if os.path.exists(GamePath + "/Launcher.exe"):
            os.remove(GamePath + "/Launcher.exe")
        if os.path.exists(GamePath + "/Launcher.exe"):
            os.remove(GamePath + "/Install.exe")
        if os.path.exists(GamePath + "/Installer.exe"):
            os.remove(GamePath + "/Installer.exe")
    except Exception:
        pass            


def main():
    '''主函数'''
    # 创造窗口
    global Note
    global Window
    Window = tk.Tk()
    Window.title(f"原神启动器Ex {VERSION}")
    try:
        Window.iconbitmap("src/ico.ico")
    except:
       Error.append("\n缺少资源文件 src\\ico.ico \n请重新解压压缩包内所有文件！") 
    canvas = tk.Canvas(Window, width=1280, height=720, bd=0, highlightthickness=0)
    Window_frame1 = tk.Frame(canvas)
    Window_frame2 = tk.Frame(canvas)

    # 加载背景图片
    try:
        bg_load = Image.open("src/background.png")
        bg_img = ImageTk.PhotoImage(bg_load)
    except:
        Error.append("\n缺少资源文件 src\\background.png \n请重新解压压缩包内所有文件！")
        download(url_background, "src/background.png")
        download(url_ico, "src/background.png")
    bg_load = Image.open("src/background.png")
    bg_img = ImageTk.PhotoImage(bg_load)
    canvas.create_image(640, 360, image = bg_img)
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
    except Exception as E:
        ErrorMessage()


