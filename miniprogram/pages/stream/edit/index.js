import streamApi from '../../../api/stream'
import deviceApi from '../../../api/device'
import Dialog from '../../../external_components/dialog/dialog'
import Toast from '../../../external_components/toast/toast'

Page({

  data: {
    type: 'edit',
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
    show: false,
    title: '',
    qos: 0,
    data_type: 'int',
    defaultIndex: 0,
    defaultDeviceIndex: 0,
    defaultTypeIndex: 0,
    defaultQosIndex: 0,
    defaultQos: '0',
    defaultType: '整型（int）',
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
      show: !this.data.show
    })

  },
  changeSelect(e) {
    const { index } = e.detail;
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
        data_type: this.data.data_type
      }).then(()=>{
        Toast({
          type: 'success',
          message: '修改成功',
          duration: 1000,
          onClose: () => {
            wx.navigateBack()
          },
        });
      })
    } else {
      streamApi.create({
        name: this.data.name,
        device: this.data.device,
        unit: this.data.unit,
        qos: this.data.qos,
        data_type: this.data.data_type
      }).then(()=>{
        Toast({
          type: 'success',
          message: '创建成功',
          duration: 1000,
          onClose: () => {
            wx.navigateBack()
          },
        });
      })
    }
  }, 
  cancel(){
    wx.navigateBack()
  },
  delete(){
    Dialog.confirm({
      title: '警告！',
      message: `确认删除 ‘${this.data.name} ’吗？\n删除后将清空该数据流下的所有历史数据,且不可恢复。`,
    })
    .then(() => {
      streamApi.delete(this.data.id).then(()=>{
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