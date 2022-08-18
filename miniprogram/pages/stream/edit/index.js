import streamApi from '../../../api/stream'
import deviceApi from '../../../api/device'
import Dialog from '@vant/weapp//dialog/dialog'
import Toast from '@vant/weapp//toast/toast'
import { colorList, iconList, streamTypeList, qosList } from '../../../const'

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
          if (this.data.typeList[i].value == res.dataType) {
            this.setData({
              defaultTypeIndex: i,
              defaultType: this.data.typeList[i].name
            })
          }
        }
        for (let i = 0; i < this.data.typeList; i++) {
          if (this.data.qosList[i].value == res.dataType) {
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
    let editStatusNotOpen = ["qos", "type", "device"]
    this.setData({
      selectName: e.currentTarget.dataset.name,
      selectList: this.data.deviceList,
      title: '所属设备',
      defaultIndex: this.data.defaultDeviceIndex
    })
    if (!(editStatusNotOpen.includes(e.currentTarget.dataset.name) && this.data.type == 'edit')){
      this.setData({
        showPopup: !this.data.showPopup,
      })
    }
    if (e.currentTarget.dataset.name){
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
  generateData(){
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
    if (this.data.type == 'edit'){
      data.id = this.data.id
      data.device = this.data.device
    }
    else if (this.data.type == 'create' && this.data.source != 'create_new_device'){
      data.device = this.data.device
    }
    return data
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
      showPopup: false
    })
  },
  selectColor(e){
    this.setData({
      color: e.currentTarget.dataset.value,
      showPopup: false
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