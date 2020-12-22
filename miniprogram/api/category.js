import { request } from './request';

export default {
  list: (params) => {
    return request('api/categories/', params, "GET")
  },
  create:(params, needJWT=true, needLoading=false) => { 
    return request('api/categories/', params, "POST") 
  },
  detail:(id, needJWT=true, needLoading=false) => { 
    return request('api/devices/'+id+'', {}, "GET") 
  },
  update:(params, needJWT=true, needLoading=false) => { 
    return request('pi/charts/'+params.id+'', params, "PUT") 
  },
}