import {
  request
} from './request';

export default {
  list: (params) => {
    return request('api/categories/', params, "GET")
  },
  create: (data, needJWT = true, needLoading = false) => {
    return request('api/categories/', data, "POST")
  },
  detail: (id, needJWT = true, needLoading = false) => {
    return request('api/categories/' + id + '/', {}, "GET")
  },
  update: (data, needJWT = true, needLoading = false) => {
    return request('api/categories/' + data.id + '/', data, "PUT")
  },
  delete: (id, needJWT = true, needLoading = false) => {
    return request('api/categories/' + id + '/', {}, "DELETE")
  },
  sort: (params, needJWT = true, needLoading = false) => {
    return request('api/categories/sort/', params, "PUT")
  },
}