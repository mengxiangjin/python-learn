import subprocess

subprocess.run('adb forward tcp:27042 tcp:27042')
subprocess.run('adb forward tcp:27043 tcp:27043')