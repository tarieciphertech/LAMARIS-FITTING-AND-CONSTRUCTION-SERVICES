const API_URL = (import.meta.env.VITE_API_URL || 'https://lamaris-api.onrender.com').replace(/\/$/, '')

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options)
  const contentType = response.headers.get('content-type') || ''
  const data = contentType.includes('application/json') ? await response.json() : await response.text()

  if (!response.ok) {
    throw new Error(typeof data === 'string' ? data : data.detail || 'Request failed')
  }
  return data
}

export function imageUrl(url) {
  if (!url) return ''
  if (/^https?:\/\//i.test(url)) return url
  return `${API_URL}${url.startsWith('/') ? '' : '/'}${url}`
}

export function fetchProperties(params = {}) {
  const query = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') query.set(key, value)
  })
  const suffix = query.toString() ? `?${query}` : ''
  return request(`/api/properties${suffix}`)
}

export function fetchProperty(id) {
  return request(`/api/properties/${encodeURIComponent(id)}`)
}

export { API_URL }
