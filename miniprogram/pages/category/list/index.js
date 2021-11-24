import categoryApi from '../../../api/category'

Page({
  data: {
    categoryData: [],
    showDialog: false,
    dialogTitle: '新增分类',
    edit: false,
    scrollTop: 0,
    pageMetaScrollTop: 0,
    inputValue: '',
    sortValue: {}
  },

  onLoad() {},

  onShow() {
    this.getCategory()
  },

  getCategory() {
    categoryApi.list({}).then((res) => {
      for (let i = 0; i < res.length; i++) {
        res[i].fixed = !this.data.edit
      }
      this.setData({
        categoryData: res,
      }, () => {
        this.selectComponent('#drag-el').init()
      }) // 更改listData需要重新init
    })
  },

  sortEnd(e) {
    let sortValue = {}
    for (let i = 0; i < this.data.categoryData.length; i++) {
      let beforItem = this.data.categoryData[i]
      for (let n = 0; n < e.detail.listData.length; n++) {
        if (beforItem.id == e.detail.listData[n].id && beforItem.sequence != n) {
          sortValue[beforItem.id] = n
        }
      }
    }
    this.setData({
      sortValue,
      categoryData: e.detail.listData
    });
  },

  openDialog() {
    this.setData({
      showDialog: true,
      inputValue: ''
    })
  },

  scroll(e) {
    this.setData({
      pageMetaScrollTop: e.detail.scrollTop
    })
  },

  onPageScroll(e) {
    this.setData({
      scrollTop: e.scrollTop
    });
  },

  bindKeyInput(e) {
    this.setData({
      inputValue: e.detail.value
    })
  },

  createCategory() {
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
      if (!edit) {
        this.selectComponent('#drag-el').initComponent(categoryData[i].id)
      }
    }
    // 退出编辑模式后将新的排序上传并刷新页面
    if (!edit) {
      categoryApi.sort(this.data.sortValue).then(() => {
        this.setData({
          edit
        })
        this.getCategory()
      })
    } else {
      this.setData({
        edit,
        categoryData
      }, () => {
        this.selectComponent('#drag-el').init()
      })
    }

  }
})