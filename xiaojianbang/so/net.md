## Hook与抓包

### 浏览器访问服务器的密钥交换过程（Https）

- 非对称加密+对称加密的结合
- 服务器有自己的公钥（S.pub）、私钥（S.pri），将自己的公钥交给CA机构进行认证
- CA机构有自己的公钥（CA.pub）、私钥（CA.pri），CA机构用自己的CA.pri对S.pub等进行加密，生成CA证书，将CA证书交给服务端
  - CA机构首先对S.pub+服务器域名+证书有效期等内容进行哈希计算（如SHA256）
  - 用CA.pri对哈希计算的结果进行加密生成**数字签名**
  - **CA证书=数字签名+S.pub+服务器域名+证书有效期**
- 浏览器内置了CA机构的公钥（CA.pub）
- 当浏览器向服务器发送Connect（TCP三次握手）
- 服务器将CA证书发送给浏览器，浏览器通过CA.pub对CA证书进行解密去校验证书的合法性
  - 浏览器先用CA.pub对CA证书的数字签名进行解密，得到H1
  - 浏览器再通过对CA证书的S.pub+服务器域名+证书有效期进行哈希计算，得到H2
  - 比较H1与H2的结果判断合法性
- 若不合法关闭连接，合法则生成随机的对称密钥
- 浏览器将生成的对称密钥通过CA证书解密后得到的S.pub加密后交给服务器
- 这时，双方即可用该对称密钥进行安全通信

### 代理检测

#### HttpsURLConnection

```java
//直连不走代理
HttpsURLConnection conn = (HttpsURLConnection) u.openConnection(Proxy.NO_PROXY);
```

#### OkHttp

```java
OkHttpClient.Builder clientBuilder = new OkHttpClient.Builder().proxy(Proxy.NO_PROXY)
```

#### System.getProperty()

```java
String host = System.getProperty("https.proxyHost");
String port = System.getProperty("https.proxyPort");
```

#### VPN检测

- next.getName().equals（"tun0"） 即检测到了相关VPN服务
- next.isUp()  是否已经运行

```java
@RequiresApi(api = Build.VERSION_CODES.KITKAT)
public static void getNetworkName() {
    try {
        Enumeration<NetworkInterface> networkInterfaces = NetworkInterface.getNetworkInterfaces();
        int count = 0;
        while (networkInterfaces.hasMoreElements()) {
            NetworkInterface next = networkInterfaces.nextElement();
            logOutPut("getName获得网络设备名称=" + next.getName());
            logOutPut("getDisplayName获得网络设备显示名称=" + next.getDisplayName());
            logOutPut("getIndex获得网络接口的索引=" + next.getIndex());
            logOutPut("isUp是否已经开启并运行=" + next.isUp());
            logOutPut("isBoopback是否为回调接口=" + next.isLoopback());
            logOutPut("**********************" + count++);
        }
    } catch (SocketException e) {
        e.printStackTrace();
    }
}
```
