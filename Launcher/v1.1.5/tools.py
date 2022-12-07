from json import dumps, loads
from winreg import (HKEY_CURRENT_USER, CloseKey, EnumKey, EnumValue, OpenKeyEx,
                    QueryValueEx)

from win10toast import ToastNotifier
from win32api import ShellExecute
from win32ui import CreateFileDialog
from threading import Thread

class GetPath:

    def GetDesktop():
        """获取桌面

        Returns:
            str: 桌面位置
        """

        key = OpenKeyEx(HKEY_CURRENT_USER,
                        r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return QueryValueEx(key, "Desktop")[0]

    def GetYuanShen():
        """从注册表中获取 YuanShen.exe 的文件所在位置

        Returns:
            str: 返回文件位置，未找到返回 "Not Found"
        """

        key = OpenKeyEx(HKEY_CURRENT_USER,
                        r'Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store')
        index = 0
        while True:
            try:
                # 获取注册表对应位置的键和值
                Path = EnumValue(key, index)[0]
                index += 1
                if Path.split("\\")[-1] == "YuanShen.exe":
                    return Path
            except OSError as error:
                # 一定要关闭这个键
                CloseKey(key)
                return "Not Find"
                break


class FileOperation:

    def SelectFile(file:str, description:str):
        """选择文件

        Args:
            file (str): 文件名
            description (str): 文件描述

        Returns:
            str: 选择文件位置
        """
        ###
        dlg = CreateFileDialog(True, file, None,
                               0x04 | 0x02, description)  # 1表⽰打开⽂件对话框
        dlg.SetOFNInitialDir(GetPath.GetDesktop())  # 设置打开⽂件对话框中的初始显⽰⽬录
        dlg.DoModal()
        Path = dlg.GetPathName()  # 获取选择的⽂件名称
        Path = Path[:Path.rfind("\\")]
        return Path

    def FileToJson(filepath:str):
        """从文件中读取 Json 格式并转为 字典

        Args:
            filepath (str): 文件位置

        Returns:
            dirt: 字典
        """
        with open(filepath, encoding="utf8") as f:
            return loads(f.read())

    def JsonToFile(filepath:str ,content:str):
        """从文件中读取 Json 格式并转为 字典

        Args:
            filepath (str): 文件位置
            content (str): 内容

        Returns:
            None: 无
        """
        with open(filepath,mode="w+" ,encoding="utf8") as f:
            f.write(dumps(content ,indent=4))


class Toast(Thread):
    def __init__(self ,title ,description):
        Thread.__init__(self)
        self.title = title
        self.description = description
    def run(self):
        """输出一个 Windows 通知，但会阻塞进程，使用时请务必使用多线程

        Args:
            title (str): 标题
            description (str): 内容
        """        
        toaster = ToastNotifier()
        toaster.show_toast(self.title, self.description, duration=10)
