import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useLang } from '../context/LangContext'
import axios from 'axios'
import './ArticleDetail.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const ICONS = {
  'fa-github':     'fab fa-github',
  'fa-hat-cowboy': 'fas fa-hat-cowboy',
  'fa-cloud':      'fas fa-cloud',
  'fa-map':        'fas fa-map',
  'fa-server':     'fas fa-server',
  'fa-robot':      'fas fa-robot',
}

/* ── Calcul du temps de lecture ──────────────────────────── */
function readTime(html) {
  const words = (html || '').replace(/<[^>]+>/g, ' ').trim().split(/\s+/).filter(Boolean).length
  return Math.max(1, Math.round(words / 200))
}

/* ── Inject IDs + data-num on h2 ─────────────────────────── */
function prepareHtml(html) {
  if (!html) return { html: '', toc: [] }
  const toc = []
  let n = 0
  const out = html.replace(/<h2([^>]*)>([\s\S]*?)<\/h2>/gi, (_, attrs, inner) => {
    n++
    const text = inner.replace(/<[^>]+>/g, '').trim()
    const id   = `s${n}`
    toc.push({ id, num: n, text })
    return `<h2${attrs} id="${id}" data-num="${n}">${inner}</h2>`
  })
  return { html: out, toc }
}

/* ══ Sommaire ════════════════════════════════════════════════ */
function TOC({ toc, lang }) {
  const [active, setActive] = useState(0)

  useEffect(() => {
    if (!toc.length) return
    const fn = () => {
      let cur = 0
      toc.forEach((s, i) => {
        const el = document.getElementById(s.id)
        if (el && window.scrollY + 160 >= el.offsetTop) cur = i
      })
      setActive(cur)
    }
    window.addEventListener('scroll', fn, { passive: true })
    fn()
    return () => window.removeEventListener('scroll', fn)
  }, [toc])

  if (toc.length < 2) return null

  const label = { fr: 'Sommaire', en: 'Contents', ar: 'المحتويات' }[lang]

  return (
    <div className="ar-toc">
      <div className="ar-toc-head"><i className="fas fa-list-ol" /> {label}</div>
      <ol>
        {toc.map((s, i) => (
          <li key={s.id} className={active === i ? 'on' : ''}>
            <a href={`#${s.id}`} onClick={e => {
              e.preventDefault()
              document.getElementById(s.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
            }}>
              <span className="ar-toc-n">{s.num}</span>
              <span className="ar-toc-t">{s.text}</span>
            </a>
          </li>
        ))}
      </ol>
    </div>
  )
}

/* ══ Barre de progression ════════════════════════════════════ */
function ProgressBar({ ref }) {
  const [w, setW] = useState(0)
  useEffect(() => {
    const fn = () => {
      const el = ref.current
      if (!el) return
      const { top, height } = el.getBoundingClientRect()
      setW(Math.min(100, Math.max(0, (-top / (height - window.innerHeight)) * 100)))
    }
    window.addEventListener('scroll', fn, { passive: true })
    return () => window.removeEventListener('scroll', fn)
  }, [])
  return <div className="ar-progress"><div className="ar-progress-fill" style={{ width: `${w}%` }} /></div>
}

/* ══ Copier lien ═════════════════════════════════════════════ */
function CopyBtn({ lang }) {
  const [ok, setOk] = useState(false)
  const label = ok
    ? { fr: 'Copié !', en: 'Copied!', ar: 'تم!' }[lang]
    : { fr: 'Copier', en: 'Copy',    ar: 'نسخ'  }[lang]
  return (
    <button className={`ar-share-btn ${ok ? 'ok' : ''}`} onClick={() => {
      navigator.clipboard.writeText(window.location.href)
      setOk(true); setTimeout(() => setOk(false), 2500)
    }}>
      <i className={`fas ${ok ? 'fa-check' : 'fa-link'}`} /> {label}
    </button>
  )
}

/* ══ COMPOSANT PRINCIPAL ═════════════════════════════════════ */
export default function ArticleDetail() {
  const { id }          = useParams()
  const navigate        = useNavigate()
  const { lang, isRTL } = useLang()
  const [state, setState] = useState({ status: 'loading', article: null, related: [] })
  const [showTop, setShowTop] = useState(false)
  const bodyRef = useRef(null)

  /* Charger l'article + la liste */
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' })
    setState({ status: 'loading', article: null, related: [] })

    const load = async () => {
      try {
        const res = await axios.get(`${API_BASE}/articles/`)
        const all = res.data
        const art = all.find(a => String(a.id) === String(id))
        if (!art) { setState({ status: 'notfound', article: null, related: [] }); return }
        const rel = all.filter(a => a.category === art.category && String(a.id) !== String(id)).slice(0, 3)
        setState({ status: 'ok', article: art, related: rel })
      } catch {
        setState({ status: 'error', article: null, related: [] })
      }
    }
    load()
  }, [id])

  useEffect(() => {
    const fn = () => setShowTop(window.scrollY > 600)
    window.addEventListener('scroll', fn, { passive: true })
    return () => window.removeEventListener('scroll', fn)
  }, [])

  const { status, article, related } = state

  /* ── Labels ─────────────────────────────────────────────── */
  const L = {
    back:    { fr: '← Mes articles',    en: '← My articles',      ar: '← مقالاتي' }[lang],
    readU:   { fr: 'min de lecture',    en: 'min read',             ar: 'دقيقة قراءة' }[lang],
    by:      { fr: 'Rédigé par',        en: 'Written by',           ar: 'بقلم' }[lang],
    role:    { fr: 'Directeur Technique · KICEKO CONSULTANT',
               en: 'Technical Director · KICEKO CONSULTANT',
               ar: 'المدير التقني · كيسيكو للاستشارات' }[lang],
    share:   { fr: 'Partager',          en: 'Share',                ar: 'مشاركة' }[lang],
    similar: { fr: 'Articles similaires', en: 'Related articles',   ar: 'مقالات ذات صلة' }[lang],
    readBtn: { fr: 'Lire →',            en: 'Read →',               ar: '← اقرأ' }[lang],
    noContent:{fr: "Contenu non encore rédigé. Allez dans l'admin Django pour écrire cet article.",
               en: "No content yet. Go to Django admin to write this article.",
               ar: "لا يوجد محتوى بعد. اذهب إلى لوحة الإدارة لكتابة المقال." }[lang],
  }

  /* ── États de chargement ─────────────────────────────────── */
  if (status === 'loading') return (
    <div className="ar-state">
      <div className="ar-spinner" />
      <p>Chargement de l'article…</p>
    </div>
  )

  if (status === 'error') return (
    <div className="ar-state">
      <i className="fas fa-wifi" style={{ fontSize: '3rem', color: 'rgba(248,113,113,.4)' }} />
      <h2 style={{ color: 'rgba(255,255,255,.6)' }}>
        Impossible de charger l'article
      </h2>
      <p style={{ color: 'var(--gray)', fontSize: '.9rem', maxWidth: 400, textAlign: 'center' }}>
        Assurez-vous que le backend Django tourne sur <code>localhost:8000</code>
      </p>
      <button className="btn-gold" onClick={() => navigate('/articles')}>
        <i className="fas fa-arrow-left" /> {L.back}
      </button>
    </div>
  )

  if (status === 'notfound') return (
    <div className="ar-state">
      <i className="fas fa-newspaper" style={{ fontSize: '3.5rem', color: 'rgba(245,197,24,.2)' }} />
      <h2 style={{ color: 'rgba(255,255,255,.55)' }}>Article introuvable</h2>
      <button className="btn-gold" onClick={() => navigate('/articles')}>
        <i className="fas fa-arrow-left" /> {L.back}
      </button>
    </div>
  )

  /* ── Données ─────────────────────────────────────────────── */
  const title   = article[`title_${lang}`]   || article.title_fr   || ''
  const summary = article[`summary_${lang}`] || article.summary_fr || ''
  const rawHtml = article[`content_${lang}`] || article.content_fr || ''
  const { html, toc } = prepareHtml(rawHtml)
  const icon    = ICONS[article.icon] || `fas ${article.icon}`
  const rt      = article.read_time || readTime(rawHtml)

  return (
    <div className={`ar-page ${isRTL ? 'rtl' : ''}`}>

      {/* Barre de progression */}
      <ProgressBar ref={bodyRef} />

      {/* ════ HERO ═══════════════════════════════════════════ */}
      <header className="ar-hero">
        <div className="ar-hero-glow" />
        <div className="ar-hero-hex" aria-hidden>
          <span /><span /><span />
        </div>

        <div className="ar-hero-inner">
          <button className="ar-back" onClick={() => navigate('/articles')}>
            {L.back}
          </button>

          {/* Badges méta */}
          <div className="ar-badges">
            <span className="ar-badge-cat"><i className={icon} /> {article.category}</span>
            <span className="ar-badge-dot" />
            <span className="ar-badge-time"><i className="fas fa-clock" /> {rt} {L.readU}</span>
            {article.published_date && (
              <>
                <span className="ar-badge-dot" />
                <span className="ar-badge-date"><i className="fas fa-calendar" /> {article.published_date}</span>
              </>
            )}
          </div>

          {/* Grand titre */}
          <h1 className="ar-title">{title}</h1>

          {/* Chapeau */}
          {summary && <p className="ar-lead">{summary}</p>}

          {/* Auteur */}
          <div className="ar-author-row">
            <div className="ar-avatar">HPB</div>
            <div>
              <span className="ar-author-name">{L.by} <strong>Hilla Prince Bambé</strong></span>
              <span className="ar-author-role">{L.role}</span>
            </div>
          </div>

          {/* Partage */}
          <div className="ar-share">
            <span>{L.share} :</span>
            <a className="ar-share-btn tw"
              href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(window.location.href)}`}
              target="_blank" rel="noreferrer">
              <i className="fab fa-twitter" /> Twitter
            </a>
            <a className="ar-share-btn li"
              href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}`}
              target="_blank" rel="noreferrer">
              <i className="fab fa-linkedin-in" /> LinkedIn
            </a>
            <CopyBtn lang={lang} />
          </div>
        </div>
      </header>

      {/* ════ CORPS ══════════════════════════════════════════ */}
      <div className="ar-body" ref={bodyRef}>

        {/* Sommaire sticky */}
        <aside className="ar-sidebar">
          <TOC toc={toc} lang={lang} />

          {/* Info auteur */}
          <div className="ar-author-card">
            <div className="ar-author-card-avatar">HPB</div>
            <div>
              <strong>Hilla Prince Bambé</strong>
              <span>KICEKO CONSULTANT</span>
              <span>N'Djamena, Tchad</span>
            </div>
          </div>
        </aside>

        {/* Article */}
        <main className="ar-main">
          {html ? (
            <article className="ar-content" dangerouslySetInnerHTML={{ __html: html }} />
          ) : (
            <div className="ar-empty">
              <i className="fas fa-pen-nib" />
              <p>{L.noContent}</p>
              <a href={`http://localhost:8000/admin/api/article/${id}/change/`}
                target="_blank" rel="noreferrer" className="btn-gold">
                <i className="fas fa-edit" /> Rédiger dans l'admin
              </a>
            </div>
          )}
        </main>
      </div>

      {/* ════ ARTICLES SIMILAIRES ════════════════════════════ */}
      {related.length > 0 && (
        <section className="ar-related">
          <div className="ar-related-wrap">
            <h2>{L.similar}</h2>
            <div className="ar-related-grid">
              {related.map(a => {
                const t = a[`title_${lang}`]   || a.title_fr   || ''
                const s = a[`summary_${lang}`] || a.summary_fr || ''
                const ic = ICONS[a.icon] || `fas ${a.icon}`
                return (
                  <div key={a.id} className="ar-rel" onClick={() => navigate(`/articles/${a.id}`)}>
                    <div className="ar-rel-top">
                      <div className="ar-rel-icon"><i className={ic} /></div>
                      <span className="ar-rel-cat">{a.category}</span>
                    </div>
                    <h3>{t}</h3>
                    <p>{s}</p>
                    <span className="ar-rel-cta">{L.readBtn}</span>
                  </div>
                )
              })}
            </div>
          </div>
        </section>
      )}

      {showTop && (
        <button className="ar-top" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <i className="fas fa-chevron-up" />
        </button>
      )}
    </div>
  )
}
