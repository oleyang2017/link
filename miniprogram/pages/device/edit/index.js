import deviceApi from '../../../api/device'
import categoryApi from '../../../api/category'
import Toast from '@vant/weapp//toast/toast'
const app = getApp()

Page({
  data: {
    type: 'edit',
    show: false,
    categoryList: [],
    categoryIndex: 0,
    charts: [],
    streams: [],
    triggers: [],
    filePath: null
  },

  onLoad: function (options) {
    this.setData({
      ...options
    })
    if (options.id) {
      deviceApi.detail(this.data.id).then((res) => {
        let image_list = []
        if (res.image) {
          image_list = [{
            url: res.image
          }]
        }
        this.setData({
          ...res,
          image_list
        })
      })
    }
  },
  onShow: function () {
    // 因为在其他页面setData不会刷新页面，这里再set一次强制刷新页面
    this.setData({...this.data})
  },
  openPopup() {
    if (!this.data.show && this.data.categoryList.length == 0) {
      this.getCategory()
    }
    this.setData({
      show: !this.data.show
    })
  },
  async getCategory() {
    let categoryList = await categoryApi.list()
    categoryList.forEach((item, index) => {
      item.text = item.name
      item.defaultIndex = item.id
      if (item.id == this.data.category) {
        this.setData({
          categoryIndex: index
        })
      }
    });
    this.setData({
      categoryList,
    })
  },
  changeCagetory(e) {
    this.setData({
      category: e.detail.value.id,
      category_name: e.detail.value.name,
      show: false,
    })
  },
  updateOrCreate(data) {
    if (this.data.type == 'edit') {
      var inverface = deviceApi.update(data)
    } else {
      var inverface = deviceApi.create(data)
      inverface.then((res) => {
        Toast({
          type: 'success',
          message: this.data.type == 'edit' ? '修改成功' : '创建成功',
          duration: 1000,
          onClose: () => {
            wx.navigateBack()
          },
        });
      })
    }

  },
  afterRead(e) {
    const {
      file
    } = e.detail;
    console.log(e.detail)
    this.setData({
      image_list: [{
        url: file.url
      }],
      filePath: file.url
    })
  },
  deleteImage() {
    this.setData({
      image_list: [],
      filePath: null
    })
  },
  confirm() {
    let _data = this.generateData()
    if (this.data.type == 'create'){
      deviceApi.create(_data).then((res) => {
        Toast({
          type: 'success',
          message: '创建成功',
          duration: 1000,
          onClose: () => {
            wx.navigateBack()
          },
        });
      })
    } else {
      deviceApi.update(_data)
      Toast({
        type: 'success',
        message: '修改成功',
        duration: 1000,
        onClose: () => {
          wx.navigateBack()
        },
      });
    }
  },
  cancel() {
    wx.navigateBack()
  },
  // 构造数据
  generateData() {
    let {
      id,
      name,
      streams,
      charts,
      filePath
    } = this.data

    let data = {
      name,
      filePath
    }
    if (this.data.category){
      data.category = this.data.category
    }
    if (this.data.desc){
      data.desc = this.data.desc
    }
    if (this.data.type == 'create') {
      if (this.data.charts.length) {
        data.charts = charts
      }
      if (this.data.streams.length) {
        data.streams = streams
      }
    } else {
      data.id = id
    }
    return data
  },

  toOtherPage(e) {
    if (this.data.type == 'edit') {
      wx.navigateTo({
        url: '/pages/' + e.currentTarget.dataset.name + '/list/index?device=' + this.data.id,
      })
    }
  },
  createStream(e){
    wx.navigateTo({
      url: '/pages/stream/edit/index?type=create&source=create_new_device',
    })
  }
})