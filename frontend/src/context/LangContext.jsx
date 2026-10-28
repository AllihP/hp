import { createContext, useContext, useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'

const LangContext = createContext()

export function LangProvider({ children }) {
  const { i18n } = useTranslation()
  const [lang, setLang] = useState(localStorage.getItem('language') || 'fr')
  const isRTL = lang === 'ar'

  const changeLang = (newLang) => {
    setLang(newLang)
    i18n.changeLanguage(newLang)
    localStorage.setItem('language', newLang)
    document.documentElement.dir = newLang === 'ar' ? 'rtl' : 'ltr'
    document.documentElement.lang = newLang
    // Retour à l'accueil + scroll en haut
    window.location.href = '/'
  }

  useEffect(() => {
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr'
    document.documentElement.lang = lang
  }, [lang, isRTL])

  return (
    <LangContext.Provider value={{ lang, changeLang, isRTL }}>
      {children}
    </LangContext.Provider>
  )
}

export const useLang = () => useContext(LangContext)
