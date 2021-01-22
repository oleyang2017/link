import category from '../../api/category'

Page({
  data: {
    category: [],
    showMask: false,
    popupHeight: 400
  },

  onLoad: function (options) {
    category.list({}).then((res)=>{
      this.setData({
        category: res,
        popupHeight: res.length * 36  > 260 ? '260px' : res.length * 36 + 'px'
      })
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  showMask:function(){
    console.log(!this.data.showMask)
    this.setData({
      showMask: !this.data.showMask
    })
  }
})