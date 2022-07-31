import inviteApi from '../../../api/invite';
import {
  permissionsMap
} from '../../../const'

Page({
  data: {
    canOperate: false,
    permissionsMap: permissionsMap,
  },

  onLoad(options) {
    this.setData({
      ...options
    })
    this.getInviteInfo(options.id)
  },

  getInviteInfo(id) {
    inviteApi.detail(id).then((res) => {
      let now = new Date()
      if (!res.enable || (res.count > 0 && res.count <= res.invitedCount) || (res.endTime && new Date(res.endTime) < now) || (res.records.length > 0)) {
        res.canOperate = false
      } else {
        res.canOperate = true
      }
      if(res.records.length){
        wx.setNavigationBarColor({
          frontColor: '#ffffff',
          backgroundColor: '#ffffff',
         
        })
      }
      this.setData({
        ...res
      })
    })
  },
  onClick(e) {
    inviteApi.share({
      id: this.data.id,
      operation: e.currentTarget.dataset.value
    }).then((res) => {
      wx.reLaunch({
        url: '/pages/device/index'
      })
    })
  }

})