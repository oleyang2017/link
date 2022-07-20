import { request } from './request';

export default { 
  verify: (params) => {
    return request('/api/auth/token/verify/', params, 'POST')
  },
  login: (params) => {
    return request('/api/auth/token/wx/', params, 'POST')
  },
  refresh: (params) => {
    return request('/api/auth/token/refresh/', params, 'POST')
  },
}