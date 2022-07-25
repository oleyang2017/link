import deviceApi from '../../../api/device' 

Page({
  data: {
    showAll: false,
    showImage: false,
    canEdit: false,
    canDelete: false,
    canControl: false,
  },
  onLoad(options) {
    this.setData({
      ...options
    })
  },
  onShow(){
    deviceApi.detail(this.data.id).then((res) => {
      wx.setNavigationBarTitle({
        title: res.name
      })
      
      this.setData({
        ...res
      })
    })
    deviceApi.getPerms(this.data.id).then((res) => {
      this.setData({
        canEdit: res.includes('change_device'),
        canDelete: res.includes('delete_device'),
        canControl: res.includes('control_device'),
        prems:res,
      })
    })

  },

  // 更改显示状态
   changeStatus: function(e){
    var key = e.currentTarget.dataset.key
    this.setData({
      [key]: ! this.data[[key]]
    })
  },

  copy(e) {
    wx.setClipboardData({
      data: e.currentTarget.dataset.value,
      success: (res) => {
        wx.showToast({
          title: '已复制',
          duration: 1000,
        })
        wx.vibrateShort({type: 'medium'})
      }
    })
  },
})


