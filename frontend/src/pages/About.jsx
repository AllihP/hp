import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { useLang } from '../context/LangContext'
import { getField } from '../hooks/useApi'
import { useInView } from 'react-intersection-observer'
import hillaImg from '../assets/hpb.png'
import './About.css'

function SkillBar({ skill, lang, delay }) {
  const { ref, inView } = useInView({ threshold: 0.3, triggerOnce: true })
  return (
    <div className="skill-item" ref={ref} style={{ animationDelay: `${delay}s` }}>
      <div className="skill-header">
        <span className="skill-name">
          <i className={`fas ${skill.icon || 'fa-circle'}`} />
          {getField(skill, lang, 'name')}
        </span>
        <span className="skill-pct">{skill.percentage}%</span>
      </div>
      <div className="progress-track">
        <div
          className="progress-fill"
          style={{ width: inView ? `${skill.percentage}%` : '0%' }}
        />
      </div>
    </div>
  )
}

export default function About({ profile, skills }) {
  const { t } = useTranslation()
  const { lang, isRTL } = useLang()
  const { ref: sectionRef, inView } = useInView({ threshold: 0.1, triggerOnce: true })

  const bio = profile ? getField(profile, lang, 'bio') : ''

  const features = [
    { icon: 'fa-laptop-code', label_fr: 'Développement', label_en: 'Development', label_ar: 'التطوير' },
    { icon: 'fa-map', label_fr: 'Géomatique GIS', label_en: 'GIS Geomatics', label_ar: 'الجيوماتيك' },
    { icon: 'fa-project-diagram', label_fr: 'Gestion Projet', label_en: 'Project Management', label_ar: 'إدارة مشاريع' },
    { icon: 'fa-cloud', label_fr: 'DevOps & Cloud', label_en: 'DevOps & Cloud', label_ar: 'ديف أوبس وسحابة' },
  ]
  const getFeatureLabel = f => f[`label_${lang}`] || f.label_fr

  return (
    <section className={`about section ${isRTL ? 'rtl' : ''}`} id="about" ref={sectionRef}>
      <div className="about__bg-decor" aria-hidden>
        {[...Array(3)].map((_, i) => <div key={i} className={`decor-hex decor-hex--${i+1}`} />)}
      </div>

      <div className="about__inner">
        {/* Left: image + floating cards */}
        <div className={`about__visual ${inView ? 'enter' : ''}`}>
          <div className="about__img-frame">
            <div className="frame-border" />
            <img src={hillaImg} alt="Hilla Prince Bambé" />
            <div className="frame-corner frame-corner--tl" />
            <div className="frame-corner frame-corner--br" />
          </div>
          <div className="about__features">
            {features.map((f, i) => (
              <div key={i} className="feature-chip" style={{ animationDelay: `${0.2 * i}s` }}>
                <i className={`fas ${f.icon}`} />
                <span>{getFeatureLabel(f)}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Right: content */}
        <div className={`about__content ${inView ? 'enter' : ''}`}>
          <h2 className="section-title">{t('about.title')}</h2>
          <div className="about__tag">
            <span>Président du Groupe @ AllihTech</span>
          </div>
          <p className="about__bio">{bio}</p>

          <div className="about__infos">
            <div className="info-row">
              <i className="fas fa-map-marker-alt" />
              <span>N'Djamena, Tchad</span>
            </div>
            <div className="info-row">
              <i className="fas fa-envelope" />
              <a href={`mailto:${profile?.email || 'hillaprincebambe@gmail.com'}`}>
                {profile?.email || 'hillaprincebambe@gmail.com'}
              </a>
            </div>
            <div className="info-row">
              <i className="fas fa-phone" />
              <span>{profile?.phone || '+235 60 92 87 48'}</span>
            </div>
          </div>

          <a href="mailto:hillaprincebambe@gmail.com" className="btn-gold">
            {t('about.hire')} <i className="fas fa-arrow-right" />
          </a>

          {/* Skills */}
          <div className="about__skills">
            <h3 className="skills__title">{t('about.skills_title')}</h3>
            <div className="skills__list">
              {(skills || []).map((s, i) => (
                <SkillBar key={s.id} skill={s} lang={lang} delay={i * 0.15} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
