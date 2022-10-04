
import os
import configparser
from shutil import copyfile
from Downloard_src import download

VERSION = "1.1.0-Pre"
AUTHOR = "Moxiner"
url_bg = "https://github.com/Moxiner/YuanShenEx_Launcher/blob/main/src/background.png"
url_ico = "https://github.com/Moxiner/YuanShenEx_Launcher/blob/main/src/ico.ico"
url_PCGameSDK = "https://wwu.lanzouy.com/iQE6V0cvyd2d"
url_config = ""
def readConfig():
    '''读取配置文件'''
    global NOTE
    global VERSION
    config = configparser.ConfigParser()
    config.read("Config.ini")
    GAME_VERSON = config.get("General","game_version" ) 
    NOTE = f"欢迎使用原神启动器EX    游戏版本 {GAME_VERSON}    作者 {AUTHOR}"
    NOTE = "读取配置文件失败 , 未找到游戏文件"
def mihoyo():
    '''将配置文件改成官服配置并启动游戏'''
    global NOTE
    config = configparser.ConfigParser()
    config.read("Config.ini") 
    config.set("General","channel","1")
    config.set("General","cps","mihoyo")
    config.set("General","sub_channel","1")
    config.write(open("Config.ini", "w"))
    os.system("start yuanshen.exe")            


def bilibili():
    '''将配置文件改成B服配置并启动游戏'''
    global NOTE
    config = configparser.ConfigParser()
    config.read("Config.ini")
    config.set("General","channel","14")
    config.set("General","cps","bilibili")
    config.set("General","sub_channel","0")
    config.write(open("Config.ini", "w"))
    os.system("start yuanshen.exe")                 
def fixbug():
    '''一键修复'''
    copyfile("src/PCGameSDK.dll" , "YuanShen_Data/Plugins/PCGameSDK.dll")
    copyfile("src/config.ini" , "config.ini")
def main():
    if __name__ == "__main__":
        readConfig()
        main()