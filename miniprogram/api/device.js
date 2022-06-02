import {
  request,
  requestWithFile
} from './request';

export default {
  list: (params) => {
    return request('api/devices/', params, "GET")
  },
  create: (data) => {
    if (data.filePath) {
      let filePath = data.filePath
      delete data.filePath
      return requestWithFile('api/devices/', data, filePath)
    }
    return request('api/devices/', data, "POST")
  },
  detail: (id) => {
    return request(`api/devices/${id}/`, {}, "GET")
  },
  update: (data) => {
    if (data.filePath) {
      let filePath = data.filePath
      delete data.filePath
      return requestWithFile(`api/devices/${data.id}/upload/`, data, filePath)
    }
    return request(`api/devices/${data.id}/`, data, "PUT")
  },
}