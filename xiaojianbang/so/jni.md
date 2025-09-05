- ## NDK开发


### 第一个NDK工程

- build.gradle中android下引入

  - ```groovy
    externalNativeBuild {
        cmake {
            path file('src/main/cpp/CMakeLists.txt')
            version '3.31.5'
        }
    }
    ```

- **构建CMakeLists.txt文件**

  - add_library（name type source_file）:

    - name:生成的so文件名称（这里的mainlib即需要后面在类中进行静态引入的），libmainlib.so
    - type：
      - STATIC：静态库，代码生成.a文件，可链接到其他代码中
      - SHARE：共享库，生成.so文件，通常用作动态链接库，可在运行时被多个程序共享
      - MODULE：模块库，但这个库不会被链接到最终的可执行文件或其他库
    - source_file：构建库的源文件

  - ```
    add_library(mainlib SHARED native-lib.cpp)
    ```

- Java调用类中静态声明so文件、声明native方法

  - ```java
    static {
        System.loadLibrary("mainlib");
    }
    
    public native String stringFromJNI();
    ```

- add_library中明确的源文件，构造源文件，即native方法的具体实现native-lib.cpp

  - ```cpp
    #include <jni.h>
    #include <string> 
    
    extern "C" JNIEXPORT jstring JNICALL
    Java_com_jin_jni_MainActivity_stringFromJNI(
            JNIEnv* env,
            jobject /* this */) {
        std::string hello = "Hello from C++";
        return env->NewStringUTF(hello.c_str());
    }
    ```

    - **#include <jni.h>：C和C++与Java程序交互的接口，定义了交互的函数变量等**
    - **#include <string> ：C++字符串的头文件（ std::string）**
    - **extern "C" JNIEXPORT jstring JNICALL**
      - **extern "C"：使用C语言链接方式，避免C++（可能对于函数会有名称修饰）**
      - **JNIEXPORT ：标记JNI可调用函数**
      - **jstring：JNI中的返回值类型，返回字符串类型**
      - **JNICALL：JNI调用约定**
    - **Java_com_jin_jni_MainActivity_stringFromJNI：方法名固定格式**
    - **JNIEnv* env：指向JNI环境的指针，用于与Java之间进行交互（env->NewStringUTF(hello.c_str())构造Java字符串等）**
    - **jobject：调用该native方法的this对象，对于静态函数，即为jclass**
    - **std::string：C++中的字符串类型**
    - **hello.c_str()：C++中字符串类型转变为C中的char数组**

### Native方法实现中函数

#### 日志输出

- ​	需要导入头文件 **#include <android/log.h>**

- ```c
  __android_log_print(int prio, const char* tag, const char* fmt, ...)
  ```

  - prio：日志输出级别（ANDROID_LOG_DEBUG、ANDROID_LOG_WARN等）

  - tag：char数组即字符串，输出的TAG

  - fmt：输出日志内容

  - ...：可变长参数（输出日志内容含有格式说明符%d等，后面所代表的参数）

  - ```c
    __android_log_print(ANDROID_LOG_DEBUG,"TAG","xxxxx jni fmt %d %d",100,200);
    ```

#### 多线程

- 需要导入头文件 **#include <pthread.h>**

- ```c
  int pthread_create(pthread_t* __pthread_ptr, pthread_attr_t const* __attr, void* (*__start_routine)(void*), void*);
  ```

  - __pthread_ptr：long类型的指针，即线程ID

  - pthread_attr_t：线程属性信息，可传nullptr

  - void*：线程的具体执行函数

  - void*：线程的执行函数所需要的参数，没有则传nullptr

  - 创建并执行线程（主线程调用pthread_join传入子线程ID，等待其执行完毕）

  - ```c
    void thread_fun() {
        __android_log_print(ANDROID_LOG_DEBUG,TAG,"xxxxx jni fmt %d %d",100,200);
    }
    
    long pthread;
    pthread_create(&pthread, nullptr, reinterpret_cast<void *(*)(void *)>(thread_fun), nullptr);
    pthread_join(pthread, nullptr);
    ```

#### JNI_OnLoad

- 当加载so文件时，会默认主动调用相关方法**init、init_array、JNI_OnLoad**（可不用声明），即当System.loadLibrary时，首先会依次触发此三个方法

- 一般用于检查JNI环境正确与否，返回Java的版本号，返回值错误会导致闪退

- ```c
  JNIEXPORT jint JNI_OnLoad(JavaVM *vm, void *reserved) {
      JNIEnv *env = nullptr;
      if (vm->GetEnv((void **) &env, JNI_VERSION_1_6) != JNI_OK) {
          LOGD("GetEnv failed");
          return -1;
      }
      return JNI_VERSION_1_6;
  }
  ```

- **JavaVM：JVM表示主要用来获取JNIEnv。跨线程即一个进程独一份**

- **JNIEnv：提供与JVM交互的各种接口，每个线程单独一份**

- JavaVM的获取方式

  - JNI_OnLoad中的第一个参数

  - JNI_OnUnLoad中的第一个参数

  - 通过JNIEnv获得env->GetJavaVM(**p);

    - 跨线程的，地址值是相同的

    - ```c
      JNIEXPORT jint JNI_OnLoad(JavaVM *vm, void *reserved) {
          JNIEnv *env = nullptr;
          if (vm->GetEnv((void **) &env, JNI_VERSION_1_6) != JNI_OK) {
              LOGD("GetEnv failed");
              return -1;
          }
          LOGD("原始地址 %p",vm);
          JavaVM *newVm = nullptr;
          env->GetJavaVM(&newVm);
          LOGD("当前地址 %p",newVm);
          return JNI_VERSION_1_6;
      }
      ```

- JNIEnv的获取：

  - 通过JavaVM获取

  - 主线程调用（GetEnv）、子线程调用（AttachCurrentThread）

    - ```c
      JNIEnv *env = nullptr;
      vm->GetEnv(reinterpret_cast<void **>(&env), JNI_VERSION_1_6)
      ```

    - ```c
      long pthread;
      pthread_create(&pthread, nullptr, reinterpret_cast<void *(*)(void *)>(thread_func), vm);
      
      void thread_func(JavaVM *vm) {
          JNIEnv* env = nullptr;
          vm->AttachCurrentThread(&env, nullptr);
          LOGD("thread_func %p",env);
      }
      ```


### JNI函数的注册

#### 静态注册

- 遵循命名规范Java_包名__类名_方法名（可以在IDA导出表中直接看到）

#### 动态注册

- **env即JNIEnv* env对象**

- **通过env->RegisterNatives进行注册（一般在JNI_OnLoad函数中注册，load时JNI_OnLoad就已被调用）**

- env->RegisterNatives()方法

  - jint：返回值，注册成功与否

  - jclass：注册的全路径类名（com/jin/jni/MainActivity）

    - 一般通过 env->FindClass进行获取

    - ```c
      jclass clazz = env->FindClass("com/jin/jni/MainActivity");
      ```

  - JNINativeMethod*：需要映射的方法数组，数组中存放着JNINativeMethod对象

    - JNINativeMethod对象中的属性相关：

      - char *name：Java Native方法中的原名称
      - char *signature：方法对应的签名信息，参数与返回值
        - (Ljava/lang/String;)Ljava/lang/String;  （String）String
      - void*  fnPtr：对应真正的函数地址（Native实现函数）

    - ```c
      JNINativeMethod methods[] = {
              {"stringFromJNIWithDynamic1", "(Ljava/lang/String;)Ljava/lang/String;",
              (void *)(realFunc1)},
              {
                  "stringFromJNIWithDynamic2","(Ljava/lang/String;I)I",(void *)(realFunc2)
              }
      };
      
      jstring realFunc1(JNIEnv* env,jobject object,jstring a) {
          const char* s = env->GetStringUTFChars(a,JNI_FALSE);
          LOGD("realFunc1 ----> %s",s);
          std::string res = "realFunc1 ---> result";
          return env->NewStringUTF(res.c_str());
      }
      
      jint realFunc2(JNIEnv* env,jobject object,jstring a,jint b) {
          const char* s = env->GetStringUTFChars(a,JNI_FALSE);
          LOGD("realFunc2 ----> %s",s);
          LOGD("realFunc2 ----> %d",b);
          std::string res = "realFunc2 ---> result";
          return 20;
      }
      ```

  - jint：动态注册的方法的个数

  - ```c
    jint (*RegisterNatives)(JNIEnv*, jclass, const JNINativeMethod*,
                        jint);
    ```

##### 动态注册案例

- Native方法

  - ```java
        static {
            System.loadLibrary("mainlib");
            System.loadLibrary("dynamiclib");
        }
    
    public native String stringFromJNIWithDynamic1(String data);
    
    public native int stringFromJNIWithDynamic2(String data,int digit);
    ```

- CPP实现

  - ```c
    #include <jni.h>
    #include <string>
    #include <android/log.h>
    #include <pthread.h>
    
    
    #define TAG "xiaojianbang"
    #define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG,TAG,__VA_ARGS__)
    #define LOGE(...) __android_log_print(ANDROID_LOG_ERROR,TAG,__VA_ARGS__)
    
    
    jstring realFunc1(JNIEnv* env,jobject object,jstring a) {
        const char* s = env->GetStringUTFChars(a,JNI_FALSE);
        LOGD("realFunc1 ----> %s",s);
        std::string res = "realFunc1 ---> result";
        return env->NewStringUTF(res.c_str());
    }
    
    jint realFunc2(JNIEnv* env,jobject object,jstring a,jint b) {
        const char* s = env->GetStringUTFChars(a,JNI_FALSE);
        LOGD("realFunc2 ----> %s",s);
        LOGD("realFunc2 ----> %d",b);
        std::string res = "realFunc2 ---> result";
        return 20;
    }
    
    JNIEXPORT jint JNI_OnLoad(JavaVM *vm, void *reserved) {
        JNIEnv *env = nullptr;
        if (vm->GetEnv(reinterpret_cast<void **>(&env), JNI_VERSION_1_6) != JNI_OK) {
            LOGD("GetEnv failed");
            return -1;
        }
        jclass clazz = env->FindClass("com/jin/jni/MainActivity");
        JNINativeMethod methods[] = {
                {"stringFromJNIWithDynamic1", "(Ljava/lang/String;)Ljava/lang/String;",
                (void *)(realFunc1)},
                {
                    "stringFromJNIWithDynamic2","(Ljava/lang/String;I)I",(void *)(realFunc2)
                }
        };
        env->RegisterNatives(clazz,methods,2);
        return JNI_VERSION_1_6;
    }
    ```

### so文件的存放位置

- /data/app/随机字符串/包名/lib/架构下/.so文件

- 获取so文件存放路径

  - ```java
    public String getSoLibraryPath(Context context) {
        PackageManager packageManager = context.getPackageManager();
        List<PackageInfo> installedPackages = packageManager.getInstalledPackages(0);
        for (int i = 0; i < installedPackages.size(); i++) {
            PackageInfo packageInfo = installedPackages.get(i);
            if (packageInfo.applicationInfo.nativeLibraryDir.startsWith("/data/app")) {
                if (packageInfo.packageName.contains("com.jin")) {
                    Log.d("TAG", "getSoLibraryPath: " + packageInfo.packageName + "---->" + packageInfo.applicationInfo.nativeLibraryDir);
                    return packageInfo.applicationInfo.nativeLibraryDir;
                }
            }
        }
        return "";
    }
    ```

### so之间的相互调用

#### 同个so下的cpp的调用

- CMakeList文件中声明

  - mainlib与native-lib.cpp native-libB.cpp进行关联（mainlib）会被编译成libmainlib.so文件，里面有cpp的相关代码

  - ```groovy
    add_library(mainlib SHARED
            # List C/C++ source files with relative paths to this CMakeLists.txt.
            native-lib.cpp native-libB.cpp)
    ```

- native-lib.cpp中想要调用native-libB.cpp中的方法

  - native-libB.cpp中方法

    - ```c
       void native_libB_test() {
          LOGD("native_libB_test");
      }
      ```

  - native-lib.cpp中声明想要调用的方法后、想要调用时直接调用即可native_libB_test();

    - ```c
      void native_libB_test();
      ```

#### 跨so下的cpp的调用

##### target_link_libraries声明

- CMakeList文件中声明

  - mainlib中的native-libB.cpp想要调用dynamiclib中的dynamic-lib.cpp函数

  - target_link_libraries：将dynamiclib链接到mainlib即可

  - ```c
    add_library(mainlib SHARED
            # List C/C++ source files with relative paths to this CMakeLists.txt.
            native-lib.cpp native-libB.cpp)
    add_library(dynamiclib SHARED dynamic-lib.cpp)
        
    find_library(log-lib log)
    target_link_libraries(mainlib ${log-lib} dynamiclib)    
    ```

  - dynamic-lib.cpp中被调用的方法

    - ```c
      void test_dynamic() {
          LOGD("dynamic-lib test_dynamic");
      }
      ```

  - native-libB.cpp声明想要调用的方法后直接调用即可

    - ```c
      void test_dynamic();
      ```

##### dlopen与dlsym函数（运行时加载so库后调用函数）

###### dlopen

- 程序运行时动态加载so库

  - **__filename：so库的绝对路径**
    - **可以通过上面so文件存放的位置+打开so库的名称（动态加载mainlib，即libmainlib.so文件）**
    - **/data/app/~~QhEuueLAUoOiDLJvicP5CQ==/com.jin.jni-0Gzxzl5XLhic2IlPCp-RIA==/lib/arm64/libmainlib.so**
  - __flag：so库如何打开（一般为RTLD_NOW）
    - RTLD_NOW、RTLD_NOLOAD、RTLD_LAZY等
  - 返回指向so库的指针（后续其可以调用so库的函数方法）

- ```c
  void* dlopen(const char* __filename, int __flag);
  //示例
  void* open = dlopen(fileName,RTLD_NOW);
  ```

###### dlsym

- 配合dlopen使用，查找so库的函数、变量等

  - __handle：指向具体so的指针，即dlopen函数后的返回值
  - __symbol：具体的函数名称或者变量名称
    - 注意：C++可能对函数名称、变量名称作了修饰符处理，此为处理过后的函数名称（可在ida中查看真实名称）
    
    - 舍弃C++函数、变量名称修复符处理，保留C的风格（原名称），使用 extern "C" （此__symbol即”native_libB_testA“）
    
      - ```c
        extern "C" void native_libB_testA() {
            LOGD("native_libB_testA");
        }
        ```
    
  - 返回指向函数的指针或者指向变量指针（需要强制转换到对应函数或对应变量）

- ```c
  void* dlsym(void* __handle, const char* __symbol);
  
  //示例 调用返回值void、参数空的def方法 实际即native_libB_testA方法
  void* open = dlopen(fileName,RTLD_NOW);
  void (*def)() = nullptr;
  def = reinterpret_cast<void (*)()>(dlsym(open, "native_libB_testA"));
  def();
  
  //示例 调用返回值是jstring、参数是JNIEnv*, char*的native_libB_testB_ptr方法 实际即native_libB_testB方法
  jstring (*native_libB_testB_ptr)(JNIEnv*, char*) =
  reinterpret_cast<jstring (*)(JNIEnv*, char*)>(dlsym(open, "native_libB_testB"));
  jstring result = native_libB_testB_ptr(env,"avaa");
  
  //另一个so库映射的cpp文件
  extern "C" void native_libB_testA() {
      LOGD("native_libB_testA");
  }
  
  extern "C" jstring native_libB_testB(JNIEnv  *env,char* data) {
      LOGD("native_libB_testB data is %s",data);
      return env->NewStringUTF("native_libB_testB_result");
  }
  ```

##### 跨so调用

- **需求：libdynamiclib.so库下的dynamic-lib.cpp中调用libmainlib.so库的native-libB.cpp中的函数方法**

- ```c
  add_library(mainlib SHARED
          # List C/C++ source files with relative paths to this CMakeLists.txt.
          native-lib.cpp native-libB.cpp)
  add_library(dynamiclib SHARED dynamic-lib.cpp)
  ```

- native-libB.cpp 属于libmainlib.so库下

  - ```c
    extern "C" void native_libB_testA() {
        LOGD("native_libB_testA");
    }
    
    extern "C" jstring native_libB_testB(JNIEnv  *env,char* data) {
        LOGD("native_libB_testB data is %s",data);
        return env->NewStringUTF("native_libB_testB_result");
    }
    ```

- dynamic-lib.cpp 属于libdynamiclib.so库下

  - Java方法中调用callPathSoFunc传入libmainlib.so的路径

  - ```java
    callPathSoFunc(getSoLibraryPath(this) + "/libmainlib.so");
    //获取so路径
    public String getSoLibraryPath(Context context) {
            PackageManager packageManager = context.getPackageManager();
            List<PackageInfo> installedPackages = packageManager.getInstalledPackages(0);
            for (int i = 0; i < installedPackages.size(); i++) {
                PackageInfo packageInfo = installedPackages.get(i);
                if (packageInfo.applicationInfo.nativeLibraryDir.startsWith("/data/app")) {
                    if (packageInfo.packageName.contains("com.jin")) {
                        Log.d("TAG", "getSoLibraryPath: " + packageInfo.packageName + "---->" + packageInfo.applicationInfo.nativeLibraryDir);
                        return packageInfo.applicationInfo.nativeLibraryDir;
                    }
                }
            }
            return "";
        }
    ```

  - ```c
    extern "C" JNIEXPORT jstring JNICALL
    Java_com_jin_jni_MainActivity_callPathSoFunc(JNIEnv* env,jobject obj,jstring path) {
        std::string res = "callPathSoFunc ---> result";
        //路径转为C语言可识别的char*
        char* fileName = const_cast<char *>(env->GetStringUTFChars(path, nullptr));
        LOGD("callPathSoFunc %s",fileName);
    	//打开该so库，获取其库指针
        void* open = dlopen(fileName,RTLD_NOW);
        
        //在该so库中查找native_libB_testA函数，该函数返回void 参数为空()
        void (*def)() = nullptr;
        def = reinterpret_cast<void (*)()>(dlsym(open, "native_libB_testA"));
        if (def == nullptr) {
            LOGE("未找到native_libB_testA方法");
        } else{
            //调用找到的指针函数
            def();
        }
    
        // 在该so库中查找native_libB_testB函数，该函数返回jstring 参数为(JNIEnv*, char*)
        jstring (*native_libB_testB_ptr)(JNIEnv*, char*) =
        reinterpret_cast<jstring (*)(JNIEnv*, char*)>(dlsym(open, "native_libB_testB"));
        
        //调用找到的指针函数，传入参数以及获取返回值
        jstring result = native_libB_testB_ptr(env,"avaa");
        LOGD("获取到结果是%s",env->GetStringUTFChars(result, nullptr));
        return env->NewStringUTF(res.c_str());
    }
    ```

### JNI与Java的交互

#### 创建Java对象

- **env->NewObject（jclass，jmethodID）**

- 找类、获取类中的方法、构造对象

- ```java
  //创建对象
  jclass ndkClass = env->FindClass("com/jin/jni/bean/NDKDemo");
  
  jmethodID jmethodId1 = env->GetMethodID(ndkClass,"<init>", "()V");
  jobject jobject1 = env->NewObject(ndkClass,jmethodId1);
  
  jmethodID jmethodId2 = env->GetMethodID(ndkClass,"<init>", "(Ljava/lang/String;I)V");
  jobject jobject2 = env->NewObject(ndkClass,jmethodId2,env->NewStringUTF("参数1"),10);
  LOGD("无参对象：jobject1 %p",jobject1);
  LOGD("有参对象：jobject2 %p",jobject2);
  ```

#### 获取静态属性

- **getStaticField（env，jclass，char* name，char* sign）**

- ```java
  jclass ndkClass = env->FindClass("com/jin/jni/bean/NDKDemo");
  //获取静态字段(String)
  jstring strField1 =(jstring) getStaticField(env,ndkClass,"publicStaticStringField","Ljava/lang/String;");
  const char* field1 = env->GetStringUTFChars(strField1, nullptr);
  LOGD("静态字段：field %s",field1);
  ```

获取对象属性

- **getField（env，jclass，char* name，char* sign，jobject）**

- ```java
  jclass ndkClass = env->FindClass("com/jin/jni/bean/NDKDemo");
  jmethodID jmethodId1 = env->GetMethodID(ndkClass,"<init>", "()V");
  jobject jobject1 = env->NewObject(ndkClass,jmethodId1);
  
  //获取对象字段(String)
  jstring strField2 =(jstring) getField(env,ndkClass,"privateStringField","Ljava/lang/String;",jobject1);
  const char* field2 = env->GetStringUTFChars(strField2, nullptr);
  LOGD("对象字段：field %s",field2);
  ```

#### 设置对象属性（String为例）

- **env->SetObjectField（jobject instance，jfieldID，jobject value）**

- ```java
  //设置对象字段(String)
  jstring value = env->NewStringUTF("这是新设置的字段");
  //获取字段ID
  jfieldID jfieldId1 = env->GetFieldID(ndkClass,"privateStringField", "Ljava/lang/String;");
  
  //设置对象字段为具体的值
  env->SetObjectField(jobject1,jfieldId1,value);
  
  jstring strField3 =(jstring) getField(env,ndkClass,"privateStringField","Ljava/lang/String;",jobject1);
  const char* field3 = env->GetStringUTFChars(strField3, nullptr);
  LOGD("对象字段设置后：field %s",field3);
  ```

- 设置字节数组

  - ```java
    //获取对象字节数组
    jbyteArray byte_array =(jbyteArray) getField(env,ndkClass,"byteArray","[B",jobject1);
    //打印字节数组
    jsize length = env->GetArrayLength(byte_array);
    jbyte* bytes = env->GetByteArrayElements(byte_array, nullptr);
    for (jsize i=0;i<length;i++) {
        LOGD("bytes值：%d",bytes[i]);
    };
    
    //设置对象字节数组值
    for (jsize i=0;i<length;i++) {
        bytes[i] = (char)(100-i);
    }
    
    env->ReleaseByteArrayElements(byte_array,bytes,0);
    
    for (jsize i=0;i<length;i++) {
        LOGD("bytes值：%d",bytes[i]);
    };
    ```

#### 调用静态方法

- **env->CallStaticVoidMethod（jclass，jmethodID）**

- ```java
  //调用静态方法，空参数、空返回值
  jclass ndkClass = env->FindClass("com/jin/jni/bean/NDKDemo");
  
  jmethodID jmethodID = env->GetStaticMethodID(ndkClass,"publicStaticFunc","()V");
  env->CallStaticVoidMethod(ndkClass,jmethodID);
  ```

#### 调用对象方法

- **env->CallObjectMethod（jobject instance，jmethodID，可变长参数）**

- ```java
  //调用对象方法  参数（String,int） 返回值String
  jstring res1 = static_cast<jstring>(env->CallObjectMethod(jobject1, env->GetMethodID(ndkClass,
                                                                                      "privateFunc",
                                                                                      "(Ljava/lang/String;I)Ljava/lang/String;"),
                                                           env->NewStringUTF("abc"), 10));
  LOGD("CallObjectMethod ---> %s",env->GetStringUTFChars(res1, nullptr));
  ```

- **env->CallObjectMethodA（jobject instance，jmethodID，共同体jvalue*）**

- ```java
  //效果等同于传递了2个参数，"def"与20
  jvalue args[2];
  args[0].l = env->NewStringUTF("def");
  args[1].i = 20;
  jstring res2 = static_cast<jstring>(env->CallObjectMethodA(jobject1, env->GetMethodID(ndkClass,
                                                                                        "privateFunc",
                                                                                        "(Ljava/lang/String;I)Ljava/lang/String;"),
                                                             args));
  LOGD("CallObjectMethodA ---> %s",env->GetStringUTFChars(res2, nullptr));
  ```

- 调用对象的此方法

  - 参数是String[]，返回值是int[]

  - ```java
    private static int[] privateStaticFunc(String[] str){
        StringBuilder retval = new StringBuilder();
        for(String i : str) {
            retval.append(i);
        }
        Log.d("xiaojianbang", "this is privateStaticFunc: " + retval.toString());
        return new int[]{0,1,2,3,4,5,6,7,8,9};
    }
    ```

  - **String[]在JNI中相当于jobjectArray，里面存放着jstring（新建参数）newObjectArray**

  - ```java
    //参数是数组，返回值是数组
    jobjectArray newObjectArray = env->NewObjectArray(3,env->FindClass("java/lang/String"), nullptr);
    for (int i = 0; i < env->GetArrayLength(newObjectArray); ++i) {
        //jstring item = env->NewStringUTF("ghi" + i);
        //拼接字符串
        jstring item = env->NewStringUTF(("ghi" + std::to_string(i)).c_str());
        env->SetObjectArrayElement(newObjectArray,i,item);
    }
    ```

  - **返回值是int[]在JNI中相当于jintArray，调用方法后强制转换即可**

  - ```java
    //参数是数组，返回值是数组
    jobjectArray newObjectArray = env->NewObjectArray(3,env->FindClass("java/lang/String"), nullptr);
    for (int i = 0; i < env->GetArrayLength(newObjectArray); ++i) {
        //jstring item = env->NewStringUTF("ghi" + i);
        //拼接字符串
        jstring item = env->NewStringUTF(("ghi" + std::to_string(i)).c_str());
        env->SetObjectArrayElement(newObjectArray,i,item);
    }
    
    //调用对象方法，传递newObjectArray参数
    jintArray intArray = static_cast<jintArray>(env->CallStaticObjectMethod(ndkClass,                                               env->GetStaticMethodID(                               		ndkClass,                                                "privateStaticFunc",                                    "([Ljava/lang/String;)								[I"),                                        	newObjectArray));
    //获取元素打印
    jint *p = env->GetIntArrayElements(intArray, nullptr);
    for (int i = 0; i < env->GetArrayLength(intArray); ++i) {
        LOGD("返回值 ---》%d",p[i]);
    }
    ```

#### 调用父类方法

- **Activity中的onResume方法重写必须调用父类的super.onResume()，否则闪退**

  ```java
  @SuppressLint("MissingSuperCall")
  protected native void onResume();
  ```

  ```java
  extern "C" JNIEXPORT void JNICALL
  Java_com_jin_jni_MainActivity_onResume(JNIEnv* env,jobject jobject1) {
      jclass cls = env->FindClass("androidx/fragment/app/FragmentActivity");
      jmethodID methodID = env->GetMethodID(cls,"onResume", "()V");
      //等价于this.super.onResume()
      env->CallNonvirtualVoidMethod(jobject1,cls,methodID);
  }
  ```

#### 全局、局部变量

- 局部变量：大多数jni函数调用之后返回的都为局部变量

- 全局变量：同大多数语法不同，将变量声明写在全局作用域不可行

  - jobject env->NewGlobalRef（jobject）

  - jweek env->NewWeakGlobalRef（jobject）：弱引用

  - ```java
    jobject ndkClass;
    JNIEXPORT jint JNI_OnLoad(JavaVM *vm, void *unused) {
        JNIEnv *env = nullptr;
        if (vm->GetEnv(reinterpret_cast<void **>(&env), JNI_VERSION_1_6) != JNI_OK) {
            LOGD("GetEnv failed");
            return -1;
        }
        jclass localRef = env->FindClass("com/jin/jni/bean/NDKDemo");
        //赋值全局变量
        ndkClass = env->NewGlobalRef(localRef);
        return JNI_VERSION_1_6;
    }
    ```

- 变量用完需释放内存空间

  - ```java
    //释放全局变量
    env->DeleteGlobalRef(ndkClass);
    //局部变量
    env->DeleteLocalRef(bClass);
    ```

#### 子线程创建类

##### 获取系统类（Java包非Android包）

- 子线程中通过拿到唯一的JavaVM* vm对象，获取JNIEnv* env对象，将获取到的env对象vm->AttachCurrentThread(&env, nullptr)附加到当前线程即可

- ```java
  void create_class(JavaVM* vm) {
      JNIEnv *env = nullptr;
      if (vm->GetEnv(reinterpret_cast<void **>(&env), JNI_VERSION_1_6) != JNI_OK) {
          vm->AttachCurrentThread(&env, nullptr);
      }
      //nullptr
      jclass aClass = env->FindClass("com/jin/jni/bean/NDKDemo");
      //nullptr
      jclass bClass = env->FindClass("android/app/Activity");
      //可以正常获取
      jclass cls = env->FindClass("java/lang/String");
      env->DeleteLocalRef(bClass);
  }
  
  
  extern "C" JNIEXPORT void JNICALL
  Java_com_jin_jni_MainActivity_createClassFromThread(JNIEnv *env,jobject obj) {
      //子线程中创建类
      long pthread;
      JavaVM* vm;
      env->GetJavaVM(&vm);
      pthread_create(&pthread, nullptr, reinterpret_cast<void *(*)(void *)>(create_class), vm);
  }
  ```

##### 获取非系统类

- 使用全局变量进行间接传递

- ```c
  //全局变量，env->NewGlobalRef声明
  jclass ndkClass;
  
  JNIEXPORT jint JNI_OnLoad(JavaVM *vm, void *unused) {
      javaVM = vm;
      JNIEnv *env = nullptr;
      if (vm->GetEnv(reinterpret_cast<void **>(&env), JNI_VERSION_1_6) != JNI_OK) {
          LOGD("GetEnv failed");
          return -1;
      }
  
      jclass localRef = env->FindClass("com/jin/jni/bean/NDKDemo");
      //赋值全局变量
      ndkClass = (jclass)env->NewGlobalRef(localRef);
      return JNI_VERSION_1_6;
  }
  
  //子线程方法体
  void create_class() {
      JNIEnv *env = nullptr;
      bool needDetach = false;
      if (javaVM->GetEnv((void **) &env, JNI_VERSION_1_4) < 0) {
          LOGD("----AttachCurrentThread----");
          javaVM->AttachCurrentThread(&env, NULL);
          needDetach = true;
      }
  
      jfieldID field = env->GetStaticFieldID(ndkClass, "publicStaticStringField", "Ljava/lang/String;");
      jstring data =(jstring) env->GetStaticObjectField(ndkClass, field);
      LOGD("data in threadFunc : %s", env->GetStringUTFChars(data, nullptr));
      env->ExceptionClear();
      if (needDetach) {
          LOGD("----DetachCurrentThread----");
          javaVM->DetachCurrentThread();
      }
  }
  
  extern "C" JNIEXPORT void JNICALL
  Java_com_jin_jni_MainActivity_createClassFromThread(JNIEnv *env,jobject obj) {
      long pthread;
      //创建子线程
      pthread_create(&pthread, nullptr, reinterpret_cast<void *(*)(void *)>(create_class), nullptr);
  }
  ```

#### _init与__initArray__

- so在执行JNI_Onload之前，还会执行两个构造函数init、initarray

- so加固、so中字符串加密等等，一般会把相关代码放到这里

- init的使用

  - ```c
    extern "C" void _init() {
        LOGE("memory-lib init");
    }
    ```

- initarray的使用

  - ```c
    __attribute__((constructor)) void fun1() {
        LOGE("memory-lib fun1");
    }
    
    __attribute__((constructor)) void fun2() {
        LOGE("memory-lib fun2");
    }
    ```

  - __attribute__ ((constructor)) void initArrayTest1(){ ... }

  - __attribute__ ((constructor(200))) void initArrayTest2(){ ... }

  - __attribute__ ((constructor(101))) void initArrayTest3(){ ... }

  - __attribute__ ((constructor, visibility("hidden"))) void initArrayTest4(){ ... }

  - constructor后面的值，较小的先执行，最好从100以后开始用如果constructor后面没有跟值，那么按定义的顺序，从上往下执行 

## so层

### Frida相关函数

#### 枚举so文件的导入表

```javascript
//枚举so文件下的导入表
console.log('------------------------------导入表开始');
var improts = Module.enumerateImports("libencryptlib.so");
for(let i = 0; i < improts.length; i++){
    // console.log(JSON.stringify(improts[i]));
    console.log(improts[i].name + " " + improts[i].address);
}
console.log('------------------------------导入表结束');
```

#### 枚举so文件的导出表

```javascript
console.log('------------------------------导出表开始');
var exports = Module.enumerateExports("libencryptlib.so")
for (let i = 0; i < exports.length; i++) {
    // console.log(JSON.stringify(improts[i]));
    console.log(exports[i].name + " " + exports[i].address);
}
console.log('------------------------------导出表结束');
```

#### 枚举so文件的符号表

```javascript
console.log('------------------------------符号表开始');
var symbols = Module.enumerateSymbols("libencryptlib.so")
for (let i = 0; i < exports.length; i++) {
    // console.log(JSON.stringify(improts[i]));
    console.log(symbols[i].name + " " + symbols[i].address);
}
console.log('------------------------------符号表结束');
```

#### 枚举进程APP已经加载的so库（模块）

```javascript
console.log('------------------------------枚举进程中已经加载的模块(lib)开始');
var modules = Process.enumerateModules()
for (let i = 0; i < modules.length; i++) {
    console.log(JSON.stringify(modules[i]));
    if (modules[i].name === 'libencryptlib.so') {
        console.log('-------------找到你了看看你的导出表')
        modules[i].enumerateExports()
    }
    // console.log(symbols[i].name + " " + symbols[i].address);
}
console.log('------------------------------枚举进程中已经加载的模块(lib)结束');
```

#### 获取so文件的基础地址

```javascript
//找lib的基地址
let module = Process.findModuleByName("libencryptlib.so")
console.log("lib的基础",module.base)
console.log("lib的基址:",Process.findModuleByName("libencryptlib.so").base)
console.log("lib的基址:",Process.getModuleByName("libencryptlib.so").base)
console.log("lib的基址:",Module.findBaseAddress("libencryptlib.so"))
```

#### 通过地址找so文件（Module）

- 只要这个地址在此so地址的区间内都可找到模块

- ```javascript
  console.log("通过基址找module:",Process.findModuleByAddress(Module.findBaseAddress("libencryptlib.so")).name)
  console.log("通过基址找module:",Process.getModuleByAddress(Module.findBaseAddress("libencryptlib.so")).name)
  ```

#### Hook so文件中导出表的函数

- 找到函数的绝对地址

  - ```javascript
    let addr = Module.findExportByName("libencryptlib.so","Java_com_pocket_snh48_base_net_utils_EncryptlibUtils_MD5");
    ```

- 通过地址进行Hook

  - args：代表的是参数数组，针对不同类型需要不同格式输出

  - res：返回值

  - ```javascript
    Interceptor.attach(addr,{
        onEnter:function (args) {
            try {
                var env = Java.vm.getEnv();
                if (!args[5].isNull()) {
                    var javaStr = env.getStringUtfChars(args[5]).readCString();
                    console.log("args[5] (as jstring):", javaStr);
                }
            } catch (e) {
                console.log("args[5] (address):", args[4]);
            }
        },
        onLeave:function (res) {
            console.log("Interceptor onLeave",res)
            try {
                var env = Java.vm.getEnv();
                if (!res.isNull()) {
                    var javaStr = env.getStringUtfChars(res).readCString();
                    console.log("res (as jstring):", javaStr);
                }
            } catch (e) {
                console.log("res (address):", res);
            }
        }
    })
    ```

#### Hook任意函数

- 函数所在so文件的基础地址+函数偏移量+1（可选，arm64无需➕1）

- ```javascript
  //绝对地址，知道函数的真正名称后
  let funcAddr = Module.findExportByName("libencryptlib.so","_ZN7MD5_CTX11MakePassMD5EPhjS0_")
  console.log("addr通过API直接找到绝对地址:",funcAddr)
  
  //通过ida反编译后导出表看到该函数的地址是0x1FA38（实际是偏移地址） 需要基址+偏移量
  console.log("addr提过得知函数的偏移量后加上基址",Process.findModuleByName("libencryptlib.so").base.add(0x1FA38))
  ```

#### 通用Hook打印数据

- ```javascript
      let funcAddr = Module.findExportByName("libencryptlib.so","_ZN7MD5_CTX11MakePassMD5EPhjS0_")
  
  function print_arg(addr){
      var module = Process.findRangeByAddress(addr);
      if(module != null) return hexdump(addr) + "\n";
      return ptr(addr) + "\n";
  }
  function hook_native_addr(funcPtr, paramsNum){
      var module = Process.findModuleByAddress(funcPtr);
      Interceptor.attach(funcPtr, {
          onEnter: function(args){
              this.logs = [];
              this.params = [];
              this.logs.push("call " + module.name + "!" + ptr(funcPtr).sub(module.base) + "\n");
              for(let i = 0; i < paramsNum; i++){
                  this.params.push(args[i]);
                  this.logs.push("this.args" + i + " onEnter: \n" + print_arg(args[i]));
              }
          }, onLeave: function(retval){
              for(let i = 0; i < paramsNum; i++){
                  this.logs.push("this.args" + i + " onLeave: " + print_arg(this.params[i]));
              }
              this.logs.push("retval onLeave: " + print_arg(retval) + "\n");
              console.log(this.logs);
          }
      });
  }
  
  hook_native_addr(funcAddr, 4);
  ```
