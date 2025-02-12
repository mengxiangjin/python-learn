import frida

# 获取设备信息
rdev = frida.get_remote_device()

# 枚举所有的进程
# processes = rdev.enumerate_processes()
# for process in processes:
#     print(process)

# 获取在前台运行的APP
front_app = rdev.get_frontmost_application()
print(front_app)  # Application(identifier="com.che168.autotradercloud", name="车智赢+", pid=19947, parameters={})  后面咱们会看包名和app名