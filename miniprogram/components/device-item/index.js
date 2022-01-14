Component({
  properties: {
      deviceId: Number,
      index: Number,
      index:  Number,
      name: String,
      status: Boolean,
      image: String,
      lastValue: null,
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
