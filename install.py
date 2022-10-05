# @ Created with PyCharm Community Edition
# @ Author Morbid
# @ Date 2022/10/04
# @ Time 20:47
import configparser
from os import makedirs, path, symlink
from shutil import copyfile, copy, copytree
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
from win32ui import CreateFileDialog
from win32api import MessageBox
from win32con import MB_OK


def get_desktop():
    key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return QueryValueEx(key, "Desktop")[0]


MessageBox(0, "点击确定后在游戏目录：...(你的路径)\\Genshin Impact\\Genshin Impact Gam中选择YuanShen.exe文件，即可自动安装", "注意了注意了", MB_OK)
lpsFilter = "txt Files (YuanShen.exe)|YuanShen.exe|"
dlg = CreateFileDialog(True, "YuanShen.exe", None, 0x04 | 0x02, lpsFilter)  # 1表⽰打开⽂件对话框
dlg.SetOFNInitialDir(get_desktop())  # 设置打开⽂件对话框中的初始显⽰⽬录
dlg.DoModal()
filename = dlg.GetPathName()  # 获取选择的⽂件名称
filename = filename[:filename.rfind("\\")]

file = open(filename + "\\YuanSenEx.ini", 'w', encoding="UTF-8")
file.write("[url]\n[public]\n[GunFu]\n[BFu]")
file.close()
config = configparser.ConfigParser()
config.read(filename + "\\YuanSenEx.ini", encoding="UTF-8")
config.set("url", "url", filename)
config.set("public", "game_version", "3.1.0")
config.set("public", "plugin_sdk_version", "3.5.0")
config.set("GunFu", "channel", "1")
config.set("GunFu", "cps", "mihoyo")
config.set("GunFu", "sub_channel", "1")
config.set("BFu", "channel", "14")
config.set("BFu", "cps", "bilibili")
config.set("BFu", "sub_channel", "0")
config.write(open(filename + "\\YuanSenEx.ini", "w", encoding="UTF-8"))

copyfile("src\\PCGameSDK.dll", filename + "\\YuanShen_Data\\Plugins\\PCGameSDK.dll")
if not path.exists(filename + "\\src"):
    makedirs(filename + "\\src")
copyfile("src\\ico.ico", filename + "\\src\\ico.ico")
copyfile("src\\background.png", filename + "\\src\\background.png")
copyfile("src\\config.ini", filename + "\\config.ini")
copyfile("src\\Launcher.exe", filename + "\\Launcher.exe")
symlink(filename + "\\Launcher.exe", get_desktop() + "\\原神双服启动器")
MessageBox(0, "安装完成", "提示", MB_OK)
