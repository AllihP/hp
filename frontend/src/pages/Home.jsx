import { useState, useEffect, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import { useLang } from '../context/LangContext'
import { getField } from '../hooks/useApi'
import hillaImg from '../assets/hilla.png'
import './Home.css'

const ROLES_FR = ['Analyste & Concepteur', 'Project Manager', 'Ingénieur DevOps', 'Développeur Full-Stack', 'Spécialiste GIS', 'Designer UI/UX']
const ROLES_EN = ['Analyst & Designer', 'Project Manager', 'DevOps Engineer', 'Full-Stack Developer', 'GIS Specialist', 'UI/UX Designer']
const ROLES_AR = ['محلل ومصمم', 'مدير مشاريع', 'مهندس ديف أوبس', 'مطور متكامل', 'متخصص GIS', 'مصمم UI/UX']
const ROLES = { fr: ROLES_FR, en: ROLES_EN, ar: ROLES_AR }

const SKILLS_FR = ['Analyste et Concepteur', 'Project management', 'Ingénieur DevOps', 'Développeur Full-Stack', 'Spécialiste GIS & SIG', 'Designer UI/UX']
const SKILLS_EN = ['Analyst and Designer', 'Project Management', 'DevOps Engineer', 'Full-Stack Developer', 'GIS & SIG Specialist', 'UI/UX Designer']
const SKILLS_AR = ['محلل ومصمم أنظمة', 'إدارة المشاريع', 'مهندس ديف أوبس', 'مطور متكامل', 'متخصص GIS و SIG', 'مصمم واجهات']
const SKILLS = { fr: SKILLS_FR, en: SKILLS_EN, ar: SKILLS_AR }

export default function Home({ profile }) {
  const { t } = useTranslation()
  const { lang, isRTL } = useLang()
  const [roleIdx, setRoleIdx] = useState(0)
  const [displayed, setDisplayed] = useState('')
  const [typing, setTyping] = useState(true)
  const [visible, setVisible] = useState(false)
  const intervalRef = useRef(null)
  const roles = ROLES[lang] || ROLES_FR
  const skills = SKILLS[lang] || SKILLS_FR

  // Typewriter effect
  useEffect(() => {
    const currentRole = roles[roleIdx]
    if (typing) {
      let i = 0
      intervalRef.current = setInterval(() => {
        setDisplayed(currentRole.slice(0, i + 1))
        i++
        if (i >= currentRole.length) { clearInterval(intervalRef.current); setTimeout(() => setTyping(false), 1800) }
      }, 60)
    } else {
      let i = currentRole.length
      intervalRef.current = setInterval(() => {
        setDisplayed(currentRole.slice(0, i - 1))
        i--
        if (i <= 0) { clearInterval(intervalRef.current); setRoleIdx(r => (r + 1) % roles.length); setTyping(true) }
      }, 35)
    }
    return () => clearInterval(intervalRef.current)
  }, [roleIdx, typing, lang])

  useEffect(() => { setTimeout(() => setVisible(true), 100) }, [])

  const name = profile ? getField(profile, lang, 'name') : 'Hilla Prince Bambé'
  const bio = profile ? getField(profile, lang, 'bio') : ''

  const socials = [
    { icon: 'fab fa-instagram', url: profile?.instagram || '#' },
    { icon: 'fab fa-twitter', url: profile?.twitter || '#' },
    { icon: 'fab fa-facebook-f', url: profile?.facebook || '#' },
    { icon: 'fab fa-linkedin-in', url: profile?.linkedin || '#' },
    { icon: 'fab fa-github', url: profile?.github || '#' },
  ]

  return (
    <section className={`home section ${isRTL ? 'rtl' : ''} ${visible ? 'visible' : ''}`} id="home">
      {/* Animated hexagons */}
      <div className="home__hexagons" aria-hidden>
        {[...Array(6)].map((_, i) => (
          <div key={i} className={`hex hex--${i + 1}`} />
        ))}
      </div>

      <div className="home__content">
        <div className="home__text">
          <span className="home__greeting">{t('hero.greeting')}</span>
          <h1 className="home__name">
            {t('hero.iam')} <span className="gold">{name}</span>
          </h1>
          <div className="home__role">
            <span className="role-cursor">{'< '}</span>
            <span className="role-text">{displayed}</span>
            <span className="role-cursor blink">{' />'}</span>
          </div>
          {bio && <p className="home__bio">{bio}</p>}
          <ul className="home__skills">
            {skills.map((s, i) => (
              <li key={i} style={{ animationDelay: `${0.3 + i * 0.1}s` }}>
                <i className="fas fa-chevron-right" />
                {s}
              </li>
            ))}
          </ul>
          <div className="home__actions">
            <a href="/about" className="btn-gold">
              {t('about.hire')} <i className="fas fa-arrow-right" />
            </a>
            <div className="home__socials">
              {socials.map((s, i) => (
                <a key={i} href={s.url} target="_blank" rel="noreferrer">
                  <i className={s.icon} />
                </a>
              ))}
            </div>
          </div>
        </div>

        <div className="home__image-wrap">
          <div className="home__image-hex">
            <div className="hex-ring hex-ring--1" />
            <div className="hex-ring hex-ring--2" />
            <div className="hex-ring hex-ring--3" />
            <div className="home__image-inner">
              <img src={hillaImg} alt="Hilla Prince Bambé" className="home__img" />
            </div>
          </div>
          {/* Floating stats */}
          <div className="home__stat home__stat--1">
            <span className="stat-num">5+</span>
            <span className="stat-label">Années<br/>d'expérience</span>
          </div>
          <div className="home__stat home__stat--2">
            <span className="stat-num">20+</span>
            <span className="stat-label">Projets<br/>réalisés</span>
          </div>
          <div className="home__stat home__stat--3">
            <span className="stat-num">10+</span>
            <span className="stat-label">Clients<br/>satisfaits</span>
          </div>
        </div>
      </div>

      <div className="home__scroll-hint">
        <span />
        <i className="fas fa-chevron-down" />
      </div>
    </section>
  )
}
