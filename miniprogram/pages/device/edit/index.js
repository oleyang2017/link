import deviceApi from '../../../api/device'
import categoryApi from '../../../api/category'
import {
  cos,
  DEFAULT_BUCKET,
  DEFAULT_REGION
} from '../../../api/upload'
import Toast from '../../../external_components/toast/toast'
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
  updateOrCreate(data){
    if (this.data.type == 'edit') {
      var inverface = deviceApi.update(data)
    } else {
      var inverface = deviceApi.create(data)
    }
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
  confirm() {
    if (this.data.filePath) {
      cos.postObject({
        Bucket: DEFAULT_BUCKET,
        Region: DEFAULT_REGION,
        Key: wx.getStorageSync('uid') + '/' + this.data.filePath.slice(11),
        FilePath: this.data.filePath,
      }, (err, data) => {
        let _data = this.generateData()
        if (err) {
          Toast.fail('图片上传失败');
        } else {
          _data.image = "http://" + data.Location
        }
        this.updateOrCreate(_data)
      });
    }
    else{
      let _data = this.generateData()
      this.updateOrCreate(_data)
    }
  },
  cancel() {
    wx.navigateBack()
  },
  // 构造数据
  generateData() {
    let {
      category,
      name,
      desc,
      sequence,
      streams,
      charts,
      image,
    } = this.data

    let data = {
      name,
      category,
      desc,
      image
    }
    if (this.data.type == 'create') {
      if (this.data.charts.length) {
        data.charts = this.data.charts
      }
      if (this.data.streams.length) {
        data.streams = this.data.streams
      }
    } else {
      data.sequence = sequence
    }
    return data
  },

  toOtherPage(e) {
    if (this.data.type == 'edit') {
      wx.navigateTo({
        url: '/pages/' + e.currentTarget.dataset.name + '/list/index?device=' + this.data.id,
      })
    }
  }
})