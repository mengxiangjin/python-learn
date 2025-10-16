
/*
* hook掉普通的VPN检测
* */

Java.perform(function() {
    var NetworkInterface = Java.use('java.net.NetworkInterface')
    NetworkInterface.getName.implementation = function () {
        var name = this.getName();
        console.log("name: " + name);
        if(name == "tun0" || name == "ppp0"){
            return "rmnet_data0";
        }else {
           return name;
        }
    }
})