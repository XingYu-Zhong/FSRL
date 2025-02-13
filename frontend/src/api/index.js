import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

export const getConfigs = async () => {
  const response = await api.get('/training/configs')
  return response.data
}

export const addConfig = async (configType, config) => {
  const response = await api.post(`/training/configs/${configType}`, config)
  return response.data
}

export const updateConfig = async (configType, configName, config) => {
  const response = await api.put(`/training/configs/${configType}/${configName}`, config)
  return response.data
}

export const deleteConfig = async (configType, configName) => {
  const response = await api.delete(`/training/configs/${configType}/${configName}`)
  return response.data
}

export const startTraining = async (config) => {
  const response = await api.post('/training/start', config)
  return response.data
} 