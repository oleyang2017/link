import inviteApi from '../../../api/invite';
import Dialog from '@vant/weapp//dialog/dialog';

Page({
  data: {
    canShare: true,
  },

  onLoad(options) {
    this.setData({
      ...options
    })
    this.getInviteInfo(options.id)
  },

  getInviteInfo(id) {
    inviteApi.detail(id).then((res) => {
      let now = new Date()
      if (!res.enable || (res.count > 0 && res.count <= res.invitedCount) || (res.endTime && new Date(res.endTime) < now)) {
        res.canShare = false
      } else {
        res.canShare = true
      }
      this.setData({
        ...res
      })
    })
  },
  close() {
    Dialog.confirm({
        message: '关闭链接后，已分享出去的链接将不可再接受邀请，且不可再打开',
      })
      .then(() => {
        inviteApi.update({
          id: this.data.id,
          enable: false,
        }).then((res) => {
          this.setData({
            ...res
          })
        })
      })
  },

  onShareAppMessage(e) {
    return {
      title: this.data.inviteType == 'device' ? '分享设备给你' : '邀请你加入群组',
      path: `/pages/invite/share/index?id=${this.data.id}&type=share&code=${this.data.code}`,
      imageUrl: '/static/images/share.png'
    }
  }
})