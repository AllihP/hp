import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useLang } from '../context/LangContext'
import { getField } from '../hooks/useApi'
import { useInView } from 'react-intersection-observer'
import './Articles.css'

const CATEGORIES = ['Tous', 'DevOps', 'Cloud', 'GIS', 'Backend', 'Linux', 'AI']
const ICON_MAP = {
  'fa-github': 'fab fa-github',
  'fa-hat-cowboy': 'fas fa-hat-cowboy',
  'fa-cloud': 'fas fa-cloud',
  'fa-map': 'fas fa-map',
  'fa-server': 'fas fa-server',
  'fa-robot': 'fas fa-robot',
}

function ArticleCard({ article, lang, index }) {
  const { ref, inView } = useInView({ threshold: 0.1, triggerOnce: true })
  const iconClass = ICON_MAP[article.icon] || `fas ${article.icon}`
  return (
    <a
      ref={ref}
      href={article.link || '#'}
      target={article.link && article.link !== '#' ? '_blank' : '_self'}
      rel="noreferrer"
      className={`article-card card ${inView ? 'enter' : ''}`}
      style={{ transitionDelay: `${(index % 3) * 0.12}s` }}
    >
      <div className="article-card__header">
        <div className="article-card__icon">
          <i className={iconClass} />
        </div>
        <span className="article-card__cat">{article.category}</span>
      </div>
      <h3 className="article-card__title">{getField(article, lang, 'title')}</h3>
      <p className="article-card__summary">{getField(article, lang, 'summary')}</p>
      <div className="article-card__footer">
        <span className="read-more">
          {lang === 'ar' ? 'اقرأ المزيد' : lang === 'en' ? 'Read more' : 'Lire plus'}
          <i className="fas fa-arrow-right" />
        </span>
      </div>
      <div className="article-card__glow" />
    </a>
  )
}

export default function Articles({ articles }) {
  const { t } = useTranslation()
  const { lang, isRTL } = useLang()
  const [activecat, setActiveCat] = useState('Tous')
  const filtered = activecat === 'Tous' ? articles : (articles || []).filter(a => a.category === activecat)

  return (
    <section className={`articles section ${isRTL ? 'rtl' : ''}`} id="articles">
      <div className="articles__bg" aria-hidden>
        <div className="bg-grid" />
      </div>

      <div className="articles__inner">
        <h2 className="section-title">{t('articles.title')}</h2>

        {/* Filter tabs */}
        <div className="articles__filters">
          {CATEGORIES.map(cat => (
            <button
              key={cat}
              className={`filter-btn ${activecat === cat ? 'active' : ''}`}
              onClick={() => setActiveCat(cat)}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Grid */}
        <div className="articles__grid">
          {(filtered || []).map((a, i) => (
            <ArticleCard key={a.id || i} article={a} lang={lang} index={i} />
          ))}
          {filtered?.length === 0 && (
            <div className="articles__empty">
              <i className="fas fa-ghost" />
              <span>Aucun article dans cette catégorie</span>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}
