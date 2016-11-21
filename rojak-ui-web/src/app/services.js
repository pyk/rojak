import axios from 'axios'

export const ajax = axios.create({
  baseURL: '//api.rojak.id/v1',
  headers: {
    'Accept': 'application/json'
  }
})
