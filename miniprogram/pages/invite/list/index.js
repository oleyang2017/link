import inviteApi from '../../../api/invite'

Page({

  /**
   * 页面的初始数据
   */
  data: {
    inviteList: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.getInviteList()
  },

  getInviteList(){
    inviteApi.list().then((res)=>{
      var now = new Date();
      for(let i=0; i<res.length;i++){
        let item = res[i]
        if(!item.enable || (item.count>0 && item.count<=item.invitedCount) || (item.endTime && new Date(item.endTime) < now)){
          item.canShare=false
        }
        else{
          item.canShare=true
        }
      }
      this.setData({
        inviteList: res
      })
    })
  }

})