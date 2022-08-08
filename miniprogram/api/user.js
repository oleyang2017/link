import { request } from './request';

export default {
  getUserInfo: () => {
    return request('/api/user/', {}, "GET")
  }
}
