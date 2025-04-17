import subprocess

cmd = 'java -jar unidbg-android.jar test.txt'
result = subprocess.check_output(cmd, shell=True,cwd='unidbg_android_jar')
result = result.strip().decode('utf-8')
print(result)