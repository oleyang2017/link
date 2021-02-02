import { request } from './request';

export default {
  list: (params) => {
    return request('api/devices/', params, "GET")
  },
  create:(params, needJWT=true, needLoading=false) => { 
    return request('api/devices/', params, "POST") 
  },
  detail:(id, needJWT=true, needLoading=false) => { 
    return request('api/devices/'+id+'', {}, "GET") 
  },
}