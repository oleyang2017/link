import streamApi from '../../../api/stream'
import deviceApi from '../../../api/device'
import * as echarts from '../../../components/ec-canvas/echarts';
import Dialog from '@vant/weapp//dialog/dialog'
import Toast from '@vant/weapp//toast/toast'
import theme from '../../../components/ec-canvas/default-theme'
import {
  colorList,
  iconList,
} from '../../../const'

function initChart(canvas, width, height, dpr) {
  echarts.registerTheme('default', theme)
  const chart = echarts.init(canvas, "default", {
    width: width,
    height: height,
    devicePixelRatio: dpr // 像素
  });
  canvas.setChart(chart);
  var option = {
    title: {
      text: "图表标题",
      left: "center",
      textStyle:{
        fontSize :14
      },
      top: "bottom",
      subtext: "图表名称"
    },
    // legend: {
    //   data: ['A'],
    //   top: 50,
    //   left: 'center',
    //   backgroundColor: 'red',
    //   z: 100
    // },
    grid: {
      containLabel: true
    },
    tooltip: {
      show: true,
      trigger: 'axis'
    },
    xAxis: {
      type: 'time',
      boundaryGap: false,
      data: [
        '2023-01-01 00:00:00', 
        '2023-01-01 01:00:00', 
        '2023-01-01 02:00:00', 
        '2023-01-01 03:00:00',
        '2023-01-01 04:00:00',
        '2023-01-01 05:00:00',
        '2023-01-01 06:00:00',
        '2023-01-01 07:00:00',
      ],
    },
    yAxis: {
      x: 'center',
      type: 'value',
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    series: [{
      name: 'A',
      type: 'line',
      smooth: true,
      data: [18, 36, 65, 30, 78, 40, 33]
    }]
  };

  chart.setOption(option);
  return chart;
}
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
    showChart: true,
    themeInputStyle: {
      maxHeight: 200
    },
    ec: {
      onInit: initChart
    },
    windowWidth: 320,
  },

  onLoad: function (options) {
    var res = wx.getSystemInfoSync();
    this.setData({
      ...options,
      windowWidth: res.windowWidth - 30
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
    } = e.detail;
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
        });
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
        });
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

  handleSwitch(e) {
    let field = e.currentTarget.dataset.value
    let result = e.detail
    this.setData({
      [field]: result
    });
    if(field === 'showChart' && result == true){
      this.setData({
        saveData: true
      });
    }
  },

  handleShowPopup(e){
    let type = e.currentTarget.dataset.type
    let value = e.currentTarget.dataset.value
    this.setData({
      [type]: value,
      showPopup: false
    });
  },

  cancel() {
    wx.navigateBack()
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