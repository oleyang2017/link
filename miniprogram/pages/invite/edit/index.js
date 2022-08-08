import {
  inviteTypeList
} from '../../../const'
import deviceApi from '../../../api/device'
import inviteApi from '../../../api/invite'
import { format } from 'fecha'
Page({

  /**
   * 页面的初始数据
   */
  data: {
    inviteType: "device",
    disInviteType: "设备",
    canChangeObj: true,
    showPopup: false,
    choiceType: 'object',
    inviteTypeList,
    defaultObjIndex:0,
    disObjName: '',
    minDate: new Date().getTime(),
    maxDate: new Date(2099, 1, 1).getTime(),
    currentDate: new Date().getTime(),
    permissions: [],
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.setData({
      ...options
    })
    deviceApi.list({onlyCreator:true}).then((res) => {
      if (this.data.objectId && this.data.inviteType == 'device') {
        for (let i = 0; i < res.length; i++) {
          if (res[i].id == this.data.objectId) {
            this.setData({
              defaultObjIndex: i,
              disObjName: res[i].name
            })
          }
        }
      }
      this.setData({
        deviceList: res
      })
    })
  },

  onShow() {

  },

  openPopup(e) {
    if (this.data.canChangeObj) {
      this.setData({
        showPopup: !this.data.showPopup,
        choiceType: e.currentTarget.dataset.name
      })
    }

  },
  onConfirmType(e) {
    const {
      detail
    } = e
    this.setData({
      showPopup: false,
      objectId: null,
      disInviteType: detail.value.name,
      inviteType: detail.value.value,
    })
  },
  onConfirmTime(e){
    this.setData({
      showPopup: false,
      endTime: format(new Date(e.detail), 'YYYY-MM-DD hh:mm:ss')
    })
  },
  
  onConfirmObj(e){
    const {
      detail
    } = e
    if(this.data.canChangeObj){
      this.setData({
        objectId:detail.value.id,
        disObjName: detail.value.name
      })
    }
    this.setData({showPopup:false})
  },
  onChangePerm(e){
    this.setData({
      permissions: e.detail
    });
  },
  confirm(){
    const {
      count,
      objectId,
      permissions,
      inviteType,
      endTime,
    } = this.data

    let data = {count, objectId,permissions,inviteType,endTime}
    inviteApi.create(data).then((res)=>{
      wx.navigateBack()
    })

  }
})