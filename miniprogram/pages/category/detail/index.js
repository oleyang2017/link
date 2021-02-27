import categoryApi from '../../../api/category'
Page({

  data: {
    showDialog: false,
    inputValue: ''
  },

  onLoad: function (options) {
    categoryApi.detail(options.id).then((res) => {
      this.setData({
        ...res,
      })
    })
  },
  updateCategory() {
    categoryApi.update({
      name: this.data.inputValue,
      id: this.data.id
    }).then((res) => {
      this.setData({
        ...res
      })
    })
  },
  deleteCategory() {
    categoryApi.delete(this.data.id).then(()=>{
      wx.navigateBack({
        delta: 0,
      })
    })
  },
  showDialog() {
    this.setData({
      showDialog: true,
      inputValue: this.data.name
    })
  },
  bindKeyInput(e) {
    this.setData({
      inputValue: e.detail.value
    })
  },

})