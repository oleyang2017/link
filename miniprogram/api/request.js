const API_BASE_URL = 'http://127.0.0.1:8000/'
import {jsonToHump, jsonToUnderline} from '../utils/convertVarName'

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
      data: jsonToUnderline(data),
      header: _header,
      success(response) {
        if (response.statusCode == 500) {
          wx.showToast({
            title: '服务器错误！',
            duration: 1000
          })
        }
        else if (response.statusCode == 400) {
          wx.showToast({
            title: '请求失败！',
            duration: 1000
          })
        }
        else if (response.statusCode == 401) {
          wx.navigateTo({
            url: '/pages/device/index',
          })
        }
        resolve(jsonToHump(response.data))
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

const requestWithFile = (url, formData, filePath) => {
  let _url = API_BASE_URL + url
  let _header = {
    'Authorization': 'Bearer ' + wx.getStorageSync('token')
  }
  wx.uploadFile({
    url: _url,
    formData: jsonToUnderline(formData),
    header: _header,
    name: 'image',
    filePath: filePath,
    success(response) {
      if (response.statusCode == 500) {
        wx.showToast({
          title: '服务器错误！',
          duration: 2000
        })
      }
    },
    fail(error) {
      wx.showToast({
        title: '请求失败!',
        duration: 2000
      })
    },
  })
}
module.exports = {
  API_BASE_URL,
  request,
  requestWithFile,
}