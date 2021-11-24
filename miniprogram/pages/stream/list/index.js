import streamApi from '../../../api/stream'
import Dialog from '../../../external_components/dialog/dialog'

Page({
  data: {
    device: null,
    streamList: []
  },

  onLoad(options) {
    if (options.device){
      this.setData({
        device: options.device
      })
    }
  },

  onShow() {
    this.getStream()
  },

  getStream() {
    streamApi.list({device: this.data.device}).then((res) => {
      this.setData({
        streamList: res,
      })
    })
  },

  deleteStream(e){
    let name = e.currentTarget.dataset.name
    Dialog.confirm({
      title: '警告！',
      message: `确认删除 ‘${name} ’吗？\n删除后将清空该数据流下的所有历史数据,且不可恢复。`,
    })
    .then(() => {
      streamApi.delete(e.currentTarget.dataset.id).then(() => {
        let streamList = this.data.streamList
        streamList.splice(e.currentTarget.dataset.index, 1)
        this.setData({
          streamList
        })
      })
    })
  },
})