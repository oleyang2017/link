import deviceApi from '../../../api/device' 

Page({
  data: {
    showAll: false,
    showImage: false,
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


