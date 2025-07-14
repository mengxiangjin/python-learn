import frida
import sys

#spawn程序重启即开始监听hook
# spawn程序重启即开始监听hook
rdev = frida.get_remote_device()
# spawn写包名
pid = rdev.spawn(["com.soom.live999"])
session = rdev.attach(pid)

# var
# MissVideoPlayViewHolder = Java.use("com.miss.video.views.MissVideoPlayViewHolder");
# // 替换类中的方法
# MissVideoPlayViewHolder.stopPlay.implementation = function()
# {
#     console.log("stopPlay stopPlay：");
# }


# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码
scr = """
Java.perform(function () {
    var VideosDetailsBean = Java.use("com.miss.common.bean.VideosDetailsBean");
   //替换类中的方法
    VideosDetailsBean.getVipFree.implementation = function(){
        console.log("this.vipFree",this.vipFree);
        return this.getVipFree();
    }
    
    
     var VideoMissPlayActivity = Java.use("com.miss.video.activity.VideoMissPlayActivity");
   //替换类中的方法
    VideoMissPlayActivity.forward.overload('android.content.Context','java.lang.String').implementation = function(ctx,p){
        console.log("forward");
        this.forward(ctx,p);
    }
 
     VideoMissPlayActivity.forwardSingle.implementation = function(ctx,bean){
        console.log("getId",bean.getId());
        console.log("getUid",bean.getUid());
         console.log("getTitle",bean.getTitle());
        console.log("getSummary",bean.getSummary());
        console.log("getThumb",bean.getThumb());
        console.log("getThumbs",bean.getThumbs());
        console.log("getTrialUrl",bean.getTrialUrl());
        console.log("getTrialSeconds",bean.getTrialSeconds());
        console.log("getTrialSecondsLabel",bean.getTrialSecondsLabel());
        console.log("getUrl",bean.getUrl());
        console.log("getUrlW",bean.getUrlW());
        console.log("getStatus",bean.getStatus());
        console.log("getStatusLabel",bean.getStatusLabel());
        console.log("getSeconds",bean.getSeconds());
        console.log("getSecondsLabel",bean.getSecondsLabel());
        console.log("getAddTime",bean.getAddTime());
        console.log("getAddTimeLabel",bean.getAddTimeLabel());
        console.log("getLat",bean.getLat());
        console.log("getLng",bean.getLng());
        console.log("getCity",bean.getCity());
        console.log("getOrientation",bean.getOrientation());
        console.log("getWeight",bean.getWeight());
        console.log("getIsTop",bean.getIsTop());
        console.log("getPrice",bean.getPrice());
        console.log("getType",bean.getType());
        console.log("getCollected",bean.getCollected());
        console.log("getCollectNum",bean.getCollectNum());
        console.log("getViewNum",bean.getViewNum());
        console.log("getWatches",bean.getWatches());
        console.log("getLikeNum",bean.getLikeNum());
        console.log("getDislikes",bean.getDislikes());
        console.log("getShareNum",bean.getShareNum());
        console.log("getDeFriends",bean.getDeFriends());
        console.log("getCommentNum",bean.getCommentNum());
        console.log("getSales",bean.getSales());
        console.log("getSalesAmount",bean.getSalesAmount());
        console.log("getSalesAmountLabel",bean.getSalesAmountLabel());
        console.log("getPurchased",bean.getPurchased());
        console.log("getLiked",bean.getLiked());
        console.log("getDisliked",bean.getDisliked());
        console.log("getFollowed",bean.getFollowed());
        console.log("getNickName",bean.getNickName());
        console.log("getAvatar",bean.getAvatar());
        console.log("getIsBuy",bean.getIsBuy());
        console.log("getPriceLabel",bean.getPriceLabel());
        console.log("getVipFree",bean.getVipFree());
        console.log("getUserBean",bean.getUserBean());
        this.forwardSingle(ctx,bean);
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

