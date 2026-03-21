import { useTranslation } from 'react-i18next'
import { useLang } from '../context/LangContext'
import { getField } from '../hooks/useApi'
import { useInView } from 'react-intersection-observer'
import './CV.css'

function CVItem({ item, lang, delay, icon }) {
  const { ref, inView } = useInView({ threshold: 0.1, triggerOnce: true })
  return (
    <div
      ref={ref}
      className={`cv-item card ${inView ? 'enter' : ''}`}
      style={{ transitionDelay: `${delay}s` }}
    >
      {icon && <div className="cv-item__icon"><i className={`fas ${icon}`} /></div>}
      <div className="cv-item__body">
        <h4>{getField(item, lang, 'title')}</h4>
        {(item[`institution_${lang}`] || item[`company_${lang}`] || item.issuer) && (
          <span className="cv-item__org">
            <i className="fas fa-building" />
            {item[`institution_${lang}`] || item[`company_${lang}`] || item.issuer}
          </span>
        )}
        {item.year || item.period ? (
          <span className="cv-item__period">
            <i className="fas fa-calendar-alt" />
            {item.year || item.period}
          </span>
        ) : null}
        {(item[`description_${lang}`] || item[`description_fr`]) && (
          <p className="cv-item__desc">{getField(item, lang, 'description')}</p>
        )}
      </div>
    </div>
  )
}

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
            <i className="fas fa-ellipsis-h" />
            <span>À compléter...</span>
          </div>
        )}
      </div>
    </div>
  )
}

export default function CV({ cvData }) {
  const { t } = useTranslation()
  const { lang, isRTL } = useLang()
  const { ref: titleRef, inView: titleIn } = useInView({ threshold: 0.3, triggerOnce: true })

  return (
    <section className={`cv section ${isRTL ? 'rtl' : ''}`} id="cv">
      <div className="cv__bg" aria-hidden />

      <div ref={titleRef} className={`cv__header ${titleIn ? 'enter' : ''}`}>
        <h2 className="section-title">{t('cv.title')}</h2>
        <a href="#" className="btn-gold cv__download">
          <i className="fas fa-download" /> {t('cv.download')}
        </a>
      </div>

      <div className="cv__grid">
        <CVColumn
          title={t('cv.education')}
          icon="fa-graduation-cap"
          items={cvData?.education}
          lang={lang}
          colorClass="col--blue"
        />
        <CVColumn
          title={t('cv.experience')}
          icon="fa-briefcase"
          items={cvData?.experience}
          lang={lang}
          colorClass="col--gold"
        />
        <CVColumn
          title={t('cv.certifications')}
          icon="fa-certificate"
          items={cvData?.certifications}
          lang={lang}
          colorClass="col--green"
        />
      </div>
    </section>
  )
}
