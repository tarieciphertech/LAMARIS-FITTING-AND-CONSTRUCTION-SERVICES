export const WHATSAPP = '263778850189'
export const PHONE = '0778850189'
export const PHONE_2 = '0714578421'
export const EMAIL = 'lifetrust.erwin90@gmail.com'

const githubImage = (name) =>
  `https://raw.githubusercontent.com/tarieciphertech/LAMARIS-FITTING-AND-CONSTRUCTION-SERVICES/main/${encodeURIComponent(name)}`

// Property/portfolio imagery from the LamarIS repository — not promotional posters.
export const images = {
  one: githubImage('Gemini_Generated_Image_5sj7395sj7395sj7.jpeg'),
  two: githubImage('Gemini_Generated_Image_b0ke6yb0ke6yb0ke.jpeg'),
  three: githubImage('Gemini_Generated_Image_e1ui2ae1ui2ae1ui.jpeg'),
  four: githubImage('Gemini_Generated_Image_ur003aur003aur00.jpeg'),
}

export const properties = [
  {
    id: 1,
    title: 'Residential Property Opportunity',
    type: 'Houses',
    location: 'Masvingo City',
    price: 'Price on enquiry',
    bedrooms: '—',
    standSize: 'Ask us',
    image: images.one,
    status: 'Available',
  },
  {
    id: 2,
    title: 'Residential Stand Opportunity',
    type: 'Residential Stands',
    location: 'Masvingo City & Beyond',
    price: 'Price on enquiry',
    bedrooms: '—',
    standSize: 'Ask us',
    image: images.two,
    status: 'Available',
  },
  {
    id: 3,
    title: 'Commercial Property Opportunity',
    type: 'Commercial Buildings',
    location: 'Masvingo City',
    price: 'Price on enquiry',
    bedrooms: '—',
    standSize: 'Ask us',
    image: images.three,
    status: 'Available',
  },
  {
    id: 4,
    title: 'Development Opportunity',
    type: 'Industrial Properties',
    location: 'Masvingo & surrounding areas',
    price: 'Price on enquiry',
    bedrooms: '—',
    standSize: 'Ask us',
    image: images.four,
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
