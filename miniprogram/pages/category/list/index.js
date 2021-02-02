import categoryApi from '../../../api/category'

Page({
  data: {
    category : [
         {id: "WgDWrDQJL4KbDAogERXLnZ", device_count: 1, name: "卧室", sequence: 0, create_time: "2020-12-21 21:25:12"}
        ,{id: "MyfsLeZiE6XUVwYwdpnDhh", device_count: 0, name: "厨房", sequence: 1, create_time: "2021-01-12 23:32:45"}
        ,{id: "MyfsLeZiE6XU1VwYwdpDhh", device_count: 0, name: "客厅", sequence: 1, create_time: "2021-01-12 23:32:45"}
        ,{id: "MyfsLeZiE6X11VwYwdpDhh", device_count: 0, name: "卫生间&浴室", sequence: 1, create_time: "2021-01-12 23:32:45"}
        ,{id: "Myfs1eZiE6X11VwYwdpDhh", device_count: 0, name: "书房", sequence: 1, create_time: "2021-01-12 23:32:45"}
        ,{id: "Myfs1eZiE6X11VwY4dpDhh", device_count: 0, name: "衣帽间", sequence: 1, create_time: "2021-01-12 23:32:45"}
        ,{id: "Myfs1eZiE6X11V4Y4dpDhh", device_count: 0, name: "保姆间", sequence: 1, create_time: "2021-01-12 23:32:45"}
        ,{id: "Myfs1eZiE6X11V4Y4d1Dhh", device_count: 0, name: "餐厅", sequence: 1, create_time: "2021-01-12 23:32:45"}
        ,{id: "Myfs1eZiE6X1174Y4d1Dhh", device_count: 0, name: "餐厅1", sequence: 1, create_time: "2021-01-12 23:32:45"}
      ]
  },
  onLoad: function (options) {
    // categoryApi.list({}).then((res)=>{
    //   this.setData({
    //     category: res,
    //   })
    // })
  },
  toDetail(e){
    console.log(e)
    wx.navigateTo({
      url: "/pages/category/detail/index?id=" + e.currentTarget.dataset.id,
    })
  },
  deleteCategory(e) {
    console.log(e)
  },
})