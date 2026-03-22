import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useLang } from '../context/LangContext'
import { getField } from '../hooks/useApi'
import './Articles.css'

const CATEGORIES = ['Tous', 'DevOps', 'Cloud', 'GIS', 'Backend', 'Linux', 'AI']

const ICON_MAP = {
  'fa-github':     'fab fa-github',
  'fa-hat-cowboy': 'fas fa-hat-cowboy',
  'fa-cloud':      'fas fa-cloud',
  'fa-map':        'fas fa-map',
  'fa-server':     'fas fa-server',
  'fa-robot':      'fas fa-robot',
}

export default function Articles({ articles }) {
  const { t }           = useTranslation()
  const { lang, isRTL } = useLang()
  const navigate         = useNavigate()
  const [activecat, setActiveCat] = useState('Tous')

  const filtered = activecat === 'Tous'
    ? (articles || [])
    : (articles || []).filter(a => a.category === activecat)

  const readMoreLabel = { fr: "Lire l'article", en: 'Read article', ar: 'اقرأ المقال' }[lang] || 'Lire'
  const readUnit      = { fr: 'min de lecture', en: 'min read',     ar: 'دقائق' }[lang]

  function goToArticle(id) {
    navigate(`/articles/${id}`)
  }

  return (
    <section className={`articles section ${isRTL ? 'rtl' : ''}`} id="articles">
      <div className="articles-bg-grid" aria-hidden />

      <div className="articles-inner">
        <h2 className="section-title">{t('articles.title')}</h2>

        {/* Filtres */}
        <div className="articles-filters">
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

        {/* Grille */}
        <div className="articles-grid">
          {filtered.length === 0 && (
            <div className="articles-empty">
              <i className="fas fa-ghost" />
              <span>Aucun article dans cette catégorie</span>
            </div>
          )}

          {filtered.map((article, i) => {
            const iconClass = ICON_MAP[article.icon] || `fas ${article.icon}`
            const delay     = `${(i % 3) * 0.08}s`

            return (
              <div
                key={article.id}
                className="art-card"
                style={{ animationDelay: delay }}
                onClick={() => goToArticle(article.id)}
                role="button"
                tabIndex={0}
                onKeyDown={e => e.key === 'Enter' && goToArticle(article.id)}
              >
                {/* Stripe couleur en haut */}
                <div className="art-card-stripe" />

                <div className="art-card-body">
                  {/* Icône + catégorie */}
                  <div className="art-card-top">
                    <div className="art-card-icon">
                      <i className={iconClass} />
                    </div>
                    <span className="art-card-cat">{article.category}</span>
                  </div>

                  {/* Titre */}
                  <h3 className="art-card-title">
                    {getField(article, lang, 'title')}
                  </h3>

                  {/* Résumé */}
                  <p className="art-card-summary">
                    {getField(article, lang, 'summary')}
                  </p>
                </div>

                {/* Footer */}
                <div className="art-card-footer">
                  {article.read_time
                    ? <span className="art-card-time"><i className="fas fa-clock" /> {article.read_time} {readUnit}</span>
                    : <span />
                  }
                  <span className="art-card-cta">
                    {readMoreLabel} <i className="fas fa-arrow-right" />
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
