import {
  request
} from './request';

export default {
  list: (params) => {
    return request('/api/categories/', params, "GET")
  },
  create: (data) => {
    return request('/api/categories/', data, "POST")
  },
  detail: (id) => {
    return request('/api/categories/' + id + '/', {}, "GET")
  },
  update: (data) => {
    return request('/api/categories/' + data.id + '/', data, "PUT")
  },
  delete: (id) => {
    return request('/api/categories/' + id + '/', {}, "DELETE")
  },
  sort: (params) => {
    return request('/api/categories/sort/', params, "PUT")
  },
}