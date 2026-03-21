import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useLang } from '../context/LangContext'
import { sendContact } from '../hooks/useApi'
import './Contact.css'

export default function Contact({ profile }) {
  const { t } = useTranslation()
  const { lang, isRTL } = useLang()
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '' })
  const [status, setStatus] = useState(null) // 'loading' | 'success' | 'error'

  const onChange = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  const onSubmit = async e => {
    e.preventDefault()
    setStatus('loading')
    try {
      await sendContact(form)
      setStatus('success')
      setForm({ name: '', email: '', subject: '', message: '' })
      setTimeout(() => setStatus(null), 5000)
    } catch {
      setStatus('error')
      setTimeout(() => setStatus(null), 5000)
    }
  }

  return (
    <section className={`contact section ${isRTL ? 'rtl' : ''}`} id="contact">
      <div className="contact__bg" aria-hidden />
      <div className="contact__inner">
        <div className="contact__info">
          <h2 className="section-title">{t('contact.title')}</h2>
          <p className="contact__intro">
            {lang === 'ar'
              ? 'لا تتردد في التواصل معي. سأرد عليك في أقرب وقت ممكن.'
              : lang === 'en'
              ? "Don't hesitate to reach out. I'll get back to you as soon as possible."
              : "N'hésitez pas à me contacter. Je vous répondrai dans les plus brefs délais."}
          </p>
          <div className="contact__cards">
            <div className="contact-card">
              <div className="cc-icon"><i className="fas fa-envelope" /></div>
              <div>
                <span className="cc-label">Email</span>
                <a href={`mailto:${profile?.email || 'hillaprincebambe@gmail.com'}`} className="cc-value">
                  {profile?.email || 'hillaprincebambe@gmail.com'}
                </a>
              </div>
            </div>
            <div className="contact-card">
              <div className="cc-icon"><i className="fas fa-phone" /></div>
              <div>
                <span className="cc-label">{t('footer.phone')}</span>
                <span className="cc-value">{profile?.phone || '+235 60 92 87 48'}</span>
              </div>
            </div>
            <div className="contact-card">
              <div className="cc-icon"><i className="fas fa-map-marker-alt" /></div>
              <div>
                <span className="cc-label">Location</span>
                <span className="cc-value">N'Djamena, Tchad</span>
              </div>
            </div>
          </div>
        </div>

        <form className="contact__form" onSubmit={onSubmit} noValidate>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="name">{t('contact.name')}</label>
              <input
                id="name" name="name" type="text"
                value={form.name} onChange={onChange}
                placeholder={t('contact.name')} required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">{t('contact.email')}</label>
              <input
                id="email" name="email" type="email"
                value={form.email} onChange={onChange}
                placeholder={t('contact.email')} required
              />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="subject">{t('contact.subject')}</label>
            <input
              id="subject" name="subject" type="text"
              value={form.subject} onChange={onChange}
              placeholder={t('contact.subject')} required
            />
          </div>
          <div className="form-group">
            <label htmlFor="message">{t('contact.message')}</label>
            <textarea
              id="message" name="message" rows={6}
              value={form.message} onChange={onChange}
              placeholder={t('contact.message')} required
            />
          </div>
          <button type="submit" className="btn-gold form-submit" disabled={status === 'loading'}>
            {status === 'loading'
              ? <><i className="fas fa-spinner fa-spin" /> Envoi...</>
              : <><i className="fas fa-paper-plane" /> {t('contact.send')}</>}
          </button>
          {status === 'success' && (
            <div className="form-alert form-alert--success">
              <i className="fas fa-check-circle" /> {t('contact.success')}
            </div>
          )}
          {status === 'error' && (
            <div className="form-alert form-alert--error">
              <i className="fas fa-exclamation-circle" /> {t('contact.error')}
            </div>
          )}
        </form>
      </div>
    </section>
  )
}
