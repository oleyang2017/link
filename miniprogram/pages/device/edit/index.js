import deviceApi from '../../../api/device'
import categoryApi from '../../../api/category'
import Dialog from '../../../external_components/dialog/dialog'

Page({

  /**
   * 页面的初始数据
   */
  data: {
    type: 'edit',
    show: false,
    categoryList: [],
    categoryIndex: 0,
    imageList: [{url: 'https://img2018.cnblogs.com/blog/1213309/201907/1213309-20190713160416264-229954616.gif'}]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    if (options.type){
      this.setData({
        type: options.type
      })
    }
    if (options.id){
      deviceApi.detail(options.id).then((res) => {
        this.setData({
          ...res
        })
      })
    }
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
  closePopup(){
    if(!this.data.show && this.data.categoryList.length == 0){
      this.getCategory()
    }
    this.setData({
      show: !this.data.show
    })
  },
  async getCategory() {
    let categoryList = await categoryApi.list()
    categoryList.forEach((item,index) => {
      item.text = item.name
      item.defaultIndex = item.id
      if(item.id == this.data.category){
        this.setData({
          categoryIndex: index
        })
      }
    });
    this.setData({
      categoryList,
    })
  },
  changeCagetory(e){
    this.setData({
      category: e.detail.value.id,
      category_name: e.detail.value.name,
      show: false,
    })
  },
  cancel(){
    this.setData({
      show: false,
    })
  },
  removeStream(e){
    console.log(e)
    let name = e.currentTarget.dataset.name
    Dialog.confirm({
      title: '警告！',
      message: `确认删除 ‘${name} ’吗？\n删除后将清空该数据流下的所有历史数据,且不可恢复。`,
    })
    .then(() => {
      // on confirm
    })
    .catch(() => {
      // on cancel
    });
  },
  removeChart(e){
    console.log(e)
    let name = e.currentTarget.dataset.name
    Dialog.confirm({
      title: '警告！',
      message: `确认删除 ‘${name} ’吗？`,
    })
    .then(() => {
      // on confirm
    })
    .catch(() => {
      // on cancel
    });
  }
})