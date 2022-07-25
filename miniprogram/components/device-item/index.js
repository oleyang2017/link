Component({
  properties: {
    deviceId: Number,
    index: Number,
    index: Number,
    name: String,
    status: Boolean,
    image: String,
    customInfo: String,
    imageUrl: String,
  },
  lifetimes: {
    attached: function () {
      let {
        image,
        imageUrl
      } = this.data
      if (!image && !imageUrl) {
        this.setData({
          deviceImage: "/static/images/device/Devices.png"
        })
      } else {
        this.setData({
          deviceImage: image ? image : imageUrl
        })
      }
    },
  },
  data: {

  },

  methods: {
    _toDeviceDetail(e) {
      wx.navigateTo({
        url: '/pages/device/detail/index?id=' + e.currentTarget.dataset.id,
      })
    },
  }
})