import { useState, useEffect } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useLang } from '../context/LangContext'
import logoImg from '../assets/logo.png'
import './Navbar.css'

export default function Navbar() {
  const { t } = useTranslation()
  const { lang, changeLang, isRTL } = useLang()
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const location = useLocation()

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => { setMenuOpen(false) }, [location])

  const navLinks = [
    { to: '/', label: t('nav.home') },
    { to: '/about', label: t('nav.about') },
    { to: '/cv', label: t('nav.cv') },
    { to: '/articles', label: t('nav.articles') },
  ]

  const langs = ['fr', 'en', 'ar']

  return (
    <nav className={`navbar ${scrolled ? 'navbar--scrolled' : ''} ${isRTL ? 'rtl' : ''}`}>
      <NavLink to="/" className="navbar__logo">
        <img src={logoImg} alt="HPB Logo" />
      </NavLink>

      <button
        className={`navbar__burger ${menuOpen ? 'open' : ''}`}
        onClick={() => setMenuOpen(!menuOpen)}
        aria-label="Menu"
      >
        <span /><span /><span />
      </button>

      <ul className={`navbar__links ${menuOpen ? 'open' : ''}`}>
        {navLinks.map(({ to, label }) => (
          <li key={to}>
            <NavLink
              to={to}
              className={({ isActive }) => isActive ? 'active' : ''}
              end={to === '/'}
            >
              {label}
            </NavLink>
          </li>
        ))}
      </ul>

      <div className={`navbar__langs ${menuOpen ? 'open' : ''}`}>
        {langs.map(l => (
          <button
            key={l}
            className={`lang-btn ${lang === l ? 'active' : ''}`}
            onClick={() => changeLang(l)}
          >
            {l.toUpperCase()}
          </button>
        ))}
      </div>
    </nav>
  )
}
