import categoryApi from '../../api/category'
import deviceApi from '../../api/device'

Page({
  data: {
    category: [],
    showMask: false,
    active: '',
    popupHeight: '100px',
    refresh: false,
  },

  onLoad: function (options) {
    this.getCategory()
  },

  showMask: function () {
    this.setData({
      showMask: !this.data.showMask
    })
  },
  async getCategory() {
    let category = await categoryApi.list()
    let device = await deviceApi.list()
    let uid = wx.getStorageSync('uid')
    let noCategory = []
    let shareCategory = []
    for (let i = 0; i < device.length; i++) {
      let hasCategory = false
      for (let m = 0; m < category.length; m++) {
        if (!category[m].device) {
          category[m].device = []
        }
        if (device[i].category == category[m].id) {
          category[m].device.push(device[i])
          hasCategory = true
        }
      }
      if (device[i].create_user != uid) {
        shareCategory.push(device[i])
      } else if (!hasCategory) {
        noCategory.push(device[i])
      }
    }
    let categoryCount = category.length
    category.push({
      name: '未分类',
      device: noCategory
    })
    category.push({
      name: '共享设备',
      device: shareCategory
    })
    if (!categoryCount){
      category.push({
        name: '',
        device:[]
      })
    }
    this.setData({
      category,
      refresh: false,
      popupHeight: categoryCount * 36 > 260 ? '260px' : categoryCount * 36 + 'px'
    })
  },
  changeCategory(e) {
    this.setData({
      active: e.detail.name ? e.detail.name : e.currentTarget.dataset.id
    })
  },
  toDetail(e) {
    wx.navigateTo({
      url: '/pages/device/detail/index?id=' + e.currentTarget.dataset.id,
    })
  },
  refresh: function () {
    this.setData({
      refresh: true
    })
    this.getCategory()
  },
})