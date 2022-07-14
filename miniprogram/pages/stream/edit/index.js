import streamApi from '../../../api/stream'
import deviceApi from '../../../api/device'
import Dialog from '@vant/weapp//dialog/dialog'
import Toast from '@vant/weapp//toast/toast'

Page({
  data: {
    type: 'edit',
    source: '',
    typeList: [{
        name: '整型（int）',
        value: 'int'
      },
      {
        name: '浮点型（float）',
        value: 'float'
      },
      {
        name: '布尔型（bool）',
        value: 'bool'
      },
      {
        name: '字符型（char）',
        value: 'char'
      }
    ],
    qosList: [{
        name: '0',
        value: 0
      },
      {
        name: '1',
        value: 1
      },
      {
        name: '2',
        value: 2
      }
    ],
    selectList: [],
    selectName: '',
    showPopup: false,
    showIconPopup: false,
    showColorPopup: false,
    title: '',
    qos: 0,
    data_type: 'int',
    defaultIndex: 0,
    defaultDeviceIndex: 0,
    defaultTypeIndex: 0,
    defaultQosIndex: 0,
    defaultQos: '0',
    defaultType: '整型（int）',
    color: "bg-blue",
    icon: "icon-kongqiwendu",
    iconList: [
      {
        "name": "电导率",
        "value": "icon-diandaoshuai"
      },
      {
        "name": "PH值",
        "value": "icon-PHzhi"
      },
      {
        "name": "含氧量",
        "value": "icon-hanyangliang"
      }, {
        "name": "水位",
        "value": "icon-shuiwei"
      },
      {
        "name": "库容",
        "value": "icon-kurong"
      },
      {
        "name": "浊度",
        "value": "icon-zhuodu"
      },
      {
        "name": "溶解氧",
        "value": "icon-rongjieyang"
      },
      {
        "name": "压力",
        "value": "icon-yali"
      },
      {
        "name": "悬浮物",
        "value": "icon-xuanfuwu"
      },
      {
        "name": "流量",
        "value": "icon-liuliang"
      },
      {
        "name": "水温",
        "value": "icon-shuiwen"
      },
      {
        "name": "土壤水分",
        "value": "icon-turangshuifen"
      },
      {
        "name": "土壤湿度",
        "value": "icon-turangshidu"
      },
      {
        "name": "风速",
        "value": "icon-fengsu"
      },
      {
        "name": "电源电压",
        "value": "icon-dianyuandianya"
      },
      {
        "name": "CO2浓度",
        "value": "icon-CO2nongdu"
      },
      {
        "name": "大气压",
        "value": "icon-daqiya"
      },
      {
        "name": "光合辐射",
        "value": "icon-guanghefushe"
      },
      {
        "name": "结露",
        "value": "icon-jielou"
      },
      {
        "name": "空气温度",
        "value": "icon-kongqiwendu"
      },
      {
        "name": "空气湿度",
        "value": "icon-kongqishidu"
      },
      {
        "name": "风向",
        "value": "icon-fengxiang"
      },
      {
        "name": "降雨量",
        "value": "icon-jiangyuliang"
      },
      {
        "name": "露点温度",
        "value": "icon-loudianwendu"
      },
      {
        "name": "光照强度",
        "value": "icon-guangzhaoqiangdu"
      },
      {
        "name": "蒸发量",
        "value": "icon-zhengfaliang"
      },
      {
        "name": "总辐射",
        "value": "icon-zongfushe"
      }, {
        "name": "光照时间",
        "value": "icon-guangzhaoshijian"
      },
      {
        "name": "PM2.5",
        "value": "icon-PM25"
      },
      {
        "name": "小时降雨量",
        "value": "icon-xiaoshijiangyuliang"
      },
      {
        "name": "风力",
        "value": "icon-fengli"
      },
      {
        "name": "硫化氢",
        "value": "icon-liuhuaqing"
      },
    ],
    colorList: [
      "bg-red",
      "bg-orange",
      "bg-yellow",
      "bg-olive",
      "bg-green",
      "bg-cyan",
      "bg-blue",
      "bg-purple",
      "bg-mauve",
      "bg-pink",
      "bg-brown",
      "bg-grey",
      "bg-black",
      "bg-gray",
      "bg-red light",
      "bg-orange light",
      "bg-yellow light",
      "bg-olive light",
      "bg-green light",
      "bg-cyan light",
      "bg-blue light",
      "bg-purple light",
      "bg-mauve light",
      "bg-pink light",
      "bg-brown light",
      "bg-grey light",
      "bg-gradual-red",
      "bg-gradual-orange",
      "bg-gradual-green",
      "bg-gradual-purple",
      "bg-gradual-pink",
      "bg-gradual-blue",
    ]
  },

  onLoad: function (options) {
    this.setData({
      ...options
    })
    if (options.id) {
      streamApi.detail(options.id).then((res) => {
        this.setData({
          ...res,
        })
        for (let i = 0; i < this.data.typeList; i++) {
          if (this.data.typeList[i].value == res.data_type) {
            this.setData({
              defaultTypeIndex: i,
              defaultType: this.data.typeList[i].name
            })
          }
        }
        for (let i = 0; i < this.data.typeList; i++) {
          if (this.data.qosList[i].value == res.data_type) {
            this.setData({
              defaultQosIndex: i,
              defaultQos: this.data.qosList[i].name
            })
          }
        }
      })
    }
    if (options.type) {
      this.setData({
        type: options.type
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
  changeIconPopup(e){
    this.setData({
      showIconPopup: !this.data.showIconPopup
    })
  },
  openPopup(e) {
    if (this.data.type == 'edit') {
      return
    }
    if (e.currentTarget.dataset.name == 'qos') {
      this.setData({
        selectName: e.currentTarget.dataset.name,
        selectList: this.data.qosList,
        title: 'QOS',
        defaultIndex: this.data.defaultQosIndex
      })
    } else if (e.currentTarget.dataset.name == 'type') {
      this.setData({
        selectName: e.currentTarget.dataset.name,
        selectList: this.data.typeList,
        title: '数据类型',
        defaultIndex: this.data.defaultTypeIndex
      })
    } else if (e.currentTarget.dataset.name == 'device') {
      this.setData({
        selectName: e.currentTarget.dataset.name,
        selectList: this.data.deviceList,
        title: '所属设备',
        defaultIndex: this.data.defaultDeviceIndex
      })
    }
    this.setData({
      showPopup: !this.data.showPopup
    })

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
        data_type: this.data.typeList[index].value,
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
  },
  confirm() {
    if (this.data.type == 'edit') {
      streamApi.update({
        id: this.data.id,
        name: this.data.name,
        device: this.data.device,
        unit_name: this.data.unit_name,
        unit: this.data.unit,
        qos: this.data.qos,
        data_type: this.data.data_type,
        icon: this.data.icon,
        color: this.data.color,
        show: this.data.show,
      }).then(() => {
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
      streamApi.create({
        name: this.data.name,
        device: this.data.device,
        unit: this.data.unit,
        qos: this.data.qos,
        data_type: this.data.data_type,
        icon: this.data.icon,
        color: this.data.color,
        show: this.data.show,
      }).then(() => {
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
      let stream = {
        name: this.data.name,
        unit: this.data.unit,
        unit_name: this.data.unit_name,
        qos: this.data.qos,
        data_type: this.data.data_type,
        icon: this.data.icon,
        color: this.data.color,
        show: this.data.show,
      }
      if (this.data.id) {
        stream.id = this.data.id
      }
      streamList.push(stream)
      prevPage.setData({
        stream: streamList
      })
      wx.navigateBack()
    }
  },
  changeShow({
    detail
  }) {
    this.setData({
      show: detail
    });
  },
  selectIcon(e){
    this.setData({
      icon: e.currentTarget.dataset.value,
      showIconPopup: false
    })
  },
  changeColorPopup(e){
    this.setData({
      showColorPopup: !this.data.showColorPopup
    })
  },
  selectColor(e){
    this.setData({
      color: e.currentTarget.dataset.value,
      showColorPopup: false
    })
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