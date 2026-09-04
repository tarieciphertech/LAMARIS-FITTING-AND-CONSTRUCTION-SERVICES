import { useEffect, useMemo, useState } from 'react'
import {
  ArrowRight,
  CheckCircle2,
  ChevronRight,
  Hammer,
  Home,
  Mail,
  MapPin,
  Menu,
  MessageCircle,
  Phone,
  Search,
  ShieldCheck,
  X,
} from 'lucide-react'
import { constructionServices, EMAIL, images, PHONE, PHONE_2, propertyTypes, WHATSAPP } from './data'
import { fetchProperties, imageUrl } from './api'

const whatsappUrl = (message = 'Hello Lamaris, I would like to enquire about a property.') =>
  `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(message)}`

const logoUrl = `${import.meta.env.BASE_URL}lamaris-logo.svg`

function Brand({ compact = false }) {
  return <span className={`brand ${compact ? 'brand-compact' : ''}`}><img src={logoUrl} alt="LAMARIS Fitting and Construction Services" /></span>
}

function App() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [filters, setFilters] = useState({ type: '', location: '' })
  const [properties, setProperties] = useState([])
  const [propertiesLoading, setPropertiesLoading] = useState(true)
  const [propertiesError, setPropertiesError] = useState('')

  useEffect(() => {
    let active = true
    setPropertiesLoading(true)
    fetchProperties({ status: 'available' })
      .then((items) => { if (active) setProperties(items) })
      .catch((error) => { if (active) setPropertiesError(error.message || 'Unable to load listings.') })
      .finally(() => { if (active) setPropertiesLoading(false) })
    return () => { active = false }
  }, [])

  const filteredProperties = useMemo(() => properties.filter((property) => {
    const typeMatch = !filters.type || property.property_type === filters.type
    const locationMatch = !filters.location || property.location.toLowerCase().includes(filters.location.toLowerCase())
    return typeMatch && locationMatch
  }), [filters, properties])

  return (
    <div className="site-shell">
      <div className="topbar">
        <div className="container topbar-inner">
          <span>Masvingo City &amp; Beyond</span>
          <span>Building Spaces. Delivering Trust.</span>
        </div>
      </div>

      <header className="navbar">
        <div className="container nav-inner">
          <a className="brand-link" href="#home" onClick={() => setMenuOpen(false)}><Brand /></a>
          <button className="menu-button" aria-label="Toggle navigation" onClick={() => setMenuOpen(!menuOpen)}>{menuOpen ? <X /> : <Menu />}</button>
          <nav className={`nav-links ${menuOpen ? 'open' : ''}`}>
            {['Home', 'Properties', 'Services', 'About', 'Contact'].map((item) => <a key={item} href={`#${item.toLowerCase()}`} onClick={() => setMenuOpen(false)}>{item}</a>)}
            <a className="nav-cta" href={whatsappUrl()} target="_blank" rel="noreferrer"><MessageCircle size={17} /> WhatsApp Us</a>
          </nav>
        </div>
      </header>

      <main>
        <section id="home" className="hero">
          <div className="hero-image" style={{ backgroundImage: `url("${images.one}")` }} />
          <div className="hero-overlay" />
          <div className="container hero-content">
            <div className="eyebrow">REAL ESTATE • CONSTRUCTION • FITTING</div>
            <h1>Find Your Property.<br /><span>Build Your Future.</span></h1>
            <p>Property sales and professional construction services in Masvingo and beyond — from finding the right property to turning your plans into a finished space.</p>
            <div className="hero-actions">
              <a className="button primary" href="#properties">Explore Properties <ArrowRight size={18} /></a>
              <a className="button light" href={whatsappUrl('Hello Lamaris, I would like help finding a property.')} target="_blank" rel="noreferrer"><MessageCircle size={18} /> Chat on WhatsApp</a>
            </div>
            <div className="hero-trust"><ShieldCheck size={18} /> Honest pricing • Reliable service • Skilled team</div>
          </div>
        </section>

        <section className="search-panel-wrap"><div className="container"><div className="search-panel"><div className="search-title"><Search size={21} /><div><strong>Find your next property</strong><small>Search Lamaris listings by type and location</small></div></div><select value={filters.type} onChange={(e) => setFilters({ ...filters, type: e.target.value })}><option value="">All property types</option>{propertyTypes.map((type) => <option key={type} value={type}>{type}</option>)}</select><input value={filters.location} onChange={(e) => setFilters({ ...filters, location: e.target.value })} placeholder="Location" /><a className="button primary" href="#properties">Search <ArrowRight size={17} /></a></div></div></section>

        <section id="properties" className="section"><div className="container"><div className="section-heading"><div><span className="kicker">PROPERTY OPPORTUNITIES</span><h2>Available Properties</h2></div><a href="#contact" className="text-link">Need something specific? <ChevronRight size={17} /></a></div>{propertiesLoading && <div className="empty-state">Loading current listings…</div>}{propertiesError && <div className="empty-state">We couldn't load the live listings right now. <a href={whatsappUrl()} target="_blank" rel="noreferrer">Ask LamarIS on WhatsApp.</a></div>}{!propertiesLoading && !propertiesError && <div className="property-grid">{filteredProperties.map((property) => <PropertyCard key={property.id} property={property} />)}</div>}{!propertiesLoading && !propertiesError && !filteredProperties.length && <div className="empty-state">No listings match those filters yet. <a href={whatsappUrl()} target="_blank" rel="noreferrer">Ask LamarIS directly.</a></div>}</div></section>

        <section id="services" className="section soft-section"><div className="container"><div className="section-heading centered"><span className="kicker">WHAT WE DO</span><h2>More Than Property Sales</h2><p>One trusted team for property opportunities and the work that turns them into valuable spaces.</p></div><div className="service-layout"><article className="service-feature"><div className="service-icon"><Home /></div><span className="kicker">REAL ESTATE</span><h3>Find the right property</h3><p>We help first-time buyers, investors, land buyers, companies and developers find property based on their requirements and budget.</p><ul><li>Houses &amp; residential stands</li><li>Commercial &amp; industrial property</li><li>Property sourcing for buyers</li><li>Viewing coordination</li></ul><a href="#properties" className="text-link">View properties <ArrowRight size={16} /></a></article><article className="service-feature dark-card"><div className="service-icon"><Hammer /></div><span className="kicker">CONSTRUCTION &amp; FITTING</span><h3>From property to finished space</h3><p>Already have a property? LamarIS can help turn your plans into reality with construction, renovations and specialist fitting services.</p><div className="service-tags">{constructionServices.map((service) => <span key={service}>{service}</span>)}</div><a href={whatsappUrl('Hello LamarIS, I would like to discuss a construction project.')} target="_blank" rel="noreferrer" className="text-link">Discuss a project <ArrowRight size={16} /></a></article></div></div></section>

        <section className="split-section"><div className="split-image" style={{ backgroundImage: `url("${images.two}")` }} /><div className="split-content"><span className="kicker">WHY LAMARIS</span><h2>Building Spaces.<br />Delivering Trust.</h2><p>LamarIS Fitting and Construction Services was established in 2025 with a simple approach: give clients a reliable path to property and construction without unnecessary complexity.</p><div className="check-grid"><div><CheckCircle2 /><strong>End-to-end service</strong><span>Property sales through construction.</span></div><div><CheckCircle2 /><strong>Honest pricing</strong><span>Clear, practical value for your budget.</span></div><div><CheckCircle2 /><strong>Reliable team</strong><span>Skilled people focused on quality work.</span></div><div><CheckCircle2 /><strong>Local expertise</strong><span>Focused on Masvingo and beyond.</span></div></div><a className="button primary" href="#about">Learn about LamarIS <ArrowRight size={18} /></a></div></section>

        <section id="about" className="section about-section"><div className="container about-grid"><div><span className="kicker">ABOUT US</span><h2>A practical partner for property and construction.</h2></div><div><p>LamarIS serves property owners, developers, buyers and businesses across Masvingo City and beyond. We sell properties, help clients find suitable opportunities, and provide construction and fitting services for residential and commercial projects.</p><p>For property paperwork, we provide guidance and facilitate referrals to affiliated legal practitioners where legal transfer work is required.</p><a href={whatsappUrl()} target="_blank" rel="noreferrer" className="text-link">Talk to our team <ArrowRight size={16} /></a></div></div></section>

        <section className="cta-section"><div className="container cta-inner"><div><span className="kicker">READY TO MOVE?</span><h2>Tell us what you're looking for.</h2><p>Whether you need a property or want to build, renovate or fit out a space, start with a WhatsApp enquiry.</p></div><a className="button white" href={whatsappUrl()} target="_blank" rel="noreferrer"><MessageCircle size={19} /> Start a WhatsApp Enquiry</a></div></section>

        <section id="contact" className="section contact-section"><div className="container"><div className="section-heading centered"><span className="kicker">GET IN TOUCH</span><h2>Let's talk about your next move.</h2></div><div className="contact-grid"><a href={whatsappUrl()} target="_blank" rel="noreferrer"><MessageCircle /><span><small>WhatsApp</small><strong>0778850189</strong></span></a><a href={`tel:${PHONE}`}><Phone /><span><small>Call us</small><strong>{PHONE} / {PHONE_2}</strong></span></a><a href={`mailto:${EMAIL}`}><Mail /><span><small>Email</small><strong>{EMAIL}</strong></span></a><div><MapPin /><span><small>Service area</small><strong>Masvingo City &amp; Beyond</strong></span></div></div></div></section>
      </main>

      <footer><div className="container footer-inner"><Brand compact /><p>© 2026 LamarIS Fitting and Construction Services. All rights reserved.</p><p className="disclaimer">Prices subject to change. Viewing by appointment.</p></div></footer>
    </div>
  )
}

function PropertyCard({ property }) {
  const image = property.images?.slice().sort((a, b) => a.sort_order - b.sort_order)[0]
  const message = `Hello LamarIS, I'm interested in the ${property.title} in ${property.location} listed on your website. Is it still available?`
  return <article className="property-card"><div className="property-image">{image ? <img src={imageUrl(image.url)} alt={image.alt_text || property.title} /> : <div className="property-image-placeholder"><Home size={34} /></div>}<span>{property.status}</span></div><div className="property-body"><small>{property.property_type}</small><h3>{property.title}</h3><div className="location"><MapPin size={15} /> {property.location}</div><div className="property-meta"><span><strong>{property.price || 'Price on enquiry'}</strong></span>{property.bedrooms != null && <span>{property.bedrooms} bedrooms</span>}{property.stand_size && <span>{property.stand_size}</span>}</div><div className="property-actions"><a href={whatsappUrl(message)} target="_blank" rel="noreferrer" className="button primary"><MessageCircle size={16} /> Enquire</a><a href={whatsappUrl(message)} target="_blank" rel="noreferrer" className="details-link">Ask for details <ChevronRight size={16} /></a></div></div></article>
}

export default App
