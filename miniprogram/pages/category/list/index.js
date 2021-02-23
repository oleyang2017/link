import categoryApi from '../../../api/category'

Page({
  data: {
    categoryData: []
  },

  onLoad: function (options) {
    categoryApi.list({}).then((res) => {
      this.setData({
        categoryData: res,
      }, () => {
        this.selectComponent('#drag-el').init()
      }) // 更改listData需要重新init
    })
  },

  sortEnd(e) {
    let newSort = {}
    for (let i = 0; i < this.data.categoryData.length; i++) {
      let beforItem = this.data.categoryData[i]
      for (let n = 0; n < e.detail.listData.length; n++) {
        if (beforItem.id == e.detail.listData[n].id && beforItem.sequence != n) {
          newSort[beforItem.id] = n
        }
      }
    }
    categoryApi.sort(newSort)
    this.setData({
      listData: e.detail.listData
    });
  },

})