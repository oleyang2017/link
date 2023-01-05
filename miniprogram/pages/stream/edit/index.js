import streamApi from '../../../api/stream'
import deviceApi from '../../../api/device'
import Dialog from '@vant/weapp//dialog/dialog'
import Toast from '@vant/weapp//toast/toast'
import defaultTheme from '../../../components/ec-canvas/default-theme'
import * as echarts from '../../../components/ec-canvas/echarts'
import defaultOption from '../../../components/ec-canvas/default-option'
import { deepCopy } from '../../../utils/deepCopy'
import {
  colorList,
  iconList
} from '../../../const'

let chart = null

Page({
  data: {
    type: 'edit',
    source: '',
    iconList: iconList,
    colorList: colorList,
    selectList: [],
    selectName: '',
    showPopup: false,
    title: '',
    qos: 0,
    dataType: 'number',
    defaultIndex: 0,
    defaultDeviceIndex: 0,
    color: "bg-blue",
    icon: "icon-kongqiwendu",
    show: false,
    saveData: false,
    showChart: false,
    dataZoom: false,
    themeInputStyle: {
      maxHeight: 100
    },
    ec: {
      lazyLoad: true
    },
    windowWidth: 320,
  },

  onLoad: function (options) {
    var res = wx.getSystemInfoSync()
    this.setData({
      ...options,
      windowWidth: res.windowWidth
    })
    if (options.id) {
      streamApi.detail(options.id).then((res) => {
        this.setData({
          ...res,
        })
      })
    }
    deviceApi.list().then((res) => {
      if (this.data.device) {
        for (let i = 0; i < res.length; i++) {
          if (res[i].id == this.data.device) {
            this.setData({
              defaultDeviceIndex: i,
              defaultDevice: res[i].name
            })
          }
        }
      }
      this.setData({
        deviceList: res
      })
    })
  },

  onReady: function () {
    if (this.data.showChart){
      this.initChart()
    }
  },

  initChart() {
    // 获取组件
    this.ecComponent = this.selectComponent('#chart-demo')
    this.ecComponent.init((canvas, width, height, dpr) => {
      let theme = deepCopy(defaultTheme)
      if (this.data.chartTheme){
        theme = this.data.chartTheme
      }
      echarts.registerTheme('default', theme)
      chart = echarts.init(canvas, "default", {
        width: width,
        height: height,
        devicePixelRatio: dpr
      })
      let options = this.generateOption()
      canvas.setChart(chart)
      chart.setOption(options)
      return chart
    })
  },

  refreshChart() {
    if (this.data.showChart){
      let options = this.generateOption()
      chart.setOption(options, { notMerge: true })
      chart.resize()
      return chart
    }
   
  },

  changeChartTheme(e){
    if(e.detail.value){
      try {
        const customTheme = JSON.parse(e.detail.value)
        this.ecComponent.init((canvas, width, height, dpr) => {
          echarts.registerTheme('custom', customTheme)
          chart = echarts.init(canvas, "custom", {
            width: width,
            height: height,
            devicePixelRatio: dpr
          })
          let options = this.generateOption()
          canvas.setChart(chart)
          chart.setOption(options)
          return chart
        })
      } catch (e) {
        Toast({
          type: 'fail',
          message: '主题设置失败',
          duration: 1000,
        })
      }
    }
    else{
      this.initChart()
    }
  },

  openPopup(e) {
    let editStatusNotOpen = ["qos", "type", "device"]
    this.setData({
      selectName: e.currentTarget.dataset.name,
      selectList: this.data.deviceList,
      title: '所属设备',
      defaultIndex: this.data.defaultDeviceIndex
    })
    if (!(editStatusNotOpen.includes(e.currentTarget.dataset.name) && this.data.type == 'edit')) {
      this.setData({
        showPopup: !this.data.showPopup,
      })
    }
    if (e.currentTarget.dataset.name) {
      this.setData({
        popupType: e.currentTarget.dataset.name,
      })
    }
  },

  changeSelect(e) {
    const {
      index
    } = e.detail
    if (this.data.selectName == 'qos') {
      this.setData({
        qos: this.data.qosList[index].value,
        defaultQos: this.data.qosList[index].name,
        show: false
      })
    } else if (this.data.selectName == 'type') {
      this.setData({
        dataType: this.data.typeList[index].value,
        defaultType: this.data.typeList[index].name,
        show: false
      })
    } else if (this.data.selectName == 'device') {
      this.setData({
        device: this.data.deviceList[index].id,
        defaultDevice: this.data.deviceList[index].name,
        show: false
      })
    }
    this.setData({
      showPopup: false
    })
  },

  generateData() {
    let data = {
      name: this.data.name,
      unitName: this.data.unitName,
      unit: this.data.unit,
      qos: this.data.qos,
      dataType: this.data.dataType,
      icon: this.data.icon,
      color: this.data.color,
      show: this.data.show,
    }
    if (this.data.type == 'edit') {
      data.id = this.data.id
      data.device = this.data.device
    } else if (this.data.type == 'create' && this.data.source != 'create_new_device') {
      data.device = this.data.device
    }
    return data
  },

  generateOption() {
    let option = deepCopy(defaultOption)
    let base = +new Date(2023, 1, 1)
    let oneDay = 24 * 3600 * 1000
    let data = [
      [base, Math.random() * 900]
    ]
    for (let i = 1; i < 200; i++) {
      let now = new Date((base += oneDay))
      data.push([+now, Math.round((Math.random() - 0.5) * 20 + data[i - 1][1])])
    }
    option.series[0].data = data
    option.series[0].name = this.data.name
    if (this.data.dataZoom) {
      delete option.grid.bottom
    } else {
      delete option.dataZoom
    }
    option.tooltip.valueFormatter = (value) => value.toFixed(2) + ` ${this.data.unit}`
    option.yAxis.name = this.data.name + (this.data.unit ? `(${this.data.unit})`: '')
    return option
  },

  handleSwitch(e) {
    let field = e.currentTarget.dataset.value
    let result = e.detail
    this.setData({
      [field]: result
    })
    if (field === 'showChart' && result == true) {
      this.setData({
        saveData: true
      })
      this.initChart()
    }
    if (field === 'dataZoom') {
      this.refreshChart()

    }
  },

  handleShowPopup(e) {
    let type = e.currentTarget.dataset.type
    let value = e.currentTarget.dataset.value
    this.setData({
      [type]: value,
      showPopup: false
    })
  },

  cancel() {
    wx.navigateBack()
  },

  confirm() {
    let data = this.generateData()
    if (this.data.type == 'edit') {
      streamApi.update(data).then(() => {
        Toast({
          type: 'success',
          message: '修改成功',
          duration: 1000,
          onClose: () => {
            wx.navigateBack()
          },
        })
      })
    } else if (this.data.type == 'create' && this.data.source != 'create_new_device') {
      streamApi.create(data).then(() => {
        Toast({
          type: 'success',
          message: '创建成功',
          duration: 1000,
          onClose: () => {
            wx.navigateBack()
          },
        })
      })
    } else if (this.data.type == 'create' && this.data.source == 'create_new_device') {
      let pages = getCurrentPages()
      let prevPage = pages[pages.length - 2]
      let streamList = prevPage.data.streams
      if (this.data.id) {
        data.id = this.data.id
      }
      streamList.push(data)
      prevPage.setData({
        stream: streamList
      })
      wx.navigateBack()
    }
  },

  delete() {
    Dialog.confirm({
        title: '警告！',
        message: `确认删除 ‘${this.data.name} ’吗？\n删除后将清空该数据流下的所有历史数据,且不可恢复。`,
      })
      .then(() => {
        streamApi.delete(this.data.id).then(() => {
          Toast({
            type: 'success',
            message: '删除成功',
            duration: 1000,
            onClose: () => {
              wx.navigateBack()
            },
          })
        })
      })
  },

})