Java.perform(function() {
    const MyWeirdTrustManager = Java.registerClass({
        name: 'com.xiaojianbang.app.MyRegisterClass',
        implements: [Java.use("com.xiaojianbang.app.TestRegisterClass")],
        fields: {
            description: 'java.lang.String',
            limit: 'int',
        },
        methods: {
            $init() {
                console.log('Constructor called');
            },
            test1: [{
                returnType: 'void',
                argumentTypes: [],
                implementation() {
                    console.log('test1 called');
                }
            }, {
                returnType: 'void',
                argumentTypes: ['java.lang.String', 'int'],
                implementation(str, num) {
                    console.log('test1(str, num) called', str, num);
                }
            }],
            test2(str, num) {
                console.log('test2(str, num) called', str, num);
                return null;
            },
        }
    });
    var myObj = MyWeirdTrustManager.$new();
    myObj.test1();
    myObj.test1("xiaojianbang1", 100);
    myObj.test2("xiaojianbang2", 200);
    myObj.limit.value = 10000;
    console.log(myObj.limit.value);

})