


function enc(phone_number,password) {
    var time = new Date().getTime();
    let str = 'equtype=ANDROID&loginImei=Androidnull&timeStamp=' + time +  '&userPwd=' + password + '&username=' + phone_number  + '&key=sdlkjsdljf0j2fsjk'
    var utils = Java.use('com.dodonew.online.util.Utils')
    let sign = utils.md5(str).toUpperCase()
    console.log('sing ----> ',sign)

    var encryptData = '{"equtype":"ANDROID","loginImei":"Android352689082129358","sign":"'+
            sign +'","timeStamp":"'+ time +'","userPwd":"' + passward + '","username":"' + username + '"}';
    var RequestUtil = Java.use('com.dodonew.online.http.RequestUtil')
    var encrypt = RequestUtil.encodeDesMap(encryptData,'65102933','32028092')
    console.log('encrypt ----> ',encrypt)
    return encrypt
}