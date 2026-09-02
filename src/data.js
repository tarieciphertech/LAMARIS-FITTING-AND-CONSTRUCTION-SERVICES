export const WHATSAPP = '263778850189'
export const PHONE = '0778850189'
export const PHONE_2 = '0714578421'
export const EMAIL = 'lifetrust.erwin90@gmail.com'

const githubImage = (name) =>
  `https://raw.githubusercontent.com/tarieciphertech/LAMARIS-FITTING-AND-CONSTRUCTION-SERVICES/main/${encodeURIComponent(name)}`

export const images = {
  one: githubImage('WhatsApp Image 2026-09-02 at 08.28.08.jpeg'),
  two: githubImage('WhatsApp Image 2026-09-02 at 08.28.08 (1).jpeg'),
  three: githubImage('WhatsApp Image 2026-09-02 at 08.28.09.jpeg'),
}

export const properties = [
  {
    id: 1,
    title: 'Featured Property Opportunity',
    type: 'Residential Property',
    location: 'Masvingo City',
    price: 'Price on enquiry',
    bedrooms: '—',
    standSize: '—',
    image: images.one,
    status: 'Available',
  },
  {
    id: 2,
    title: 'Residential Stand',
    type: 'Residential Stand',
    location: 'Masvingo & surrounding areas',
    price: 'Price on enquiry',
    bedrooms: '—',
    standSize: 'Ask us',
    image: images.two,
    status: 'Available',
  },
  {
    id: 3,
    title: 'Property & Development Opportunity',
    type: 'Commercial / Development',
    location: 'Masvingo City & Beyond',
    price: 'Price on enquiry',
    bedrooms: '—',
    standSize: 'Ask us',
    image: images.three,
    status: 'Available',
  },
]

export const propertyTypes = [
  'Houses',
  'Residential Stands',
  'Commercial Buildings',
  'Commercial Stands',
  'Industrial Stands',
  'Industrial Properties',
]

export const constructionServices = [
  'Residential construction',
  'Commercial construction',
  'Renovations',
  'Ceilings',
  'Skimming',
  'Painting',
  'Fencing',
  'Welding',
  'Plumbing',
  'Plan drawings',
]
