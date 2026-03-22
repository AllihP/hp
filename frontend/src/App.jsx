import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import { LangProvider } from './context/LangContext'
import { getProfile, getSkills, getCV, getArticles } from './hooks/useApi'
import Navbar from './components/Navbar'
import ScrollToTop from './components/ScrollToTop'
import Footer from './components/Footer'
import Contact from './components/Contact'
import Home from './pages/Home'
import About from './pages/About'
import CV from './pages/CV'
import Articles from './pages/Articles'
import ArticleDetail from './pages/ArticleDetail'
import './i18n/index'
import './styles/global.css'

const FALLBACK = {
  profile: {
    name_fr: 'Hilla Prince Bambé', name_en: 'Hilla Prince Bambé', name_ar: 'هيلا برانس بامبي',
    title_fr: "Ingénieur des Technologies d'Information",
    title_en: 'Information Technology Engineer',
    title_ar: 'مهندس تكنولوجيا المعلومات',
    bio_fr: "Directeur Technique chez KICEKO CONSULTANT. Jeune ambitieux, je serai un excellent atout pour votre institution notamment dans la gestion de vos projets.",
    bio_en: "Technical Director at KICEKO CONSULTANT. Young and ambitious, I will be a great asset to your institution, particularly in managing your projects.",
    bio_ar: "المدير التقني في شركة كيسيكو للاستشارات. شاب طموح، سأكون أصلاً ممتازاً لمؤسستكم.",
    email: 'hillaprincebambe@gmail.com', phone: '+235 60 92 87 48',
    instagram: 'https://www.instagram.com/prince_allih/',
    facebook: 'https://www.facebook.com/prince.sirius/',
    linkedin: '', github: '', twitter: '',
  },
  skills: [
    { id:1, name_fr:'UI et UX Design',    name_en:'UI & UX Design',    name_ar:'تصميم واجهة المستخدم', percentage:95, icon:'fa-pen-ruler' },
    { id:2, name_fr:'Conception Système', name_en:'System Design',     name_ar:'تصميم الأنظمة',        percentage:98, icon:'fa-diagram-project' },
    { id:3, name_fr:'Méthodes Agiles',    name_en:'Agile Methods',     name_ar:'المنهجيات الرشيقة',    percentage:70, icon:'fa-arrows-spin' },
    { id:4, name_fr:'Développement Web',  name_en:'Web Development',   name_ar:'تطوير الويب',          percentage:85, icon:'fa-code' },
    { id:5, name_fr:'Infrastructure GIS', name_en:'GIS Infrastructure',name_ar:'البنية التحتية GIS',   percentage:90, icon:'fa-map' },
    { id:6, name_fr:'DevOps & Cloud',     name_en:'DevOps & Cloud',    name_ar:'ديف أوبس والسحابة',    percentage:75, icon:'fa-cloud' },
  ],
  cvData: {
    education: [
      { id:1, title_fr:"Master en Technologies de l'Information", title_en:'Master in Information Technology', title_ar:'ماجستير في تكنولوجيا المعلومات', institution_fr:'SupMTI - Rabat, Maroc', institution_en:'SupMTI - Rabat, Morocco', institution_ar:'سوب إم تي آي - الرباط', year:'2018-2020', description_fr:"Diplôme d'ingénieur en Technologies de l'Information.", description_en:'Engineering degree in Information Technology.', description_ar:'درجة الهندسة في تكنولوجيا المعلومات.' },
      { id:2, title_fr:'Certificat en Maintenance PC', title_en:'Certificate in PC Maintenance', title_ar:'شهادة في صيانة الحاسوب', institution_fr:'Centre de Formation', institution_en:'Training Center', institution_ar:'مركز التدريب', year:'2016', description_fr:'', description_en:'', description_ar:'' },
      { id:3, title_fr:'Baccalauréat Scientifique', title_en:'Scientific High School Diploma', title_ar:'البكالوريا العلمية', institution_fr:"Lycée National de N'Djamena", institution_en:'National High School', institution_ar:'الثانوية الوطنية', year:'2014', description_fr:'', description_en:'', description_ar:'' },
    ],
    experience: [
      { id:1, title_fr:'Directeur Technique', title_en:'Technical Director', title_ar:'المدير التقني', company_fr:'KICEKO CONSULTANT', company_en:'KICEKO CONSULTANT', company_ar:'كيسيكو للاستشارات', period:'2022 - Présent', description_fr:'Direction technique. Projets BM, PNUD, ANLA, LWF, OXFAM, NIRAS, TCHADELEC.', description_en:'Technical direction. Projects WB, UNDP, ANLA, LWF, OXFAM, NIRAS.', description_ar:'الإدارة التقنية. مشاريع مع البنك الدولي واليونامي.' },
      { id:2, title_fr:"Ingénieur Systèmes d'Information", title_en:'Information Systems Engineer', title_ar:'مهندس نظم المعلومات', company_fr:'PNSN - Chad', company_en:'PNSN - Chad', company_ar:'البرنامج الوطني للصحة الرقمية', period:'2020 - 2022', description_fr:'Gestion de plateformes pour 500+ utilisateurs.', description_en:'Platform management for 500+ users.', description_ar:'إدارة المنصات لأكثر من 500 مستخدم.' },
    ],
    certifications: [
      { id:1, title_fr:'AWS Cloud Practitioner', title_en:'AWS Cloud Practitioner', title_ar:'شهادة AWS السحابية', issuer:'Amazon Web Services', year:'2023', icon:'fa-aws' },
      { id:2, title_fr:'Professional Scrum Master', title_en:'Professional Scrum Master', title_ar:'سكروم ماستر المحترف', issuer:'Scrum.org', year:'2022', icon:'fa-certificate' },
      { id:3, title_fr:'GIS Professional', title_en:'GIS Professional', title_ar:'متخصص GIS', issuer:'ESRI / QGIS Foundation', year:'2021', icon:'fa-map' },
    ],
  },
  articles: [
    { id:1, title_fr:'GitHub Actions : Guide Complet avec Exemples', title_en:'GitHub Actions: Complete Guide with Examples', title_ar:'GitHub Actions: دليل شامل', summary_fr:'Automatisez vos workflows CI/CD avec GitHub Actions.', summary_en:'Automate your CI/CD workflows with GitHub Actions.', summary_ar:'أتمتة سير عمل CI/CD.', content_fr:'', content_en:'', content_ar:'', icon:'fa-github', link:'#', category:'DevOps', read_time:12 },
    { id:2, title_fr:'Red Hat avec GitHub Actions', title_en:'Red Hat with GitHub Actions', title_ar:'Red Hat مع GitHub Actions', summary_fr:'Intégrez Red Hat dans vos pipelines CI/CD.', summary_en:'Integrate Red Hat into your CI/CD pipelines.', summary_ar:'دمج Red Hat في مسارات CI/CD.', content_fr:'', content_en:'', content_ar:'', icon:'fa-hat-cowboy', link:'#', category:'Linux', read_time:10 },
    { id:3, title_fr:"GitHub Actions et Azure DevOps", title_en:'GitHub Actions and Azure DevOps', title_ar:'GitHub Actions وAzure DevOps', summary_fr:"Guide d'intégration GitHub Actions + Azure.", summary_en:'Integration guide GitHub Actions + Azure.', summary_ar:'دليل التكامل مع Azure.', content_fr:'', content_en:'', content_ar:'', icon:'fa-cloud', link:'#', category:'Cloud', read_time:15 },
    { id:4, title_fr:'Infrastructure GIS avec PostGIS', title_en:'GIS Infrastructure with PostGIS', title_ar:'البنية التحتية GIS مع PostGIS', summary_fr:'PostGIS, GeoServer et OpenLayers en production.', summary_en:'PostGIS, GeoServer and OpenLayers in production.', summary_ar:'PostGIS وGeoServer في الإنتاج.', content_fr:'', content_en:'', content_ar:'', icon:'fa-map', link:'#', category:'GIS', read_time:18 },
    { id:5, title_fr:'Django REST Framework Avancé', title_en:'Advanced Django REST Framework', title_ar:'Django REST Framework المتقدم', summary_fr:"Construction d'une API REST robuste.", summary_en:'Building a robust REST API.', summary_ar:'بناء واجهة برمجة REST قوية.', content_fr:'', content_en:'', content_ar:'', icon:'fa-server', link:'#', category:'Backend', read_time:14 },
    { id:6, title_fr:"Intégration IA avec l'API Anthropic", title_en:'AI Integration with Anthropic API', title_ar:'تكامل الذكاء الاصطناعي مع Anthropic', summary_fr:'Intégrez Claude dans vos apps Django.', summary_en:'Integrate Claude into your Django apps.', summary_ar:'دمج Claude في تطبيقاتك.', content_fr:'', content_en:'', content_ar:'', icon:'fa-robot', link:'#', category:'AI', read_time:16 },
  ]
}

function LoadingScreen() {
  return (
    <div className="loading-screen">
      <div className="loading-hex" />
      <p style={{ color: 'var(--gold)', fontFamily: 'var(--font-display)', fontSize: '0.9rem', letterSpacing: '0.2em' }}>
        HPB PORTFOLIO
      </p>
    </div>
  )
}

function ParticleField() {
  return (
    <div className="particle-field" aria-hidden>
      {[...Array(20)].map((_, i) => (
        <div key={i} className="particle" style={{
          width:  `${Math.random() * 3 + 1}px`,
          height: `${Math.random() * 3 + 1}px`,
          left:   `${Math.random() * 100}%`,
          animationDuration: `${Math.random() * 15 + 10}s`,
          animationDelay:    `${Math.random() * 10}s`,
        }} />
      ))}
    </div>
  )
}

// ─────────────────────────────────────────────────────────────
// AppRoutes : composant ENFANT de BrowserRouter
// → useLocation() peut être appelé ici sans erreur
// ─────────────────────────────────────────────────────────────
function AppRoutes({ profile, skills, cvData, articles }) {
  const location = useLocation()
  const isArticleDetail =
    location.pathname.startsWith('/articles/') &&
    location.pathname.replace('/articles/', '').length > 0

  return (
    <>
      <ScrollToTop />
      <ParticleField />
      <div className="hex-bg" aria-hidden />
      <Navbar />
      <main>
        <Routes>
          <Route path="/"             element={<Home    profile={profile} />} />
          <Route path="/about"        element={<About   profile={profile} skills={skills} />} />
          <Route path="/cv"           element={<CV      cvData={cvData} />} />
          <Route path="/articles"     element={<Articles articles={articles} />} />
          <Route path="/articles/:id" element={<ArticleDetail />} />
        </Routes>
        {!isArticleDetail && <Contact profile={profile} />}
      </main>
      <Footer profile={profile} />
    </>
  )
}

// ─────────────────────────────────────────────────────────────
// AppContent : charge les données, puis rend BrowserRouter
// ─────────────────────────────────────────────────────────────
function AppContent() {
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const [pRes, sRes, cvRes, aRes] = await Promise.all([
          getProfile(), getSkills(), getCV(), getArticles()
        ])
        setData({
          profile:  pRes.data,
          skills:   sRes.data,
          cvData:   cvRes.data,
          articles: aRes.data,
        })
      } catch {
        setData(FALLBACK)
      } finally {
        setTimeout(() => setLoading(false), 800)
      }
    }
    load()
  }, [])

  if (loading) return <LoadingScreen />

  const { profile, skills, cvData, articles } = data || FALLBACK

  return (
    <BrowserRouter>
      <AppRoutes
        profile={profile}
        skills={skills}
        cvData={cvData}
        articles={articles}
      />
    </BrowserRouter>
  )
}

// ─────────────────────────────────────────────────────────────
// Point d'entrée
// ─────────────────────────────────────────────────────────────
export default function App() {
  return (
    <LangProvider>
      <AppContent />
    </LangProvider>
  )
}
