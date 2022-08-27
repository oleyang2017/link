import {
  request,
  requestWithFile
} from './request';

export default {
  list: (params) => {
    let url = "/api/devices/"
    if(params && "perms" in params){
      url = "/api/devices/?"
      for(let i = 0; i<params.perms.length; i++){
        url += `perms=${params.perms[i]}&`
      }
      url = url.substring(0, url.length-1)
      delete params.perms
    }
    return request(url, params, "GET")
  },
  create: (data) => {
    if (data.filePath) {
      let filePath = data.filePath
      delete data.filePath
      return requestWithFile('/api/devices/', data, filePath)
    }
    return request('/api/devices/', data, "POST")
  },
  detail: (id) => {
    return request(`/api/devices/${id}/`, {}, "GET")
  },
  update: (data) => {
    if (data.filePath) {
      let filePath = data.filePath
      delete data.filePath
      return requestWithFile(`/api/devices/${data.id}/upload/`, data, filePath)
    }
    return request(`/api/devices/${data.id}/`, data, "PUT")
  },
  getStreams:(id) =>{
    return request(`/api/devices/${id}/streams/`, {}, "GET")
  },
  getCharts:(id) =>{
    return request(`/api/devices/${id}/charts/`, {}, "GET")
  },
  getTriggers:(id) =>{
    return request(`/api/devices/${id}/triggers/`, {}, "GET")
  },
  getPerms:(id) =>{
    return request(`/api/devices/${id}/perms/`, {}, "GET")
  }
}