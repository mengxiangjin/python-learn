import frida
import sys

#attach 程序已经处于运行状态才能进行监听hook
#模拟器启动frida-server
#运行程序开始监听，模拟器应用操作模拟，触发监听
# 连接手机设备
rdev = frida.get_remote_device()
session = rdev.attach("唯品会")  # app名字

# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码

scr = """
Java.perform(function () {
    var info = Java.use('com.vip.vcsp.KeyInfo');
     var treeMap = Java.use('java.util.TreeMap')
    info.esNav.implementation = function(context,str,str2,str3,i){
        console.log("入参：",str);
        console.log("入参：",str2);
        console.log("入参：",str3);
        console.log("入参：",i);
        var res = this.esNav(context,str,str2,str3,i);
        console.log("返回值：",res);
        return res;
    }
});
"""


# -----下面固定---以后不会动
script = session.create_script(scr)

def on_message(message, data):
    print(message, data)

script.on("message", on_message)
script.load()
sys.stdin.read()


# 入参： app_name=shop_android&app_version=7.83.3&client_type=android&dinfo=%7B%22ah1%22%3A%22%22%2C%22ah2%22%3A%22%22%2C%22ah3%22%3A%22%22%2C%22ah4%22%3A%22wifi%22%2C%22ah5%22%3A%221440_2712%22%2C%22ah6%22%3A1900800%2C%22ah7%22%3A8%2C%22ah8%22%3A3839954944%2C%22ah9%22%3A%22Pixel+2+XL%22%2C%22ah10%22%3A%22%22%2C%22ah11%22%3A%22%22%2C%22ah12%22%3A%22%22%2C%22ah13%22%3A%22%22%2C%22as1%22%3A%2211%22%2C%22as2%22%3A%22%22%2C%22as3%22%3A%22%22%2C%22as4%22%3A%223a48d6bacc328464%22%2C%22as5%22%3A%22%22%2C%22as6%22%3A%22%22%2C%22as7%22%3A%2230%22%2C%22ac1%22%3A%221f3fb32d-9f6a-3cb8-86d2-4c8dc359650b%22%7D&mars_cid=1f3fb32d-9f6a-3cb8-86d2-4c8dc359650b&phone_model=Pixel+2+XL&session_id=1f3fb32d-9f6a-3cb8-86d2-4c8dc359650b_shop_android_1743475544538&sys_version=30&vcspKey=4d9e524ad536c03ff203787cf0dfcd29&vcspToken=NGQ5ZTUyNGFkNTM2YzAzZmYyMDM3ODdjZjBkZmNkMjl8fHwxNzQ2MDY3NTIzfHx8.f38c4d2ecc689f35ef3e893a35e2fcbb
# 入参： null
# 入参： null
# 入参： 0
# 返回值： MDExNWJiOGJkNGUwNjQ4Mn8GbKd/QGESAfsLRETPE49dVuzvgVSQ8Dn2pDIcSM7hfdtfJhr5apwKRmJrwf+4ycF84whpLsfeCOLovo8TC93p+tOYzbBR0j8uGlMepXxVXNGdjuARmVL26PML9AaKqSBuM6C1agLF3SedISIKp0ixIimkC2oap9/Dz1nfwZOSN5Xm4BQHs9TEaLL9zVe5qKWq+aK206afHhRd7eyrE1NV6iQ4FXukjF5ldf4+oA9qynuU3pPwC9GtJDjK4lGY4RNdlGb0Re+VScwAVkZjGBmylCLg5BZw1ZEkjNpHjqhe3IvnnaLtiPdmHOlXEshYj1jZN3Dvw2z5aEZ83khfnO3UA/NXa7wIUdqntjxaxUJT/ocatOhE3qF5NcHlfgs5bQIIJl+PQV6aJThuQcTAKLA9OGrvdQLXGd87kd+XrFUJq68YEz7fLHP2vrln2+lhl6N1ABVVX4C+1JwJ1ijb1Ic2h/FK+stwkQJtZmoJKsll7gumrCAqK6vZGXCUzupVzA2/p+fONOFsX55NQdmd4ARFeClRXnH2ZM2K0kMFoKSP0AMpID9zdVfJtbrj0hZMPqzdc0BsR9R7DM2oLlvqrrFCMt443gnvyrwQVjlO3JOfuIc6iBf9Ih56QCxi0Tm3OGKZbYlC6jvysIIHx7ahBgf/7AmUBrE1rP5tK6qZizSUnx6S+7k/uK9Uo3lnEBxL4AhItcKHwUH46PlVmX+n6N3jcB4mQIO3dLIghd1EzoZ4sBFWSrAvHvTNYUTjpqRkuyCVNGIjAyZRFhVaEiF9N6IjPKvsQyThSZbV0KQcKvUCnZUGClyeGADJgnxUITptOODte2m9qYBBexFMhFATA2gFHvJSSz0933ZsTZUBOKiGPP9hQWV7JjmWoogv6mj53aqdPeHJ/Ca1CROyWY2SN7aepTMiSrEpxgB+pnAbAedcd6AwWellk4egIvY0R0AWC70UFaA5mwymKOHWrEb6oFjOAUyvp+vzZLgpxlP+vvaVoJYpI+hDSdhwhJ9MmHgNx1hrYL+MYMU2vJDlW+7CXpyEu8yMvfyyuI+tB69l9RkItqajUf4pNNA0NKOBLj48n2q81jh9dIksaLz7n1ZlxGeHcMlGgTBi2BQl+kzQ5Xzhlhes8Luu6lCJLhsTeiOlOr0I2KY7pv/ULiFYTzKSnGMaM9x+aLFj0JfZuUKa7alZX4I8eBDLJx52Qa3B2fDY3g==


