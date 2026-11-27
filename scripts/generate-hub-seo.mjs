import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { join } from 'node:path'

const SITE_URL = 'https://lamaris.cyphertech.co.zw'
const BUSINESS_NAME = 'LamarIS Fitting and Construction Services'
const WHATSAPP = '263778850189'

const HUBS = [
  {
    path: '/property-for-sale-masvingo/', kind: 'all',
    title: 'Property for Sale in Masvingo | Houses, Stands & Land | LamarIS',
    description: 'Explore houses, residential stands, land and commercial property opportunities in Masvingo, Zimbabwe. View current LamarIS listings and enquire directly.',
    heading: 'Property for Sale in Masvingo',
    intro: 'Explore property opportunities represented by LamarIS in Masvingo City and beyond. Browse available houses, stands, land and commercial properties, then contact the team to arrange a viewing or discuss your requirements.',
  },
  {
    path: '/houses-for-sale-masvingo/', kind: 'type', terms: ['house'],
    title: 'Houses for Sale in Masvingo | LamarIS Property Listings',
    description: 'Browse houses for sale in Masvingo and surrounding areas. Review available property details and contact LamarIS for viewing arrangements.',
    heading: 'Houses for Sale in Masvingo',
    intro: 'Browse house listings represented by LamarIS in Masvingo and surrounding areas. Each listing includes the available details supplied for that property. Contact the team to confirm current availability and arrange a viewing.',
  },
  {
    path: '/stands-for-sale-masvingo/', kind: 'type', terms: ['stand'],
    title: 'Stands for Sale in Masvingo | Residential & Commercial | LamarIS',
    description: 'Explore residential, commercial and development stands for sale in Masvingo and beyond. Contact LamarIS to confirm details and viewing arrangements.',
    heading: 'Stands for Sale in Masvingo',
    intro: 'Explore stand opportunities represented by LamarIS, including residential and commercial options where available. Review the published size, location and price information, then contact the team to confirm details before making a decision.',
  },
  {
    path: '/land-for-sale-masvingo/', kind: 'type', terms: ['land', 'hectare', 'plot'],
    title: 'Land for Sale in Masvingo & Zimbabwe | LamarIS',
    description: 'Browse land and plot opportunities represented by LamarIS in Masvingo and other locations in Zimbabwe. Enquire for current details and viewing arrangements.',
    heading: 'Land for Sale in Masvingo and Beyond',
    intro: 'View land and plot opportunities represented by LamarIS across Masvingo and other locations in Zimbabwe. Land sizes, locations and asking prices are shown where supplied. Contact the team to confirm availability and arrange further information.',
  },
  {
    path: '/commercial-property-masvingo/', kind: 'type', terms: ['commercial', 'industrial', 'warehouse', 'shop', 'business'],
    title: 'Commercial Property for Sale in Masvingo | LamarIS',
    description: 'Find commercial and industrial property opportunities in Masvingo and beyond. Browse LamarIS listings and enquire about viewing and property details.',
    heading: 'Commercial Property in Masvingo',
    intro: 'Explore commercial and industrial property opportunities represented by LamarIS. Listings may include commercial stands, buildings, warehouses and business premises. Contact the team to confirm each property’s current status and viewing arrangements.',
  },
  {
    path: '/construction-services-masvingo/', kind: 'service-index',
    title: 'Construction Services in Masvingo | LamarIS',
    description: 'LamarIS provides construction, renovations, ceilings, skimming, painting, fencing, welding, plumbing and plan drawing services in Masvingo.',
    heading: 'Construction Services in Masvingo',
    intro: 'LamarIS supports residential and commercial projects in Masvingo City and surrounding areas. Explore the available construction and fitting services below, then contact the team to discuss your project scope and requirements.',
  },
  {
    path: '/areas/zexcom/', kind: 'area', area: 'zexcom',
    title: 'Property in Zexcom, Masvingo | LamarIS',
    description: 'Explore property opportunities in Zexcom, Masvingo. View LamarIS listings and contact the team to confirm availability and viewing arrangements.',
    heading: 'Property in Zexcom, Masvingo',
    intro: 'This page brings together property opportunities represented by LamarIS in Zexcom, Masvingo. Check the current listings below and contact the team if you need further information or want to discuss a property search.',
  },
  {
    path: '/areas/rujeko/', kind: 'area', area: 'rujeko',
    title: 'Property in Rujeko, Masvingo | LamarIS',
    description: 'Browse houses, stands and other property opportunities in Rujeko, Masvingo. Enquire with LamarIS about current listings and viewings.',
    heading: 'Property in Rujeko, Masvingo',
    intro: 'Explore property opportunities represented by LamarIS in Rujeko, Masvingo. Listing details are provided where available. Contact the team to confirm current availability and arrange a viewing.',
  },
  {
    path: '/areas/victoria-ranch/', kind: 'area', area: 'victoria ranch',
    title: 'Property in Victoria Ranch, Masvingo | LamarIS',
    description: 'View property opportunities in Victoria Ranch, Masvingo, including available LamarIS listings. Contact the team for current details.',
    heading: 'Property in Victoria Ranch, Masvingo',
    intro: 'Browse LamarIS property opportunities in Victoria Ranch, Masvingo. Review the details shown for each current listing and contact the team to confirm availability or arrange a viewing.',
  },
  {
    path: '/areas/kmp/', kind: 'area', area: 'kmp',
    title: 'Property in KMP, Masvingo | LamarIS',
    description: 'Explore property opportunities in KMP, Masvingo. View available LamarIS listings and enquire about details and viewings.',
    heading: 'Property in KMP, Masvingo',
    intro: 'This page highlights property opportunities represented by LamarIS in KMP, Masvingo. Check the current listings below and contact the team for further information or viewing arrangements.',
  },
  {
    path: '/areas/pambudzi/', kind: 'area', area: 'pambudzi',
    title: 'Property in Pambudzi, Masvingo | LamarIS',
    description: 'Browse houses and other property opportunities in Pambudzi, Masvingo. Contact LamarIS to confirm listing details and viewings.',
    heading: 'Property in Pambudzi, Masvingo',
    intro: 'Explore property opportunities represented by LamarIS in Pambudzi, Masvingo. Available listing information is shown below. Contact the team to confirm the latest status and arrange a viewing.',
  },
  {
    path: '/areas/westview-industrial/', kind: 'area', area: 'westview industrial',
    title: 'Industrial Property in Westview Industrial, Masvingo | LamarIS',
    description: 'Explore commercial and industrial property opportunities in Westview Industrial, Masvingo. Enquire with LamarIS for current listing details.',
    heading: 'Property in Westview Industrial, Masvingo',
    intro: 'Browse commercial, industrial and development opportunities represented by LamarIS in Westview Industrial, Masvingo. Contact the team to confirm the details and current availability of any listing.',
  },
  {
    path: '/services/construction/', kind: 'service',
    title: 'Construction Services in Masvingo | LamarIS',
    description: 'Discuss residential and commercial construction projects in Masvingo with LamarIS Fitting and Construction Services.',
    heading: 'Construction Services in Masvingo',
    intro: 'LamarIS provides construction services for residential and commercial projects in Masvingo City and surrounding areas. Contact the team to discuss your project, location, scope, materials and timing.',
  },
  {
    path: '/services/renovations/', kind: 'service',
    title: 'Building Renovations in Masvingo | LamarIS',
    description: 'Talk to LamarIS about residential and commercial renovation projects in Masvingo and surrounding areas.',
    heading: 'Renovation Services in Masvingo',
    intro: 'LamarIS undertakes renovation work for residential and commercial spaces in Masvingo and surrounding areas. Get in touch to discuss the condition of the property, the work required and your project priorities.',
  },
  {
    path: '/services/ceilings/', kind: 'service',
    title: 'Ceiling Installation Services in Masvingo | LamarIS',
    description: 'Enquire about ceiling installation and related fitting work for residential and commercial spaces in Masvingo.',
    heading: 'Ceiling Services in Masvingo',
    intro: 'LamarIS offers ceiling services for residential and commercial spaces in Masvingo. Contact the team to discuss the type of space, ceiling requirements and the work you would like quoted.',
  },
  {
    path: '/services/skimming/', kind: 'service',
    title: 'Wall Skimming Services in Masvingo | LamarIS',
    description: 'Discuss wall skimming and surface preparation work with LamarIS in Masvingo and surrounding areas.',
    heading: 'Skimming Services in Masvingo',
    intro: 'LamarIS provides skimming services as part of its construction and fitting work in Masvingo. Contact the team to discuss the surfaces, property and finish required for your project.',
  },
  {
    path: '/services/painting/', kind: 'service',
    title: 'Painting Services in Masvingo | LamarIS',
    description: 'Enquire about interior and exterior painting work for residential and commercial properties in Masvingo.',
    heading: 'Painting Services in Masvingo',
    intro: 'LamarIS offers painting services for residential and commercial properties in Masvingo and surrounding areas. Get in touch to discuss the property, surfaces and scope of your painting project.',
  },
  {
    path: '/services/fencing-welding/', kind: 'service',
    title: 'Fencing & Welding Services in Masvingo | LamarIS',
    description: 'Contact LamarIS about fencing and welding requirements for properties and projects in Masvingo.',
    heading: 'Fencing and Welding in Masvingo',
    intro: 'LamarIS provides fencing and welding services for property and construction projects in Masvingo. Contact the team to describe the site, the work required and the details you would like assessed.',
  },
  {
    path: '/services/plumbing/', kind: 'service',
    title: 'Plumbing Services in Masvingo | LamarIS',
    description: 'Discuss plumbing work for residential and commercial properties with LamarIS in Masvingo.',
    heading: 'Plumbing Services in Masvingo',
    intro: 'LamarIS offers plumbing services for residential and commercial properties in Masvingo and surrounding areas. Contact the team to explain the plumbing work required and arrange a discussion about your project.',
  },
  {
    path: '/services/plan-drawings/', kind: 'service',
    title: 'Building Plan Drawings in Masvingo | LamarIS',
    description: 'Enquire about building plan drawing services for property and construction projects in Masvingo.',
    heading: 'Plan Drawing Services in Masvingo',
    intro: 'LamarIS lists plan drawing services among its construction and fitting offerings. Contact the team to discuss your project, the type of drawings required and the next steps.',
  },
]

const escapeHtml = (value = '') => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#39;')

const normalize = (value = '') => String(value).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()

function readMeta(html, expression) {
  const match = html.match(expression)
  return match ? match[1].replaceAll('&amp;', '&').replaceAll('&quot;', '"') : ''
}

async function readPropertyPages() {
  const sitemap = await readFile(join(process.cwd(), 'public', 'sitemap.xml'), 'utf8')
  const urls = [...sitemap.matchAll(/<loc>(https:\/\/lamaris\.cyphertech\.co\.zw\/properties\/[^<]+)<\/loc>/g)]
    .map((match) => match[1])

  const properties = []
  for (const url of urls) {
    const slug = url.split('/').filter(Boolean).at(-1)
    const file = join(process.cwd(), 'public', 'properties', slug, 'index.html')
    try {
      const html = await readFile(file, 'utf8')
      const jsonMatch = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)
      if (!jsonMatch) continue
      const schema = JSON.parse(jsonMatch[1])
      const statusMatch = html.match(/<div class="status">([^<]+)<\/div>/)
      const priceMatch = html.match(/<div class="price">([\s\S]*?)<\/div>/)
      properties.push({
        url,
        name: schema.name || slug,
        description: schema.description || '',
        location: schema.address?.addressLocality || '',
        image: Array.isArray(schema.image) ? schema.image[0] : schema.image,
        status: statusMatch ? statusMatch[1].trim() : 'Available',
        price: priceMatch ? priceMatch[1].replace(/<[^>]*>/g, '').trim() : 'Price on enquiry',
        typeText: (schema.description || '').split('—')[1] || '',
      })
    } catch (error) {
      console.warn('Could not read generated property page ' + file + ': ' + error.message)
    }
  }
  return properties
}

function matchesHub(hub, property) {
  if (property.status.toLowerCase() !== 'available') return false
  if (hub.kind === 'all') return true
  if (hub.kind === 'type') {
    const text = normalize(property.name + ' ' + property.description + ' ' + property.typeText)
    return hub.terms.some((term) => text.includes(normalize(term)))
  }
  if (hub.kind === 'area') {
    return normalize(property.location + ' ' + property.description).includes(normalize(hub.area))
  }
  return false
}

function propertyCard(property) {
  const image = property.image || SITE_URL + '/lamaris-logo.svg'
  return '<a class="property-card" href="' + escapeHtml(property.url) + '">' +
    '<img src="' + escapeHtml(image) + '" alt="' + escapeHtml(property.name) + '" loading="lazy">' +
    '<div class="property-copy"><span>' + escapeHtml(property.location || 'Zimbabwe') + '</span>' +
    '<h2>' + escapeHtml(property.name) + '</h2><p>' + escapeHtml(property.description) + '</p>' +
    '<strong>' + escapeHtml(property.price || 'Price on enquiry') + '</strong><span class="card-link">View property details →</span></div></a>'
}

function pageFor(hub, properties) {
  const related = HUBS.filter((item) => item.path !== hub.path && (hub.kind === 'service' || hub.kind === 'service-index'
    ? item.kind === 'service' || item.kind === 'service-index'
    : item.kind === 'all' || item.kind === 'type' || item.kind === 'area')).slice(0, 10)

  const listings = properties.filter((property) => matchesHub(hub, property))
  const listingSection = listings.length
    ? '<section class="section"><div class="section-heading"><div><span class="eyebrow">CURRENT LISTINGS</span><h2>Properties to explore</h2></div><span class="count">' + listings.length + ' available</span></div><div class="grid">' + listings.map(propertyCard).join('') + '</div></section>'
    : (hub.kind === 'service' || hub.kind === 'service-index'
      ? ''
      : '<section class="empty"><h2>No matching listings are published right now</h2><p>Property availability changes. Contact LamarIS to ask about current opportunities or to discuss what you are looking for.</p><a class="button" href="https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent('Hello LamarIS, I am enquiring about ' + hub.heading + '.') + '">Ask LamarIS on WhatsApp</a></section>')

  const serviceLinks = HUBS.filter((item) => item.kind === 'service')
    .map((item) => '<a class="service-link" href="' + item.path + '"><strong>' + escapeHtml(item.heading) + '</strong><span>' + escapeHtml(item.description) + '</span></a>').join('')

  const serviceSection = hub.kind === 'service-index'
    ? '<section class="section"><div class="section-heading"><div><span class="eyebrow">OUR SERVICES</span><h2>Explore construction and fitting services</h2></div></div><div class="service-grid">' + serviceLinks + '</div></section>'
    : ''

  const schema = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: hub.heading,
    description: hub.description,
    url: SITE_URL + hub.path,
    isPartOf: { '@type': 'WebSite', name: BUSINESS_NAME, url: SITE_URL + '/' },
    about: { '@type': 'Thing', name: hub.kind === 'service' || hub.kind === 'service-index' ? 'Construction and fitting services in Masvingo' : 'Property listings in Masvingo and Zimbabwe' },
  }
  const breadcrumb = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: SITE_URL + '/' },
      { '@type': 'ListItem', position: 2, name: hub.heading, item: SITE_URL + hub.path },
    ],
  }

  return '<!doctype html>\n<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<title>' + escapeHtml(hub.title) + '</title><meta name="description" content="' + escapeHtml(hub.description) + '">' +
    '<meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="' + SITE_URL + hub.path + '">' +
    '<meta property="og:type" content="website"><meta property="og:title" content="' + escapeHtml(hub.title) + '">' +
    '<meta property="og:description" content="' + escapeHtml(hub.description) + '"><meta property="og:url" content="' + SITE_URL + hub.path + '">' +
    '<meta property="og:image" content="' + SITE_URL + '/lamaris-logo.svg"><meta property="og:site_name" content="' + BUSINESS_NAME + '">' +
    '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="' + escapeHtml(hub.title) + '">' +
    '<meta name="twitter:description" content="' + escapeHtml(hub.description) + '">' +
    '<script type="application/ld+json">' + JSON.stringify(schema).replaceAll('</script>', '<\\/script>') + '</script>' +
    '<script type="application/ld+json">' + JSON.stringify(breadcrumb).replaceAll('</script>', '<\\/script>') + '</script>' +
    '<style>' +
    ':root{font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#182018;background:#f7f7f3;font-synthesis:none}' +
    '*{box-sizing:border-box}body{margin:0;line-height:1.6}.wrap{max-width:1120px;margin:auto;padding:26px 22px 72px}.top{display:flex;align-items:center;justify-content:space-between;gap:20px;padding-bottom:22px;border-bottom:1px solid #dfe3dc}.brand{font-weight:850;letter-spacing:.06em;color:#182018;text-decoration:none}.nav{display:flex;gap:18px;flex-wrap:wrap}.nav a,.crumbs a,.related a{color:#52634b}.crumbs{margin:26px 0;color:#687265;font-size:.9rem}.hero{padding:42px 0 34px;max-width:850px}.eyebrow{font-size:.75rem;font-weight:850;letter-spacing:.13em;color:#718064;text-transform:uppercase}.hero h1{font-size:clamp(2.2rem,5vw,3.8rem);line-height:1.08;letter-spacing:-.04em;margin:12px 0 18px}.hero p{font-size:1.12rem;color:#586254;max-width:780px}.button{display:inline-block;margin-top:14px;padding:12px 18px;background:#182018;color:#fff;border-radius:9px;text-decoration:none;font-weight:750}.section{padding:32px 0}.section-heading{display:flex;align-items:end;justify-content:space-between;gap:20px;margin-bottom:20px}.section-heading h2{font-size:1.8rem;margin:6px 0 0}.count{color:#687265;font-size:.9rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}.property-card{display:block;border:1px solid #dfe3dc;border-radius:15px;overflow:hidden;background:#fff;color:inherit;text-decoration:none;transition:transform .15s ease,box-shadow .15s ease}.property-card:hover{transform:translateY(-2px);box-shadow:0 12px 28px #18201814}.property-card img{width:100%;height:205px;object-fit:cover;background:#e8ebe4}.property-copy{padding:17px}.property-copy>span:first-child{font-size:.8rem;color:#687265}.property-copy h2{font-size:1.15rem;line-height:1.3;margin:7px 0}.property-copy p{font-size:.9rem;color:#687265;margin:0 0 12px}.property-copy strong{display:block;font-size:1.1rem}.card-link{display:block;margin-top:12px;color:#52634b;font-weight:750;font-size:.9rem}.empty{margin:28px 0;padding:26px;border-radius:14px;background:#e9eee5}.empty h2{margin:0 0 8px}.empty p{max-width:720px;color:#586254}.service-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}.service-link{display:block;padding:18px;border:1px solid #dfe3dc;border-radius:12px;background:#fff;color:inherit;text-decoration:none}.service-link strong,.service-link span{display:block}.service-link span{margin-top:7px;color:#687265;font-size:.9rem}.related{padding:26px 0;border-top:1px solid #dfe3dc;margin-top:30px}.related h2{font-size:1.2rem}.related ul{display:flex;gap:10px 20px;flex-wrap:wrap;padding:0;list-style:none}.contact{margin-top:34px;padding:25px;border-radius:14px;background:#182018;color:#fff}.contact p{color:#d6ded1}.contact a{color:#fff}.footer{padding-top:24px;margin-top:38px;border-top:1px solid #dfe3dc;color:#687265;font-size:.88rem}@media(max-width:680px){.top{align-items:flex-start;flex-direction:column}.nav{gap:12px}.hero{padding-top:30px}.section-heading{align-items:flex-start;flex-direction:column}}' +
    '</style></head><body><main class="wrap"><header class="top"><a class="brand" href="/">LAMARIS FITTING AND CONSTRUCTION SERVICES</a><nav class="nav" aria-label="Main navigation"><a href="/">Home</a><a href="/property-for-sale-masvingo/">Property</a><a href="/construction-services-masvingo/">Construction</a></nav></header>' +
    '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / ' + escapeHtml(hub.heading) + '</nav>' +
    '<section class="hero"><span class="eyebrow">MASVINGO CITY &amp; BEYOND</span><h1>' + escapeHtml(hub.heading) + '</h1><p>' + escapeHtml(hub.intro) + '</p>' +
    '<a class="button" href="https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent('Hello LamarIS, I would like to enquire about ' + hub.heading + '.') + '">Enquire on WhatsApp</a></section>' +
    listingSection + serviceSection +
    '<section class="related"><h2>Explore more from LamarIS</h2><ul>' + related.map((item) => '<li><a href="' + item.path + '">' + escapeHtml(item.heading) + '</a></li>').join('') + '</ul></section>' +
    '<section class="contact"><h2>Need help with your property or project?</h2><p>Contact LamarIS Fitting and Construction Services for current property information, viewing arrangements and construction enquiries in Masvingo and beyond.</p><a href="https://wa.me/' + WHATSAPP + '">WhatsApp 077 885 0189</a> · <a href="mailto:lifetrust.erwin90@gmail.com">Email LamarIS</a></section>' +
    '<footer class="footer">© 2026 ' + BUSINESS_NAME + ' · <a href="/">Return to LamarIS home</a></footer></main></body></html>'
}

async function main() {
  const properties = await readPropertyPages()
  for (const hub of HUBS) {
    const relative = hub.path.replace(/^\/|\/$/g, '')
    const output = join(process.cwd(), 'public', relative, 'index.html')
    await mkdir(join(process.cwd(), 'public', relative), { recursive: true })
    await writeFile(output, pageFor(hub, properties), 'utf8')
  }
  console.log('Generated ' + HUBS.length + ' crawlable LamarIS category, area and service pages from ' + properties.length + ' property SEO pages.')
}

main().catch((error) => {
  console.error('Hub SEO generation failed:', error)
  process.exit(1)
})
