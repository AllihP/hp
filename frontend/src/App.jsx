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
import ArticlePage from './pages/ArticlePage'
import './i18n/index'
import './styles/global.css'

const FALLBACK = {
  profile: {
    name_fr: 'Hilla Prince Bambé', name_en: 'Hilla Prince Bambé', name_ar: 'هيلا برانس بامبي',
    title_fr: 'CEO du groupe AllihTech | Consultant Chef de Projet',
    title_en: 'CEO of AllihTech Group | Project Management Consultant',
    title_ar: 'الرئيس التنفيذي لمجموعة AllihTech | مستشار إدارة المشاريع',
    bio_fr: "CEO du groupe AllihTech | Consultant Chef de Projet chez KICEKO. Jeune ambitieux, je serai un excellent atout pour votre institution notamment dans la gestion de vos projets en digitalisation et infrastructures numériques. Spécialisé en gestion de projets IT, transformation digitale, systèmes d'information géographique (SIG/GIS) et architecture cloud, je construis des ponts entre la vision stratégique et l'exécution opérationnelle.",
    bio_en: "CEO of AllihTech Group | Project Management Consultant at KICEKO. Young and ambitious, I will be an excellent asset to your institution, particularly in managing your digitalization and digital infrastructure projects. Specialized in IT project management, digital transformation, GIS/SIG, and cloud architecture, I bridge the gap between strategic vision and operational execution.",
    bio_ar: "الرئيس التنفيذي لمجموعة AllihTech | مستشار إدارة المشاريع في KICEKO. شاب طموح، سأكون أصلاً ممتازاً لمؤسستكم، لا سيما في إدارة مشاريعكم في مجال الرقمنة والبنية التحتية الرقمية. متخصص في إدارة مشاريع تكنولوجيا المعلومات والتحول الرقمي ونظم المعلومات الجغرافية، أبني جسراً بين الرؤية الاستراتيجية والتنفيذ الميداني.",
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
      {
        id:1,
        title_fr:"Master en Technologies de l'Information", title_en:'Master in Information Technology', title_ar:'ماجستير في تكنولوجيا المعلومات',
        institution_fr:'SupMTI - Rabat, Maroc', institution_en:'SupMTI - Rabat, Morocco', institution_ar:'سوب إم تي آي - الرباط، المغرب',
        year:'2017-2022',
        description_fr:"Diplôme d'ingénieur en Technologies de l'Information avec double spécialisation en systèmes d'information géographique (SIG/GIS) et architecture logicielle. Formation approfondie en développement web full-stack, méthodes agiles (Scrum, Kanban), bases de données spatiales (PostGIS), cartographie numérique et déploiement cloud. Mémoire de fin d'études axé sur la digitalisation des services publics en Afrique subsaharienne.",
        description_en:"Engineering degree in Information Technology with dual specialization in Geographic Information Systems (GIS/SIG) and software architecture. Comprehensive training in full-stack web development, agile methodologies (Scrum, Kanban), spatial databases (PostGIS), digital mapping, and cloud deployment. Thesis focused on digitalization of public services in sub-Saharan Africa.",
        description_ar:"درجة هندسة في تكنولوجيا المعلومات مع تخصص مزدوج في نظم المعلومات الجغرافية وهندسة البرمجيات. تدريب شامل في تطوير الويب الكامل، المنهجيات الرشيقة، قواعد البيانات المكانية والنشر السحابي.",
      },
      {
        id:2,
        title_fr:'Certificat en Maintenance PC', title_en:'Certificate in PC Maintenance', title_ar:'شهادة في صيانة الحاسوب',
        institution_fr:'Centre de Formation Informatique', institution_en:'IT Training Center', institution_ar:'مركز التدريب على تكنولوجيا المعلومات',
        year:'2016',
        description_fr:"Formation certifiante couvrant le diagnostic, la maintenance préventive et corrective du matériel informatique, la configuration des réseaux locaux et l'installation de systèmes d'exploitation Windows et Linux.",
        description_en:'Certified training covering diagnosis, preventive and corrective maintenance of IT hardware, local network configuration, and installation of Windows and Linux operating systems.',
        description_ar:'تدريب معتمد يغطي تشخيص وصيانة أجهزة تكنولوجيا المعلومات وإعداد الشبكات المحلية وتثبيت أنظمة التشغيل.',
      },
      {
        id:3,
        title_fr:'Baccalauréat Scientifique', title_en:'Scientific High School Diploma', title_ar:'البكالوريا العلمية',
        institution_fr:"Lycée National de N'Djamena", institution_en:"National High School of N'Djamena", institution_ar:'الثانوية الوطنية بنجامينا',
        year:'2014',
        description_fr:"Obtention du baccalauréat série scientifique avec mention. Solide fondation en mathématiques, physique et sciences naturelles, posant les bases d'un parcours d'ingénieur.",
        description_en:'Obtained the scientific baccalaureate with honors. Strong foundation in mathematics, physics, and natural sciences, laying the groundwork for an engineering career.',
        description_ar:'الحصول على شهادة البكالوريا العلمية بامتياز. أساس قوي في الرياضيات والفيزياء والعلوم الطبيعية.',
      },
    ],
    experience: [
      {
        id:3,
        title_fr:'CEO & Fondateur du Groupe', title_en:'Group CEO & Founder', title_ar:'الرئيس التنفيذي والمؤسس للمجموعة',
        company_fr:"AllihTech Group - N'Djamena, Tchad", company_en:"AllihTech Group - N'Djamena, Chad", company_ar:'مجموعة AllihTech - نجامينا، تشاد',
        period:'2022 - Présent',
        description_fr:"Fondation et direction générale du groupe AllihTech, entreprise tchadienne spécialisée en digitalisation, développement logiciel, infrastructure numérique et conseil IT pour les secteurs public et privé en Afrique centrale. Définition de la vision stratégique, management d'une équipe pluridisciplinaire, pilotage commercial et développement de partenariats stratégiques pour accélérer la transformation numérique au Tchad.",
        description_en:"Founded and lead AllihTech Group, a Chadian company specializing in digitalization, software development, digital infrastructure, and IT consulting for public and private sectors across Central Africa. Defined strategic vision, managed a multidisciplinary team, drove business development, and built strategic partnerships to accelerate digital transformation in Chad.",
        description_ar:'تأسيس وقيادة مجموعة AllihTech، شركة تشادية متخصصة في الرقمنة وتطوير البرمجيات والبنية التحتية الرقمية. تحديد الرؤية الاستراتيجية وإدارة فريق متعدد التخصصات وبناء شراكات لتسريع التحول الرقمي في تشاد.',
      },
      {
        id:1,
        title_fr:'Consultant Chef de Projet', title_en:'Project Management Consultant', title_ar:'مستشار إدارة المشاريع',
        company_fr:"KICEKO CONSULTANT - N'Djamena", company_en:"KICEKO CONSULTANT - N'Djamena", company_ar:'كيسيكو للاستشارات - نجامينا',
        period:'Janvier 2026 - Présent',
        description_fr:"Pilotage de missions de conseil en gestion de projets IT, digitalisation et développement d'infrastructures numériques pour des clients institutionnels et privés. Coordination de projets d'envergure avec des partenaires internationaux : Banque Mondiale, PNUD, ANLA, LWF, OXFAM, NIRAS. Définition des cadres PMO, rédaction de TDR, suivi budgétaire, reporting et conduite du changement organisationnel.",
        description_en:"Leading IT project management consulting missions covering digitalization and digital infrastructure for institutional and private clients. Coordinating large-scale projects with international partners: World Bank, UNDP, ANLA, LWF, OXFAM, NIRAS. Defining PMO frameworks, drafting ToRs, budget tracking, reporting, and change management.",
        description_ar:'قيادة مهام استشارية في إدارة مشاريع تكنولوجيا المعلومات والرقمنة لعملاء مؤسسيين وخاصين. تنسيق مشاريع مع شركاء دوليين: البنك الدولي، UNDP، ANLA، LWF، OXFAM، NIRAS.',
      },
      {
        id:2,
        title_fr:"Ingénieur Systèmes d'Information", title_en:'Information Systems Engineer', title_ar:'مهندس نظم المعلومات',
        company_fr:'Programme National Santé Numérique (PNSN)', company_en:'National Digital Health Program (PNSN)', company_ar:'البرنامج الوطني للصحة الرقمية',
        period:'Février 2025 - Juillet 2025',
        description_fr:"Conception, déploiement et administration de plateformes numériques de santé pour plus de 500 utilisateurs répartis dans les régions du Tchad. Intégration des systèmes DHIS2, OpenMRS et tableaux de bord analytiques. Coordination avec les ministères de la Santé et de la Transition Numérique et les partenaires internationaux (Banque Mondiale, PNUD, UNICEF).",
        description_en:"Design, deployment, and administration of digital health platforms for 500+ users across Chad's regions. Integration of DHIS2, OpenMRS systems, and analytical dashboards. Coordination with Ministries of Health and Digital Transition, and international partners (World Bank, UNDP, UNICEF).",
        description_ar:'تصميم ونشر وإدارة منصات الصحة الرقمية لأكثر من 500 مستخدم. دمج أنظمة DHIS2 وOpenMRS. التنسيق مع الوزارات والشركاء الدوليين.',
      },
    ],
    certifications: [
      { id:1, title_fr:'AWS Cloud Practitioner', title_en:'AWS Cloud Practitioner', title_ar:'شهادة AWS السحابية', issuer:'Amazon Web Services', year:'2023', icon:'fa-aws' },
      { id:2, title_fr:'Professional Scrum Master', title_en:'Professional Scrum Master', title_ar:'سكروم ماستر المحترف', issuer:'Scrum.org', year:'2022', icon:'fa-certificate' },
      { id:3, title_fr:'GIS Professional', title_en:'GIS Professional', title_ar:'متخصص GIS', issuer:'ESRI / QGIS Foundation', year:'2021', icon:'fa-map' },
    ],
  },
  articles: [
    { id:1, title_fr:'GitHub Actions : Guide Complet avec Exemples', title_en:'GitHub Actions: Complete Guide with Examples', title_ar:'GitHub Actions: دليل شامل', summary_fr:'Automatisez vos workflows CI/CD avec GitHub Actions.', summary_en:'Automate your CI/CD workflows with GitHub Actions.', summary_ar:'أتمتة سير عمل CI/CD.', icon:'fa-github', link:'#', category:'DevOps', read_time:12 },
    { id:2, title_fr:'Red Hat avec GitHub Actions', title_en:'Red Hat with GitHub Actions', title_ar:'Red Hat مع GitHub Actions', summary_fr:'Intégrez Red Hat dans vos pipelines CI/CD.', summary_en:'Integrate Red Hat into your CI/CD pipelines.', summary_ar:'دمج Red Hat في مسارات CI/CD.', icon:'fa-hat-cowboy', link:'#', category:'Linux', read_time:10 },
    { id:3, title_fr:"GitHub Actions et Azure DevOps", title_en:'GitHub Actions and Azure DevOps', title_ar:'GitHub Actions وAzure DevOps', summary_fr:"Guide d'intégration GitHub Actions + Azure.", summary_en:'Integration guide GitHub Actions + Azure.', summary_ar:'دليل التكامل مع Azure.', icon:'fa-cloud', link:'#', category:'Cloud', read_time:15 },
    { id:4, title_fr:'Infrastructure GIS avec PostGIS', title_en:'GIS Infrastructure with PostGIS', title_ar:'البنية التحتية GIS مع PostGIS', summary_fr:'PostGIS, GeoServer et OpenLayers en production.', summary_en:'PostGIS, GeoServer and OpenLayers in production.', summary_ar:'PostGIS وGeoServer في الإنتاج.', icon:'fa-map', link:'#', category:'GIS', read_time:18 },
    { id:5, title_fr:'Django REST Framework Avancé', title_en:'Advanced Django REST Framework', title_ar:'Django REST Framework المتقدم', summary_fr:"Construction d'une API REST robuste.", summary_en:'Building a robust REST API.', summary_ar:'بناء واجهة برمجة REST قوية.', icon:'fa-server', link:'#', category:'Backend', read_time:14 },
    { id:6, title_fr:"Intégration IA avec l'API Anthropic", title_en:'AI Integration with Anthropic API', title_ar:'تكامل الذكاء الاصطناعي مع Anthropic', summary_fr:'Intégrez Claude dans vos apps Django.', summary_en:'Integrate Claude into your Django apps.', summary_ar:'دمج Claude في تطبيقاتك.', icon:'fa-robot', link:'#', category:'AI', read_time:16 },
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
          <Route path="/articles/:id" element={<ArticlePage />} />
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
