import { API_BASE_URL, DEFAULT_BUCKET, DEFAULT_REGION } from './request';

var COS = require('../sdk/cos-wx-sdk-v5.js')
var cos = new COS({
  getAuthorization: function (options, callback) {
      wx.request({
          url: API_BASE_URL+'api/auth/tmp_secret/',
          header: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + wx.getStorageSync('token')
          },
          success: function (result) {
              var data = result.data;
              var credentials = data && data.credentials;
              if (!data || !credentials) return console.error('credentials invalid');
              callback({
                  TmpSecretId: credentials.tmpSecretId,
                  TmpSecretKey: credentials.tmpSecretKey,
                  XCosSecurityToken: credentials.sessionToken,
                  StartTime: data.startTime,
                  ExpiredTime: data.expiredTime,
              });
          }
      });
  }
});
module.exports =  {
  cos,DEFAULT_BUCKET, DEFAULT_REGION
}