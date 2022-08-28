import deviceApi from '../../../api/device'
import categoryApi from '../../../api/category'
import streamApi from '../../../api/stream'
import Toast from '@vant/weapp//toast/toast'
import {
  deviceImageList
} from '../../../const'
const app = getApp()

Page({
  data: {
    needRefresh: false,
    type: 'edit',
    show: false,
    popupType: "category",
    categoryList: [],
    categoryIndex: 0,
    charts: [],
    streams: [],
    triggers: [],
    filePath: null,
    deleteStreams: [],
    deviceImageList,
  },

  onLoad: function (options) {
    this.setData({
      ...options
    })
    if (options.id) {
      this.getDetailInfo(this.data.id)
    }
  },
  onShow: function () {
    if (this.data.type == 'create') {
      // 因为在其他页面setData不会刷新页面，这里再set一次强制刷新页面
      this.setData({
        ...this.data
      })
    }
  },
  openPopup(e) {
    if (e.currentTarget.dataset.type) {
      this.setData({
        popupType: e.currentTarget.dataset.type
      })
    }
    if (e.currentTarget.dataset.type == 'category') {
      // 关闭的时候也会调用这个方法，避免再次请求分类接口
      if (!this.data.show && this.data.categoryList.length == 0) {
        this.getCategory()
      }
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
  selectItem(e) {
    if (this.data.popupType == 'category') {
      this.setData({
        category: e.detail.value.id,
        categoryName: e.detail.value.name,
        show: false,
      })
    } else if (this.data.popupType == 'stream') {
      let customInfo = this.data.customInfo ? this.data.customInfo : ""
      if (e.detail.value.name) {
        customInfo = customInfo + `[${e.detail.value.name}]`
      }
      this.setData({
        customInfo,
        show: false,
      })
    }
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
      let imageList = []
      if (res.image) {
        imageList = [{
          url: res.image
        }]
      }
      this.setData({
        ...res,
        imageList
      })
    })
  },
  afterRead(e) {
    const {
      file
    } = e.detail;
    this.setData({
      imageList: [{
        url: file.url
      }],
      filePath: file.url,
      image: file.url,
      show: false,
    })
  },
  deleteImage() {
    this.setData({
      imageList: [],
      filePath: null,
      image: null,
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
      filePath,
      customInfo,
      desc,
      category,
      imageUrl,
    } = this.data

    let data = {
      name,
      streams,
      charts,
      filePath,
      customInfo,
      desc,
      category,
      imageUrl,
    }
    data = Object.keys(data).filter((key) => data[key] !== null && data[key] !== undefined).reduce((acc, key) => ({
      ...acc,
      [key]: data[key]
    }), {});

    if (this.data.type == 'create') {
      if (charts.length == 0) {
        delete data.charts
      }
      if (streams.length == 0) {
        delete data.streams
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
  choiceImage(e) {
    this.setData({
      imageUrl: `/static/images/device/${e.currentTarget.dataset.value}`,
      show: false
    })
  }
})