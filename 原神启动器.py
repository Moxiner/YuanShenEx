
from PIL import Image ,ImageTk
from tkinter import END, messagebox , font
import tkinter as tk 
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import os
import configparser

def mihoyo():
    try:
        config = configparser.ConfigParser()
        config.read("Config.ini")
        config.set("General","channel","1")
        config.set("General","cps","mihoyo")
        config.set("General","sub_channel","1")
        config.write(open("Config.ini", "w"))
    except:
        messagebox.showerror(title="找不到配置文件" , message="找不到配置文件\n请将启动器移动至游戏目录\n并确保目录里有 Config.ini 文件")
    try:
        os.system("start yuanshen.exe")                
    except:
        messagebox.showerror(title="找不到配置文件" , message="找不到游戏本体\n请将启动器移动至游戏目录\n并确保目录里有 yuanshen.exe 文件")
    

    


def bilibili():
    try:
        config = configparser.ConfigParser()
        config.read("Config.ini")
        config.set("General","channel","14")
        config.set("General","cps","bilibili")
        config.set("General","sub_channel","0")
        config.write(open("Config.ini", "w"))
    except:
        messagebox.showerror(title="找不到配置文件" , message="找不到配置文件\n请将启动器移动至游戏目录\n并确保目录里有 Config.ini 文件")
    try:
        os.system("start yuanshen.exe")
    except:
        messagebox.showerror(title="找不到配置文件" , message="找不到游戏本体\n请将启动器移动至游戏目录\n并确保目录里有 yuanshen.exe 文件")
    


def main():
    global Window
    Window = tk.Tk()
    Window.title("原神启动器")
    # Window.iconbitmap("ico.ico")
    canvas = tk.Canvas(Window, width=1280,height=720,bd=0, highlightthickness=0)
    Window_frame = tk.Frame(canvas)
    bg_load = Image.open("img.png")
    bg_img = ImageTk.PhotoImage(bg_load)
    



    canvas.create_image(640, 360, image=bg_img)
    mihoyo_button = tk.Button(Window_frame , text="启动官服",width=27 , command=mihoyo ,height=40 ,background="#FFCB20" ,bd=0 ,activebackground="#d2a617")
    bilibili_button = tk.Button(Window_frame , text="启动B服",width=27 ,command=bilibili ,height=40 , background="#FFCB20" , bd=0 ,activebackground="#d2a617")
    Window_frame.pack(side="left")
    mihoyo_button.pack(side="left")
    bilibili_button.pack(side="left")
    canvas.create_window(1000, 610, width=380, height=60 , window = Window_frame)
    canvas.pack()



    x_cordinate = int((Window.winfo_screenwidth() / 2) - (1280 / 2))
    y_cordinate = int((Window.winfo_screenheight() / 2) - (720 / 2))
    Window.geometry("1280x720+{}+{}".format(x_cordinate, y_cordinate-20))
    Window.mainloop()

if __name__ == "__main__":
    main()