import { request } from './request';

export default {
  list: (params) => {
    return request('api/streams/', params, "GET")
  },
  create:(params, needJWT=true, needLoading=false) => { 
    return request('api/streams/', params, "POST") 
  },
  detail:(id, needJWT=true, needLoading=false) => { 
    return request('api/streams/'+id, {}, "GET") 
  },
  delete:(id, needJWT=true, needLoading=false) => { 
    return request('api/streams/'+id, {}, "DELETE") 
  },
  update: (data, needJWT = true, needLoading = false) => {
    return request('api/streams/' + data.id + '/', data, "PUT")
  },
}