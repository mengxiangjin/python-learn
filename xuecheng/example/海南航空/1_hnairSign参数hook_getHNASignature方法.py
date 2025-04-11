import frida
import sys

#spawn程序重启即开始监听hook
rdev = frida.get_remote_device()
# spawn写包名
pid = rdev.spawn(["com.rytong.hnair"])
session = rdev.attach(pid)

scr = """
Java.perform(function () {
    var hNASignature = Java.use('com.rytong.hnair.HNASignature');
    hNASignature.getHNASignature.implementation = function(str,str2,str3,str4,str5){
        console.log("参数：",str);
        console.log("参数：",str2);
        console.log("参数：",str3);
        console.log("参数：",str4);
        console.log("参数：",str5);
        var res = this.getHNASignature(str,str2,str3,str4,str5);
        console.log("返回值：",res);
        return res
    }
});
"""


script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
rdev.resume(pid)
sys.stdin.read()


# 参数： {}
# 参数： {}
# 参数： {"akey":"184C5F04D8BE43DCBD2EE3ABC928F616","aname":"com.rytong.hnair","atarget":"standard","aver":"9.0.0","did":"12a6a371aba0f791","dname":"Google_Pixel 2 XL","gtcid":"815f8252cd8c6ea58efa58988d7dae17","mchannel":"huawei","schannel":"AD","slang":"zh-CN","sname":"google\/taimen\/taimen:11\/RP1A.201005.004.A1\/6934943:user\/release-keys","stime":"1744274996209","sver":"11","system":"AD","szone":"+0800","abuild":"64249","riskToken":"67f78617Xv17x7AHF5xE3wgBNBjfQig8oeq5xn03","hver":"9.0.0.35417.7ac793f2e.standard","style":"roll","type":"8"}
# 参数： 21047C596EAD45209346AE29F0350491
# 参数： F6B15ABD66F91951036C955CB25B069F
# 返回值： 4B8078EF539CC94069F68D79017DAD558350FD54>>64249184C5F04D8BE43DCBD2EE3ABC928F616com.rytong.hnairstandard9.0.012a6a371aba0f791Google_Pixel 2 XL815f8252cd8c6ea58efa58988d7dae179.0.0.35417.7ac793f2e.standardhuawei67f78617Xv17x7AHF5xE3wgBNBjfQig8oeq5xn03ADzh-CNgoogle/taimen/taimen:11/RP1A.201005.004.A1/6934943:user/release-keys1744274996209roll11AD+08008>>F6B15ABD66F91951036C955CB25B069F
#
#
# 参数： {}
# 参数： {}
# 参数： {"akey":"184C5F04D8BE43DCBD2EE3ABC928F616","aname":"com.rytong.hnair","atarget":"standard","aver":"9.0.0","did":"12a6a371aba0f791","dname":"Google_Pixel 2 XL","gtcid":"815f8252cd8c6ea58efa58988d7dae17","mchannel":"huawei","schannel":"AD","slang":"zh-CN","sname":"google\/taimen\/taimen:11\/RP1A.201005.004.A1\/6934943:user\/release-keys","stime":"1744274997501","sver":"11","system":"AD","szone":"+0800","abuild":"64249","riskToken":"67f7861aLym0FQ6CxW0KUDaoV29TNTf92MVfsvn3","hver":"9.0.0.35417.7ac793f2e.standard","type":"8"}
# 参数： 21047C596EAD45209346AE29F0350491
# 参数： F6B15ABD66F91951036C955CB25B069F
# 返回值： 7913C1CF7C91F1F2704E45435E4ADE1DEC797E2D>>64249184C5F04D8BE43DCBD2EE3ABC928F616com.rytong.hnairstandard9.0.012a6a371aba0f791Google_Pixel 2 XL815f8252cd8c6ea58efa58988d7dae179.0.0.35417.7ac793f2e.standardhuawei67f7861aLym0FQ6CxW0KUDaoV29TNTf92MVfsvn3ADzh-CNgoogle/taimen/taimen:11/RP1A.201005.004.A1/6934943:user/release-keys174427499750111AD+08008>>F6B15ABD66F91951036C955CB25B069F