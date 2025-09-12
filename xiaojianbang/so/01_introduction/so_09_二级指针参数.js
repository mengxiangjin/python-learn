

/*
* 传递二级指针参数
*
* __int64 __fastcall xiugaiStr(char **a1)
{
  return __strcat_chk(*a1, " QQ24358757", -1LL);
}
* */
function call_pointer_pointer() {
    var soAddr = Module.findBaseAddress("libxiaojianbang.so");
    let func = new NativeFunction(soAddr.add(0x17D0),'int',['pointer'])

    let str_addr = Memory.allocUtf8String("newdata")
    let final_adr = Memory.alloc(8).writePointer(str_addr)

    console.log(hexdump(str_addr))
    func(final_adr)
    console.log(hexdump(str_addr))

}


Java.perform(function() {

})