pyinstaller -F -w Launcher.py -i .\ico.ico --uac-admin
del .\*.spec
copy .\dist\* .\
rd /s /q .\dist
rd /s /q .\build
rd /s /q .\__pycache__