import { request, requestWithFile } from './request';

export default {
  list: (params) => {
    return request('api/devices/', params, "GET")
  },
  create:(params, needJWT=true, needLoading=false) => { 
    return request('api/devices/', params, "POST") 
  },
  detail:(id, needJWT=true, needLoading=false) => { 
    return request('api/devices/'+id+'/', {}, "GET") 
  },
  update: (data, needJWT = true, needLoading = false) => {
    if (data.image){
      return requestWithFile('api/devices/' + data.id + '/', data, "PUT")
    }
    return request('api/devices/' + data.id + '/', data, "PUT")
  },
}