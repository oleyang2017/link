import categoryApi from '../../api/category'
import deviceApi from '../../api/device'

Page({
  data: {
    category: [],
    showMask: false,
    active: '',
    popupHeight: '100px',
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
    let noCategory = []
    for (let i = 0; i < device.length; i++) {
      let hasCategory = false
      for (let m = 0; m < category.length; m++) {
        if (!category[m].device) {
          category[m].device = []
        }
        if (device[i].category == category[m].id) {
          category[m].device = [device[i]]
          hasCategory = true
        }
      }
      if (!hasCategory){
        noCategory.push(device[i])
      }
    }
    category.push({name: '未分类', device: noCategory})
    this.setData({
      category,
      popupHeight: (category.length - 1) * 36 > 260 ? '260px' : (category.length - 1) * 36 + 'px'
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
  }
})