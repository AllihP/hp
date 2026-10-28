import { NavLink } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useLang } from '../context/LangContext'
import logoImg from '../assets/logo.png'
import './Footer.css'

export default function Footer({ profile }) {
  const { t } = useTranslation()
  const { isRTL } = useLang()

  const socials = [
    { icon: 'fab fa-instagram', url: profile?.instagram || '#', label: 'Instagram' },
    { icon: 'fab fa-twitter', url: profile?.twitter || '#', label: 'Twitter' },
    { icon: 'fab fa-facebook-f', url: profile?.facebook || '#', label: 'Facebook' },
    { icon: 'fab fa-linkedin-in', url: profile?.linkedin || '#', label: 'LinkedIn' },
    { icon: 'fab fa-github', url: profile?.github || '#', label: 'GitHub' },
  ]

  const links = [
    { to: '/', label: t('nav.home') },
    { to: '/about', label: t('nav.about') },
    { to: '/cv', label: t('nav.cv') },
    { to: '/articles', label: t('nav.articles') },
  ]

  return (
    <footer className={`footer ${isRTL ? 'rtl' : ''}`}>
      <div className="footer__glow" />
      <div className="footer__inner">
        <div className="footer__brand">
          <img src={logoImg} alt="HPB" className="footer__logo" />
          <p className="footer__tagline">
            {profile?.title_fr || 'Ingénieur IT & GIS | Directeur Technique KICEKO'}
          </p>
          <div className="footer__socials">
            {socials.map(s => (
              <a key={s.label} href={s.url} target="_blank" rel="noreferrer" aria-label={s.label}>
                <i className={s.icon} />
              </a>
            ))}
          </div>
        </div>

        <div className="footer__section">
          <h4>{t('footer.links')}</h4>
          <ul>
            {links.map(l => (
              <li key={l.to}><NavLink to={l.to} end={l.to === '/'}>{l.label}</NavLink></li>
            ))}
          </ul>
        </div>

        <div className="footer__section">
          <h4>{t('footer.contact')}</h4>
          <p><i className="fas fa-envelope" /> {profile?.email || 'hillaprincebambe@gmail.com'}</p>
          <p><i className="fas fa-phone" /> {profile?.phone || '+235 60 92 87 48'}</p>
          <p><i className="fas fa-map-marker-alt" /> N'Djamena, Tchad</p>
        </div>
      </div>

      <div className="footer__bottom">
        <div className="footer__line" />
        <p>© 2025 Hilla Prince Bambé. {t('footer.rights')}</p>
      </div>
    </footer>
  )
}
