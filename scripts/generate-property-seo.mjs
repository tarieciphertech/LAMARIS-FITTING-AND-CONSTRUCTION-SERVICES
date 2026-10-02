import { mkdir, rm, writeFile } from 'node:fs/promises'
import { join } from 'node:path'

const API_URL = (process.env.VITE_API_URL || 'https://lamaris-api.onrender.com').replace(/\/$/, '')
const SITE_URL = 'https://lamaris.cyphertech.co.zw'
const BUSINESS_NAME = 'LamarIS Fitting and Construction Services'
const DEFAULT_IMAGE = `${SITE_URL}/lamaris-logo.svg`
const HUBS = [
  ['/property-for-sale-masvingo/', 'daily'],
  ['/houses-for-sale-masvingo/', 'daily'],
  ['/stands-for-sale-masvingo/', 'daily'],
  ['/land-for-sale-masvingo/', 'daily'],
  ['/commercial-property-masvingo/', 'weekly'],
  ['/construction-services-masvingo/', 'weekly'],
  ['/areas/zexcom/', 'weekly'],
  ['/areas/rujeko/', 'weekly'],
  ['/areas/victoria-ranch/', 'weekly'],
  ['/areas/kmp/', 'weekly'],
  ['/areas/pambudzi/', 'weekly'],
  ['/areas/westview-industrial/', 'weekly'],
  ['/services/construction/', 'monthly'],
  ['/services/renovations/', 'monthly'],
  ['/services/ceilings/', 'monthly'],
  ['/services/skimming/', 'monthly'],
  ['/services/painting/', 'monthly'],
  ['/services/fencing-welding/', 'monthly'],
  ['/services/plumbing/', 'monthly'],
  ['/services/plan-drawings/', 'monthly'],
]

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

async function fetchJson(url, attempt = 1) {
  try {
    const response = await fetch(url, {
      headers: { accept: 'application/json' },
      signal: AbortSignal.timeout(30000),
    })
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`)
    return await response.json()
  } catch (error) {
    if (attempt >= 3) throw error
    await sleep(attempt * 2000)
    return fetchJson(url, attempt + 1)
  }
}

const escapeHtml = (value = '') => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#39;')

const escapeXml = (value = '') => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&apos;')

const stripHtml = (value = '') => String(value).replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim()

function descriptionFor(property) {
  const facts = [
    property.property_type,
    property.location,
    property.stand_size,
    property.bedrooms != null ? `${property.bedrooms} bedrooms` : null,
    property.rooms != null ? `${property.rooms} rooms` : null,
    property.price,
  ].filter(Boolean)
  const extra = stripHtml(property.description || property.features || '')
  return (`${property.title} in ${property.location} — ${facts.join(', ')}. ${extra} View details and enquire with LamarIS in Masvingo, Zimbabwe.`).slice(0, 155)
}

function numericPrice(price) {
  if (!price) return null
  const match = String(price).replace(/,/g, '').match(/(?:US\\$|USD\\$|\\$)?\\s*(\\d+(?:\\.\\d+)?)/i)
  return match ? Number(match[1]) : null
}

function imageFor(property) {
  const image = [...(property.images || [])].sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0))[0]
  return image?.url || DEFAULT_IMAGE
}

function pageFor(property) {
  const url = `${SITE_URL}/properties/${property.slug}/`
  const description = descriptionFor(property)
  const image = imageFor(property)
  const price = numericPrice(property.price)
  const statusLabel = property.status === 'sold' ? 'Sold' : 'Available'
  const updated = property.updated_at || property.created_at
  const offer = price ? `,"offers":{"@type":"Offer","price":${price},"priceCurrency":"USD","availability":"${property.status === 'available' ? 'https://schema.org/InStock' : 'https://schema.org/SoldOut'}","url":"${url}"}` : ''
  const facts = [
    property.property_type ? `<dt>Property type</dt><dd>${escapeHtml(property.property_type)}</dd>` : '',
    property.location ? `<dt>Location</dt><dd>${escapeHtml(property.location)}</dd>` : '',
    property.stand_size ? `<dt>Size</dt><dd>${escapeHtml(property.stand_size)}</dd>` : '',
    property.bedrooms != null ? `<dt>Bedrooms</dt><dd>${property.bedrooms}</dd>` : '',
    property.rooms != null ? `<dt>Rooms</dt><dd>${property.rooms}</dd>` : '',
    property.paperwork_status ? `<dt>Paperwork</dt><dd>${escapeHtml(property.paperwork_status)}</dd>` : '',
    property.price ? `<dt>Price</dt><dd>${escapeHtml(property.price)}</dd>` : '',
    `<dt>Status</dt><dd>${statusLabel}</dd>`,
  ].filter(Boolean).join('')

  const schema = {
    '@context': 'https://schema.org',
    '@type': 'RealEstateListing',
    name: property.title,
    description,
    url,
    image: [image],
    dateModified: updated,
    seller: { '@type': 'RealEstateAgent', name: BUSINESS_NAME, url: SITE_URL, telephone: '+263778850189' },
    datePosted: property.created_at || undefined,
    address: { '@type': 'PostalAddress', addressLocality: property.location, addressCountry: 'ZW' },
    mainEntity: { '@type': 'Thing', name: property.title },
  }
  if (price) schema.offers = {
    '@type': 'Offer',
    price,
    priceCurrency: 'USD',
    availability: property.status === 'available' ? 'https://schema.org/InStock' : 'https://schema.org/SoldOut',
    url,
  }

  const breadcrumb = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: SITE_URL + '/' },
      { '@type': 'ListItem', position: 2, name: 'Properties', item: SITE_URL + '/property-for-sale-masvingo/' },
      { '@type': 'ListItem', position: 3, name: property.title, item: url },
    ],
  }

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${escapeHtml(property.title)} | ${escapeHtml(property.location)} | LamarIS</title>
<meta name="description" content="${escapeHtml(description)}">
<link rel="canonical" href="${url}">
<meta property="og:type" content="website">
<meta property="og:title" content="${escapeHtml(property.title)} | LamarIS">
<meta property="og:description" content="${escapeHtml(description)}">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${escapeHtml(image)}">
<meta property="og:image:alt" content="${escapeHtml(property.title)} in ${escapeHtml(property.location)}">
<meta property="og:site_name" content="LamarIS Fitting and Construction Services">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${escapeHtml(property.title)} | LamarIS">
<meta name="twitter:description" content="${escapeHtml(description)}">
<meta name="twitter:image" content="${escapeHtml(image)}">
<meta name="twitter:image:alt" content="${escapeHtml(property.title)} in ${escapeHtml(property.location)}">
<script type="application/ld+json">${JSON.stringify(schema)}</script>
<script type="application/ld+json">${JSON.stringify(breadcrumb)}</script>
<style>
:root{font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#182018;background:#f7f7f3}
body{margin:0}.wrap{max-width:920px;margin:auto;padding:28px 20px 70px}.brand{font-weight:800;letter-spacing:.08em;color:#182018;text-decoration:none}.crumbs{margin:24px 0;color:#667064;font-size:.9rem}.crumbs a{color:inherit}.hero{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(280px,.85fr);gap:32px;align-items:start}.hero img{width:100%;max-height:520px;object-fit:cover;border-radius:18px;background:#e6e8e1}.eyebrow{font-size:.78rem;font-weight:800;letter-spacing:.12em;color:#6d7a64}.status{display:inline-block;margin:12px 0;padding:6px 10px;border-radius:999px;background:#e4eadf;font-size:.78rem;font-weight:800}.price{font-size:2rem;font-weight:850;margin:18px 0}.facts{display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:1px solid #dfe3dc}.facts div{padding:12px 0;border-bottom:1px solid #dfe3dc}.facts strong{display:block}.facts span{color:#667064;font-size:.9rem}.cta{display:inline-block;margin-top:22px;padding:13px 18px;border-radius:10px;background:#182018;color:white;text-decoration:none;font-weight:800}.content{margin-top:36px;line-height:1.7}.content dl{display:grid;grid-template-columns:180px 1fr;gap:0;border-top:1px solid #dfe3dc}.content dt,.content dd{margin:0;padding:12px 0;border-bottom:1px solid #dfe3dc}.content dt{font-weight:700}.content dd{color:#4f594d}.footer{margin-top:48px;padding-top:24px;border-top:1px solid #dfe3dc;color:#667064;font-size:.9rem}@media(max-width:700px){.hero{grid-template-columns:1fr}.facts{grid-template-columns:1fr}.content dl{grid-template-columns:1fr}.content dt{padding-bottom:2px;border-bottom:0}.content dd{padding-top:2px}}
</style>
</head>
<body>
<main class="wrap">
<a class="brand" href="/">LAMARIS FITTING AND CONSTRUCTION SERVICES</a>
<nav aria-label="Primary"><a href="/property-for-sale-masvingo/">Property for Sale</a> · <a href="/land-for-sale-masvingo/">Land for Sale</a> · <a href="/construction-services-masvingo/">Construction Services</a></nav>
<nav class="crumbs"><a href="/">Home</a> / <a href="/property-for-sale-masvingo/">Properties</a> / ${escapeHtml(property.title)}</nav>
<section class="hero">
<div><img src="${escapeHtml(image)}" alt="${escapeHtml(property.title)} in ${escapeHtml(property.location)}"></div>
<div>
<div class="eyebrow">${escapeHtml(property.property_type || 'PROPERTY')} • MASVINGO &amp; BEYOND</div>
<div class="status">${statusLabel}</div>
<h1>${escapeHtml(property.title)}</h1>
<p>${escapeHtml(description)}</p>
<div class="price">${escapeHtml(property.price || 'Price on enquiry')}</div>
<div class="facts">
${property.location ? `<div><span>Location</span><strong>${escapeHtml(property.location)}</strong></div>` : ''}
${property.stand_size ? `<div><span>Size</span><strong>${escapeHtml(property.stand_size)}</strong></div>` : ''}
${property.bedrooms != null ? `<div><span>Bedrooms</span><strong>${property.bedrooms}</strong></div>` : ''}
${property.rooms != null ? `<div><span>Rooms</span><strong>${property.rooms}</strong></div>` : ''}
</div>
<a class="cta" href="https://wa.me/263778850189?text=${encodeURIComponent(`Hello LamarIS, I'm interested in the ${property.title} in ${property.location}. Is it still available?`)}">Enquire on WhatsApp</a>
</div>
</section>
<section class="content">
<h2>Property details</h2>
<dl>${facts}</dl>
${property.description ? `<h2>Description</h2><p>${escapeHtml(stripHtml(property.description))}</p>` : ''}
${property.features ? `<h2>Features</h2><p>${escapeHtml(stripHtml(property.features))}</p>` : ''}
<p>Contact LamarIS Fitting and Construction Services for viewing arrangements, availability and property guidance in Masvingo City and beyond.</p>
</section>
<footer class="footer">© 2026 LamarIS Fitting and Construction Services · <a href="/property-for-sale-masvingo/">View all property opportunities</a></footer>
</main>
</body>
</html>`
}

async function main() {
  const statuses = ['available', 'sold']
  const responses = await Promise.all(statuses.map((status) => fetchJson(`${API_URL}/api/properties?status=${status}&limit=100`)))
  const byId = new Map()
  responses.flat().forEach((property) => byId.set(property.id, property))
  const properties = [...byId.values()].filter((property) => property.slug)

  const outputDir = join(process.cwd(), 'public', 'properties')
  await rm(outputDir, { recursive: true, force: true })
  await mkdir(outputDir, { recursive: true })

  for (const property of properties) {
    const dir = join(outputDir, property.slug)
    await mkdir(dir, { recursive: true })
    await writeFile(join(dir, 'index.html'), pageFor(property), 'utf8')
  }

  const urls = [
    { path: '/', changefreq: 'weekly', lastmod: null },
    ...HUBS.map(([path, changefreq]) => ({ path, changefreq, lastmod: null })),
    ...properties.map((property) => ({
      path: `/properties/${property.slug}/`,
      changefreq: property.status === 'available' ? 'weekly' : 'monthly',
      lastmod: property.updated_at || property.created_at,
    })),
  ]

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(({ path, changefreq, lastmod }) => `  <url><loc>${escapeXml(SITE_URL + path)}</loc>${lastmod ? `<lastmod>${escapeXml(new Date(lastmod).toISOString())}</lastmod>` : ''}<changefreq>${changefreq}</changefreq></url>`).join('\n')}
</urlset>
`
  await writeFile(join(process.cwd(), 'public', 'sitemap.xml'), xml, 'utf8')
  console.log(`Generated ${properties.length} property SEO pages and sitemap entries from ${API_URL}`)
}

main().catch((error) => {
  console.error('Property SEO generation failed:', error)
  process.exit(1)
})
