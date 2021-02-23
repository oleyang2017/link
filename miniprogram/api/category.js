import { request } from './request';

export default {
  list: (params) => {
    return request('api/categories/', params, "GET")
  },
  create:(params, needJWT=true, needLoading=false) => { 
    return request('api/categories/', params, "POST") 
  },
  detail:(id, needJWT=true, needLoading=false) => { 
    return request('api/categories/'+id, {}, "GET") 
  },
  update:(params, needJWT=true, needLoading=false) => { 
    return request('api/categories/'+params.id+'', params, "PUT") 
  },
  delete:(id, needJWT=true, needLoading=false) => { 
    return request('api/categories/'+id, {}, "DELETE") 
  },
  sort:(params, needJWT=true, needLoading=false) => { 
    return request('api/categories/sort/', params, "PUT") 
  },
}