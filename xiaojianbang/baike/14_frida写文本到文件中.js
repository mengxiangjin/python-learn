Java.perform(function() {
    var write = new File('/data/data/com.xiaojianbang.app/new.txt','w')
    write.write('aaabbbccc')
    write.flush()
    write.close()
})