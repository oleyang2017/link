import categoryApi from '../../../api/category'
Page({

  data: {

  },

  onLoad: function (options) {
    this.setData({
      id: options.id
    })
    categoryApi.detail(options.id).then()
  },

})