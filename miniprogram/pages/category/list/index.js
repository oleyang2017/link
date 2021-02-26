import categoryApi from '../../../api/category'

Page({
  data: {
    categoryData: [],
    showDialog: false,
    dialogTitle: '新增分类',
    edit: false,
    inputValue: ''
  },

  onLoad: function (options) {
    this.getCategory()
  },

  getCategory() {
    categoryApi.list({}).then((res) => {
      for (let i = 0; i < res.length; i++) {
        res[i].fixed = true
      }
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

  openDialog(e) {
    this.setData({
      showDialog: true,
    })
  },

  bindKeyInput: function (e) {
    this.setData({
      inputValue: e.detail.value
    })
  },

  addCategory() {
    categoryApi.create({
      name: this.data.inputValue
    }).then((res) => {
      res.fixed = !this.data.edit
      let categoryData = this.data.categoryData
      categoryData.push(res)
      this.setData({
        categoryData
      }, () => {
        this.selectComponent('#drag-el').init()
      })
    })
  },
  edit() {
    let categoryData = this.data.categoryData
    let edit = !this.data.edit
    for (let i = 0; i < categoryData.length; i++) {
      categoryData[i].fixed = !edit
      // 关闭所有已经打开的滑动单元格
      if (!edit){
        console.log('#' +categoryData[i].id)
        console.log(this.selectComponent('#drag-el'))
        console.log(this.selectComponent('#' + categoryData[i].id))
        this.selectComponent('#drag-el').selectComponent('#' + categoryData[i].id).close()
      }
      
    }
    this.setData({
      edit,
      categoryData
    }, () => {
      this.selectComponent('#drag-el').init()
    })
  }
})