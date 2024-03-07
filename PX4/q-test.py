from subprocess import Popen
import time
import psutil
qgc_handle = Popen(["/home/pgfuzz/Downloads/QGroundControl.AppImage"])



time.sleep(10)
qgc_handle.terminate()

PROCNAMES = ["QGroundControl", "QGroundControl.AppImage"]

for proc in psutil.process_iter():
    # check whether the process name matches
    print(proc.name())
    
    for PROCNAME in PROCNAMES:
        if PROCNAME in proc.name():
            proc.kill()
