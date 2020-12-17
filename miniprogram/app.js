import auth from './api/auth'

App({
  onLaunch: function () {
    // 检查token是否过期
    let token = wx.getStorageSync('token') || ""
    let refresh = wx.getStorageSync('refresh') || ""
    if (token){
      auth.verify({token}).then((res)=>{
        if ('detail' in res){
          // 尝试刷新token
          if (refresh){
            auth.refresh({refresh}).then((res)=>{
              if ('detail' in res){
                // 跳转登录页面
                console.log('to login page')
              }
              if ('access' in res){
                wx.setStorageSync('token', res.access)
              }
            })
          }
        }
      })
    } else {
      console.log('no token to login page!')
    }
  }
    
})