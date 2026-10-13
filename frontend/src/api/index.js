import axios from 'axios'

const request = axios.create({ baseURL: '/api/v1' })

request.interceptors.response.use(
  (res) => {
    const data = res.data
    if (data.code === 200) return data.data
    return Promise.reject(new Error(data.message || '请求失败'))
  },
  (err) => Promise.reject(new Error(err.response?.data?.message || err.message || '请求失败')),
)

export default request
