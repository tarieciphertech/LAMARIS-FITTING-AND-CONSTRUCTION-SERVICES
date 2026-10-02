const API_URL = (import.meta.env.VITE_API_URL || 'https://lamaris-api.onrender.com').replace(/\/$/, '')

async function request(path, options = {}) {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), options.timeout || 10000)
  let response
  try {
    response = await fetch(`${API_URL}${path}`, { ...options, signal: options.signal || controller.signal })
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('The listings service took too long to respond.')
    throw error
  } finally {
    clearTimeout(timeout)
  }

  const contentType = response.headers.get('content-type') || ''
  const data = contentType.includes('application/json') ? await response.json() : await response.text()
  if (!response.ok) throw new Error(typeof data === 'string' ? data : data.detail || 'Request failed')
  return data
}

export function imageUrl(url) {
  if (!url) return ''
  if (/^https?:\/\//i.test(url)) return url
  return `${API_URL}${url.startsWith('/') ? '' : '/'}${url}`
}

const PROPERTY_CACHE_KEY = 'lamaris:available-properties:v1'
const PROPERTY_CACHE_TTL = 30 * 60 * 1000
const PROPERTY_STALE_TTL = 7 * 24 * 60 * 60 * 1000

function readPropertyCache() {
  try {
    const cached = JSON.parse(sessionStorage.getItem(PROPERTY_CACHE_KEY) || 'null')
    if (cached && Array.isArray(cached.data) && cached.timestamp) return cached
  } catch {}
  return null
}

function writePropertyCache(data) {
  try {
    sessionStorage.setItem(PROPERTY_CACHE_KEY, JSON.stringify({ timestamp: Date.now(), data }))
  } catch {}
}

export function fetchProperties(params = {}) {
  const query = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') query.set(key, value)
  })
  const suffix = query.toString() ? `?${query}` : ''
  const isAvailable = params.status === 'available' && Object.keys(params).length === 1
  const cached = isAvailable ? readPropertyCache() : null

  if (cached && Date.now() - cached.timestamp < PROPERTY_CACHE_TTL) {
    return Promise.resolve(cached.data)
  }

  return request(`/api/properties${suffix}`)
    .then((data) => {
      if (isAvailable && Array.isArray(data)) writePropertyCache(data)
      return data
    })
    .catch((error) => {
      if (isAvailable && cached && Date.now() - cached.timestamp < PROPERTY_STALE_TTL) return cached.data
      throw error
    })
}

export function fetchProperty(slug) {
  return request(`/api/properties/public/${encodeURIComponent(slug)}`)
}

export function submitEnquiry(payload) {
  return request('/api/enquiries', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export { API_URL }
