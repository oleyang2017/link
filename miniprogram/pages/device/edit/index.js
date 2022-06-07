import deviceApi from '../../../api/device'
import categoryApi from '../../../api/category'
import streamApi from '../../../api/stream'
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
    filePath: null,
    deleteStreams: [],
  },

  onLoad: function (options) {
    this.setData({
      ...options
    })
  },
  onShow: function () {
    if (this.data.type == 'edit') {
      this.getDetailInfo(this.data.id)
    } else if (this.data.type == 'create') {
      // 因为在其他页面setData不会刷新页面，这里再set一次强制刷新页面
      this.setData({
        ...this.data
      })
    }
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
  getDetailInfo(id) {
    deviceApi.detail(id).then((res) => {
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
  },
  afterRead(e) {
    const {
      file
    } = e.detail;
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
  async confirm() {
    let _data = this.generateData()
    let deleteStreams = this.data.deleteStreams
    if (this.data.type == 'create') {
      await deviceApi.create(_data)
    } else {
      await deviceApi.update(_data)
    }

    for (let i = 0; i < deleteStreams.length; i++) {
      await streamApi.delete(deleteStreams[i])
    }
    Toast({
      type: 'success',
      message: this.data.type == 'create' ? '创建成功' : '修改成功',
      duration: 1000,
      onClose: () => {
        wx.navigateBack()
      },
    });
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
    if (this.data.category) {
      data.category = this.data.category
    }
    if (this.data.desc) {
      data.desc = this.data.desc
    }
    if (this.data.streams.length) {
      data.streams = streams
    }
    if (this.data.type == 'create') {
      if (this.data.charts.length) {
        data.charts = charts
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
  createStream(e) {
    wx.navigateTo({
      url: `/pages/stream/edit/index?type=create&source=${e.currentTarget.dataset.source}&device=${this.data.id}`,
    })
  },
  deleteStream(e) {
    let streams = this.data.streams
    streams.splice(e.currentTarget.dataset.index, 1)
    this.setData({
      streams
    })
    if (e.currentTarget.dataset.id) {
      let deleteStreams = this.data.deleteStreams
      deleteStreams.push(e.currentTarget.dataset.id)
      this.setData({
        deleteStreams
      })
    }
  },
})