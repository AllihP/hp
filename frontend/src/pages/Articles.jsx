import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useLang } from '../context/LangContext'
import axios from 'axios'
import './Articles.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

/* Champ localisé avec fallback FR */
function g(obj, lang, field) {
  if (!obj) return ''
  return obj[`${field}_${lang}`] || obj[`${field}_fr`] || ''
}

/* Icône par défaut selon le journal ou les mots-clés */
function getIcon(article) {
  const kw = (article.keywords_fr || '').toLowerCase()
  if (kw.includes('gis') || kw.includes('sig') || kw.includes('cartogr')) return 'fas fa-map'
  if (kw.includes('ia') || kw.includes('ai') || kw.includes('deep')) return 'fas fa-robot'
  if (kw.includes('cloud') || kw.includes('server')) return 'fas fa-cloud'
  if (kw.includes('data') || kw.includes('donnée')) return 'fas fa-database'
  if (kw.includes('linux') || kw.includes('devops')) return 'fas fa-server'
  return 'fas fa-newspaper'
}

export default function Articles() {
  const { t }           = useTranslation()
  const { lang, isRTL } = useLang()
  const navigate         = useNavigate()

  const [articles, setArticles] = useState([])
  const [loading,  setLoading]  = useState(true)
  const [error,    setError]    = useState(false)
  const [search,   setSearch]   = useState('')
  const [activeY,  setActiveY]  = useState('Tous')

  /* ── Toujours fetch directement — ignore les props stales ─ */
  useEffect(() => {
    setLoading(true)
    setError(false)
    axios.get(`${API}/articles/`)
      .then(r => setArticles(r.data || []))
      .catch(() => setError(true))
      .finally(() => setLoading(false))
  }, [])

  /* ── Années disponibles ──────────────────────────────────── */
  const years = ['Tous', ...Array.from(
    new Set(articles.map(a => String(a.year)).filter(Boolean))
  ).sort((a, b) => b - a)]

  /* ── Filtrage ────────────────────────────────────────────── */
  const filtered = articles.filter(a => {
    const yOk = activeY === 'Tous' || String(a.year) === activeY
    const sOk = !search || [a.title_fr, a.title_en, a.abstract_fr, a.keywords_fr]
      .some(f => f?.toLowerCase().includes(search.toLowerCase()))
    return yOk && sOk
  })

  /* ── Labels multilingues ────────────────────────────────── */
  const L = {
    title:    t('articles.title'),
    readMore: { fr: "Lire l'article", en: 'Read article',    ar: 'اقرأ المقال' }[lang],
    allYears: { fr: 'Toutes',         en: 'All',             ar: 'الكل'        }[lang],
    srch:     { fr: 'Rechercher…',    en: 'Search…',         ar: 'ابحث…'       }[lang],
    empty:    { fr: 'Aucun article publié pour le moment.',
                en: 'No articles published yet.',
                ar: 'لا توجد مقالات منشورة بعد.' }[lang],
    offline:  { fr: 'Backend Django inaccessible — lancez le serveur.',
                en: 'Django backend unreachable — start the server.',
                ar: 'خادم Django غير متاح.' }[lang],
    by:       { fr: 'Par', en: 'By', ar: 'بقلم' }[lang],
    views:    { fr: 'vues', en: 'views', ar: 'مشاهدة' }[lang],
  }

  return (
    <section className={`articles section ${isRTL ? 'rtl' : ''}`} id="articles">
      <div className="articles-bg-grid" aria-hidden />

      <div className="articles-inner">
        <h2 className="section-title">{L.title}</h2>

        {/* ── Recherche + filtre années ───────────────────── */}
        <div className="articles-toolbar">
          <div className="articles-search-wrap">
            <i className="fas fa-search" />
            <input
              type="text"
              className="articles-search"
              placeholder={L.srch}
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            {search && (
              <button className="articles-search-clear" onClick={() => setSearch('')}>✕</button>
            )}
          </div>

          <div className="articles-filters">
            {years.map(y => (
              <button
                key={y}
                className={`filter-btn ${activeY === y ? 'active' : ''}`}
                onClick={() => setActiveY(y)}
              >
                {y === 'Tous' ? L.allYears : y}
              </button>
            ))}
          </div>
        </div>

        {/* ── Grille ──────────────────────────────────────── */}
        {loading ? (
          /* Skeleton loader */
          <div className="articles-grid">
            {[1,2,3].map(n => (
              <div key={n} className="art-card art-card--skeleton">
                <div className="art-sk-cover" />
                <div className="art-card-body">
                  <div className="art-sk-line art-sk-line--short" />
                  <div className="art-sk-line" />
                  <div className="art-sk-line art-sk-line--med" />
                </div>
              </div>
            ))}
          </div>
        ) : error ? (
          <div className="articles-empty">
            <i className="fas fa-plug" />
            <span>{L.offline}</span>
          </div>
        ) : filtered.length === 0 ? (
          <div className="articles-empty">
            <i className="fas fa-newspaper" />
            <span>{L.empty}</span>
          </div>
        ) : (
          <div className="articles-grid">
            {filtered.map((article, i) => {
              const title   = g(article, lang, 'title')
              const excerpt = (g(article, lang, 'abstract') || g(article, lang, 'subtitle'))
                .replace(/<[^>]+>/g, '').trim()
              const imgUrl   = article.og_image_url
              const icon     = getIcon(article)
              const authors  = article.authors_names?.slice(0, 2).join(', ') || ''
              const kws      = (article.keywords_fr || '').split(',').map(k => k.trim()).filter(Boolean).slice(0, 3)
              const delay    = `${(i % 3) * 0.07}s`

              return (
                <div
                  key={article.id}
                  className="art-card"
                  style={{ animationDelay: delay }}
                  onClick={() => navigate(`/articles/${article.id}`)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={e => e.key === 'Enter' && navigate(`/articles/${article.id}`)}
                >
                  {/* Stripe dorée au hover */}
                  <div className="art-card-stripe" />

                  {/* Image de couverture — si présente */}
                  {imgUrl && (
                    <div className="art-card-cover"
                      style={{ backgroundImage: `url(${imgUrl})` }} />
                  )}

                  <div className="art-card-body">
                    {/* Icône + badge année/journal */}
                    <div className="art-card-top">
                      <div className="art-card-icon">
                        <i className={icon} />
                      </div>
                      {article.year && (
                        <span className="art-card-cat">{article.year}</span>
                      )}
                    </div>

                    {/* Titre */}
                    <h3 className="art-card-title">{title}</h3>

                    {/* Résumé tronqué */}
                    {excerpt && (
                      <p className="art-card-summary">
                        {excerpt.length > 140 ? excerpt.substring(0, 140) + '…' : excerpt}
                      </p>
                    )}

                    {/* Mots-clés */}
                    {kws.length > 0 && (
                      <div className="art-card-kws">
                        {kws.map((k, j) => <span key={j} className="art-card-kw">{k}</span>)}
                      </div>
                    )}
                  </div>

                  {/* Footer */}
                  <div className="art-card-footer">
                    <div className="art-card-footer-left">
                      {authors && (
                        <span className="art-card-authors">
                          <i className="fas fa-user" /> {authors}
                        </span>
                      )}
                      {article.view_count > 0 && (
                        <span className="art-card-views">
                          <i className="fas fa-eye" /> {article.view_count}
                        </span>
                      )}
                    </div>
                    <span className="art-card-cta">
                      {L.readMore} <i className="fas fa-arrow-right" />
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </section>
  )
}
