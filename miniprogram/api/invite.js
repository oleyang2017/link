import { request } from './request';

export default {
  list: (params) => {
    return request('/api/invite_links/', params, 'GET')
  },
  detail:(id) => { 
    return request(`/api/invite_links/${id}/`, {}, "GET") 
  },
  recordList: (id) => {
    return request(`/api/invite_links/${id}/record_list/`, params, 'GET')
  },
  create:(params) => { 
    return request('/api/invite_links/', params, "POST") 
  },
  update: (data) => {
    return request(`/api/invite_links/${data.id}/`, data, "PUT")
  },
  share: (data) => {
    return request(`/api/invite_links/${data.id}/share/`, data, "POST")
  },
}