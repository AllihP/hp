import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useLang } from '../context/LangContext'
import { getField } from '../hooks/useApi'
import { useInView } from 'react-intersection-observer'
import axios from 'axios'
import './CV.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

/* ─── Item CV ─────────────────────────────────────────────── */
function CVItem({ item, lang, delay }) {
  const { ref, inView } = useInView({ threshold: 0.1, triggerOnce: true })
  return (
    <div ref={ref} className={`cv-item card ${inView ? 'enter' : ''}`}
      style={{ transitionDelay: `${delay}s` }}>
      <div className="cv-item__body">
        <h4>{getField(item, lang, 'title')}</h4>
        {(item[`institution_${lang}`] || item[`company_${lang}`] || item.issuer) && (
          <span className="cv-item__org">
            <i className="fas fa-building" />
            {item[`institution_${lang}`] || item[`company_${lang}`] || item.issuer}
          </span>
        )}
        {(item.year || item.period) && (
          <span className="cv-item__period">
            <i className="fas fa-calendar-alt" />
            {item.year || item.period}
          </span>
        )}
        {(item[`description_${lang}`] || item.description_fr) && (
          <p className="cv-item__desc">{getField(item, lang, 'description')}</p>
        )}
      </div>
    </div>
  )
}

/* ─── Colonne CV ──────────────────────────────────────────── */
function CVColumn({ title, icon, items, lang, colorClass }) {
  const { ref, inView } = useInView({ threshold: 0.1, triggerOnce: true })
  return (
    <div className={`cv-column ${colorClass}`} ref={ref}>
      <div className={`cv-column__header ${inView ? 'enter' : ''}`}>
        <div className="cv-col-icon"><i className={`fas ${icon}`} /></div>
        <h3>{title}</h3>
        <div className="cv-col-line" />
      </div>
      <div className="cv-column__items">
        {items?.map((item, i) => (
          <CVItem key={item.id || i} item={item} lang={lang} delay={i * 0.15} />
        ))}
        {(!items || items.length === 0) && (
          <div className="cv-item card cv-item--empty">
            <i className="fas fa-ellipsis-h" /><span>À compléter...</span>
          </div>
        )}
      </div>
    </div>
  )
}

/* ─── Modale de téléchargement protégée ──────────────────── */
function ModalDownload({ onClose, lang }) {
  const [code, setCode]     = useState('')
  const [status, setStatus] = useState('idle') // idle | loading | error | success
  const [errMsg, setErrMsg] = useState('')

  const L = {
    title:       { fr: 'Télécharger mon CV',          en: 'Download my CV',           ar: 'تحميل السيرة الذاتية' }[lang],
    subtitle:    { fr: 'Entrez le code d\'accès qui vous a été transmis pour télécharger le CV au format PDF.',
                   en: 'Enter the access code you received to download the CV in PDF format.',
                   ar: 'أدخل رمز الوصول الذي تلقيته لتنزيل السيرة الذاتية.' }[lang],
    placeholder: { fr: 'Code d\'accès…',              en: 'Access code…',              ar: 'رمز الوصول…' }[lang],
    btn:         { fr: 'Télécharger',                  en: 'Download',                 ar: 'تحميل' }[lang],
    loading:     { fr: 'Vérification…',                en: 'Checking…',                ar: 'جارٍ التحقق…' }[lang],
    success:     { fr: 'Téléchargement en cours…',     en: 'Downloading…',             ar: 'جارٍ التنزيل…' }[lang],
    cancel:      { fr: 'Annuler',                      en: 'Cancel',                   ar: 'إلغاء' }[lang],
    contact:     { fr: 'Contactez Hilla Prince Bambé pour obtenir le code.',
                   en: 'Contact Hilla Prince Bambé to get the code.',
                   ar: 'تواصل مع هيلا برانس بامبي للحصول على الرمز.' }[lang],
  }

  const handleDownload = async () => {
    if (!code.trim()) return
    setStatus('loading')
    setErrMsg('')

    try {
      const response = await axios.post(
        `${API_BASE}/cv/download/`,
        { code: code.trim() },
        { responseType: 'blob' }
      )

      // Créer un lien temporaire et déclencher le téléchargement
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url  = window.URL.createObjectURL(blob)
      const link = document.createElement('a')

      // Récupérer le nom du fichier depuis l'en-tête si disponible
      const disposition = response.headers['content-disposition'] || ''
      const match = disposition.match(/filename="?([^"]+)"?/)
      link.download = match ? match[1] : 'CV_Hilla_Prince_Bambe.pdf'
      link.href = url
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)

      setStatus('success')
      setTimeout(() => { onClose(); setStatus('idle') }, 2000)

    } catch (err) {
      const msg = err.response?.data?.error || 'Une erreur est survenue.'
      setErrMsg(msg)
      setStatus('error')
    }
  }

  return (
    <div className="cv-modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="cv-modal" role="dialog" aria-modal="true">

        {/* En-tête */}
        <div className="cv-modal__header">
          <div className="cv-modal__icon">
            <i className="fas fa-file-pdf" />
          </div>
          <div>
            <h3>{L.title}</h3>
            <p>{L.subtitle}</p>
          </div>
          <button className="cv-modal__close" onClick={onClose} aria-label="Fermer">
            <i className="fas fa-times" />
          </button>
        </div>

        {/* Corps */}
        <div className="cv-modal__body">

          {/* Input code */}
          <div className="cv-modal__field">
            <label htmlFor="cv-code">
              <i className="fas fa-key" />
              {' '}Code d'accès
            </label>
            <input
              id="cv-code"
              type="text"
              value={code}
              onChange={e => { setCode(e.target.value); setStatus('idle'); setErrMsg('') }}
              onKeyDown={e => e.key === 'Enter' && handleDownload()}
              placeholder={L.placeholder}
              autoFocus
              autoComplete="off"
              spellCheck={false}
            />
          </div>

          {/* Message d'erreur */}
          {status === 'error' && (
            <div className="cv-modal__error">
              <i className="fas fa-exclamation-circle" />
              <div>
                <strong>{errMsg}</strong>
                {errMsg.includes('incorrect') && <p>{L.contact}</p>}
              </div>
            </div>
          )}

          {/* Succès */}
          {status === 'success' && (
            <div className="cv-modal__success">
              <i className="fas fa-check-circle" />
              <strong>{L.success}</strong>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="cv-modal__footer">
          <button className="cv-modal__cancel" onClick={onClose}>
            {L.cancel}
          </button>
          <button
            className="cv-modal__download btn-gold"
            onClick={handleDownload}
            disabled={!code.trim() || status === 'loading' || status === 'success'}
          >
            {status === 'loading' ? (
              <><i className="fas fa-spinner fa-spin" /> {L.loading}</>
            ) : status === 'success' ? (
              <><i className="fas fa-check" /> {L.success}</>
            ) : (
              <><i className="fas fa-download" /> {L.btn}</>
            )}
          </button>
        </div>

        {/* Indication discrète */}
        <p className="cv-modal__hint">
          <i className="fas fa-lock" />
          {lang === 'ar'
            ? ' الرمز متاح فقط للمجنّدين المعتمدين.'
            : lang === 'en'
            ? ' Code available only to authorized recruiters.'
            : ' Code transmis uniquement aux recruteurs autorisés.'}
        </p>
      </div>
    </div>
  )
}

/* ─── Page CV principale ──────────────────────────────────── */
export default function CV({ cvData }) {
  const { t } = useTranslation()
  const { lang, isRTL } = useLang()
  const { ref: titleRef, inView: titleIn } = useInView({ threshold: 0.3, triggerOnce: true })
  const [showModal, setShowModal] = useState(false)

  return (
    <section className={`cv section ${isRTL ? 'rtl' : ''}`} id="cv">
      <div className="cv__bg" aria-hidden />

      <div ref={titleRef} className={`cv__header ${titleIn ? 'enter' : ''}`}>
        <h2 className="section-title">{t('cv.title')}</h2>

        {/* Bouton téléchargement → ouvre la modale */}
        <button className="btn-gold cv__download" onClick={() => setShowModal(true)}>
          <i className="fas fa-download" /> {t('cv.download')}
        </button>
      </div>

      <div className="cv__grid">
        <CVColumn title={t('cv.education')}      icon="fa-graduation-cap" items={cvData?.education}      lang={lang} colorClass="col--blue" />
        <CVColumn title={t('cv.experience')}     icon="fa-briefcase"      items={cvData?.experience}     lang={lang} colorClass="col--gold" />
        <CVColumn title={t('cv.certifications')} icon="fa-certificate"    items={cvData?.certifications} lang={lang} colorClass="col--green" />
      </div>

      {/* Modale */}
      {showModal && <ModalDownload onClose={() => setShowModal(false)} lang={lang} />}
    </section>
  )
}
