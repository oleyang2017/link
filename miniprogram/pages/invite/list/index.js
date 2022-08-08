import inviteApi from '../../../api/invite'

Page({

  data: {
    inviteList: []
  },
  onShow(){
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