import categoryApi from '../../../../api/category'

Component({
  properties: {
    columns: {
      type: Number,
      value: 1
    },
    itemData: {
      type: Object,
      value: {}
    }
  },

  data: {

  },

  methods: {
    closeSwipe(e) {
      let _el = this.selectComponent('#drag-item-' + e.currentTarget.dataset.id)
      if (_el){
        _el.close()
      }
    },
    init(id){
      let _el = this.selectComponent('#' + id)
      if (_el) {
        _el.close()
      }
    },
    toDetail(e) {
      if(e.currentTarget.dataset.edit){
        wx.navigateTo({
          url: "/pages/category/detail/index?id=" + e.currentTarget.dataset.id,
        })
      }
    },
    deleteCategory(e) {
      categoryApi.delete(e.currentTarget.dataset.id).then(()=>{
        this.triggerEvent('refresh')
      })
    },
  }
})