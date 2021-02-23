
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
    onClose(event) {
      const { position, instance } = event.detail;
      instance.close()
      console.log(event)
      console.log(position)
      console.log(instance)
    },
    closeSwipe(event) {
      console.log(event)
      const { instance } = event.detail;
      console.log(instance)
      instance.close()
    },
    toDetail(e){
      console.log(e)
      wx.navigateTo({
        url: "/pages/category/detail/index?id=" + e.currentTarget.dataset.id,
      })
    },
    deleteCategory(e) {
      console.log(e)
      console.log('close')
    },
  }
})
