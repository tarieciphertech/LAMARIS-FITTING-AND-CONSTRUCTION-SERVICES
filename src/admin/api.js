const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

async function request(path, options = {}) {
  const token = localStorage.getItem('lamaris_admin_token')
  const headers = new Headers(options.headers || {})
  if (token) headers.set('Authorization', `Bearer ${token}`)
  if (options.body && !(options.body instanceof FormData)) headers.set('Content-Type', 'application/json')

  const response = await fetch(`${API_URL}${path}`, { ...options, headers })
  const contentType = response.headers.get('content-type') || ''
  const data = contentType.includes('application/json') ? await response.json() : await response.text()

  if (!response.ok) {
    if (response.status === 401) localStorage.removeItem('lamaris_admin_token')
    throw new Error(typeof data === 'string' ? data : data.detail || 'Request failed')
  }
  return data
}

export const api = {
  properties: (params = '') => request(`/api/properties${params ? `?${params}` : ''}`),
  property: (id) => request(`/api/properties/${id}`),
  enquiry: (payload) => request('/api/enquiries', { method: 'POST', body: JSON.stringify(payload) }),
}

export const adminApi = {
  login: (email, password) => request('/api/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  me: () => request('/api/auth/me'),
  changePassword: (current_password, new_password) => request('/api/auth/change-password', { method: 'POST', body: JSON.stringify({ current_password, new_password }) }),
  logout: () => request('/api/auth/logout', { method: 'POST' }),
  properties: (params = '') => request(`/api/properties${params ? `?${params}` : ''}`),
  property: (id) => request(`/api/properties/${id}`),
  createProperty: (payload) => request('/api/properties', { method: 'POST', body: JSON.stringify(payload) }),
  updateProperty: (id, payload) => request(`/api/properties/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),
  archiveProperty: (id) => request(`/api/properties/${id}`, { method: 'DELETE' }),
  uploadPropertyImage: (propertyId, file, altText = '') => {
    const form = new FormData()
    form.append('file', file)
    const query = altText ? `?alt_text=${encodeURIComponent(altText)}` : ''
    return request(`/api/properties/${propertyId}/images/upload${query}`, { method: 'POST', body: form })
  },
  attachImage: (propertyId, url, altText = '') => request(`/api/properties/${propertyId}/images?url=${encodeURIComponent(url)}${altText ? `&alt_text=${encodeURIComponent(altText)}` : ''}`, { method: 'POST' }),
  deleteImage: (imageId) => request(`/api/properties/images/${imageId}`, { method: 'DELETE' }),
  reorderImages: (propertyId, imageIds) => request(`/api/properties/${propertyId}/images/reorder`, { method: 'POST', body: JSON.stringify(imageIds) }),
  enquiries: () => request('/api/enquiries'),
}

export { API_URL }
