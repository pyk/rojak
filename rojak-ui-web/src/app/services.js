import axios from 'axios'

export const ajax = axios.create({
  baseURL: 'http://api.rojak.id/v1',
  headers: {
    'Accept': 'application/json'
  }
})
