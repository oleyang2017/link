const API_BASE_URL = 'http://192.168.0.103:8000/'
// const API_BASE_URL = 'http://127.0.0.1:8000/'
// const API_BASE_URL = 'https://www.iotforfml.cn/'
const DEFAULT_BUCKET = 'iot-1253390446'
const DEFAULT_REGION = 'ap-shanghai'

const request = (url, data, method) => {
  let _url = API_BASE_URL + url
  let _header = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + wx.getStorageSync('token')
  }
  return new Promise((resolve, reject) => {
    wx.request({
      url: _url,
      method: method,
      data: data,
      header: _header,
      success(response) {
        if (response.statusCode == 500) {
          wx.showToast({
            title: '服务器错误！',
            duration: 2000
          })
        }
        resolve(response.data)
      },
      fail(error) {
        wx.showToast({
          title: '请求失败!',
          duration: 2000
        })
        reject(error)
      },
    })
  })
}

const requestWithFile = (url, data, method) => {
  let _url = API_BASE_URL + url
  let _header = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + wx.getStorageSync('token')
  }
  console.log(12313123)
  wx.uploadFile({
    url: _url,
    method: method,
    formData: data,
    header: _header,
    name: 'a',
    filePath: data.image,
    success(response) {
      if (response.statusCode == 500) {
        wx.showToast({
          title: '服务器错误！',
          duration: 2000
        })
      }
    },
    fail(error) {
      console.log(error)
      wx.showToast({
        title: '请求失败!',
        duration: 2000
      })
    },
  })
}

module.exports = {
  API_BASE_URL,
  DEFAULT_BUCKET,
  DEFAULT_REGION,
  request,
  requestWithFile,
}