


Java.perform(function() {
    let module = Process.getModuleByName("libxiaojianbang.so")

    let target_address = module.base.add(0x1B70)
    Memory.protect(module.base,module.size,'rwx')
    Interceptor.attach(target_address,{
        onEnter: function(args) {
            console.log('onEnter',this.context.x8)
            console.log('onEnter x1',this.context.x1)
            console.log(hexdump(this.context.x1))

        },
        onLeave: function (retval) {
            console.log('onLeave',this.context.x8)
            console.log('onLeave x1',this.context.x1)
        }
    })
})