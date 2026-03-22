import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useLang } from '../context/LangContext'
import axios from 'axios'
import './ArticleDetail.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const ICONS = {
  'fa-github':'fab fa-github','fa-hat-cowboy':'fas fa-hat-cowboy',
  'fa-cloud':'fas fa-cloud','fa-map':'fas fa-map',
  'fa-server':'fas fa-server','fa-robot':'fas fa-robot',
  'fa-file-code':'fas fa-file-code',
}

/* ─── Calcul temps de lecture ─────────────────────────────── */
function wpm(html) {
  const w = (html || '').replace(/<[^>]+>/g,' ').trim().split(/\s+/).filter(Boolean).length
  return Math.max(1, Math.round(w / 200))
}

/* ─── Préparer le HTML : IDs sur h2 ──────────────────────── */
function prepareHtml(html) {
  if (!html) return { html:'', toc:[] }
  const toc = []
  let n = 0
  const out = html.replace(/<h2([^>]*)>([\s\S]*?)<\/h2>/gi, (_, a, inner) => {
    n++
    const text = inner.replace(/<[^>]+>/g,'').trim()
    const id   = `s${n}`
    toc.push({ id, num:n, text })
    return `<h2${a} id="${id}" data-num="${n}">${inner}</h2>`
  })
  return { html: out, toc }
}

/* ══ SOMMAIRE ════════════════════════════════════════════════ */
function TOC({ toc, lang }) {
  const [active, setActive] = useState(0)
  useEffect(() => {
    if (!toc.length) return
    const fn = () => {
      let c = 0
      toc.forEach((s,i) => {
        const el = document.getElementById(s.id)
        if (el && window.scrollY + 160 >= el.offsetTop) c = i
      })
      setActive(c)
    }
    window.addEventListener('scroll', fn, { passive:true }); fn()
    return () => window.removeEventListener('scroll', fn)
  }, [toc])
  if (!toc.length) return null
  const label = { fr:'Sommaire', en:'Contents', ar:'المحتويات' }[lang]
  return (
    <div className="mag-toc">
      <div className="mag-toc-head"><i className="fas fa-list-ol"/>{label}</div>
      <ol>
        {toc.map((s,i) => (
          <li key={s.id} className={active===i?'on':''}>
            <a href={`#${s.id}`} onClick={e=>{
              e.preventDefault()
              document.getElementById(s.id)?.scrollIntoView({behavior:'smooth',block:'start'})
            }}>
              <span className="mag-toc-n">{s.num}</span>
              <span className="mag-toc-t">{s.text}</span>
            </a>
          </li>
        ))}
      </ol>
    </div>
  )
}

/* ══ BARRE DE LECTURE ════════════════════════════════════════ */
function ReadBar({ target }) {
  const [w, setW] = useState(0)
  useEffect(() => {
    const fn = () => {
      const el = target.current
      if (!el) return
      const { top, height } = el.getBoundingClientRect()
      setW(Math.min(100, Math.max(0, (-top/(height-window.innerHeight))*100)))
    }
    window.addEventListener('scroll', fn, { passive:true })
    return () => window.removeEventListener('scroll', fn)
  }, [])
  return (
    <div className="mag-bar">
      <div className="mag-bar-fill" style={{width:`${w}%`}}/>
    </div>
  )
}

/* ══ BOUTON COPIER ═══════════════════════════════════════════ */
function CopyBtn({ lang }) {
  const [ok, setOk] = useState(false)
  return (
    <button className={`mag-share-btn ${ok?'ok':''}`}
      onClick={()=>{ navigator.clipboard.writeText(window.location.href); setOk(true); setTimeout(()=>setOk(false),2500) }}>
      <i className={`fas ${ok?'fa-check':'fa-link'}`}/>
      <span>{{fr:ok?'Copié!':'Lien', en:ok?'Copied!':'Link', ar:ok?'تم!':'رابط'}[lang]}</span>
    </button>
  )
}

/* ══ PAGE PRINCIPALE ═════════════════════════════════════════ */
export default function ArticleDetail() {
  const { id }          = useParams()
  const navigate        = useNavigate()
  const { lang, isRTL } = useLang()
  const [state, setState] = useState({ s:'load', art:null, related:[] })
  const [top, setTop]   = useState(false)
  const bodyRef         = useRef(null)

  useEffect(() => {
    window.scrollTo({top:0,behavior:'instant'})
    setState({s:'load',art:null,related:[]})
    axios.get(`${API}/articles/`).then(r => {
      const all = r.data
      const art = all.find(a => String(a.id)===String(id))
      if (!art) { setState({s:'404',art:null,related:[]}); return }
      const rel = all.filter(a=>a.category===art.category&&String(a.id)!==String(id)).slice(0,3)
      setState({s:'ok',art,related:rel})
    }).catch(() => setState({s:'err',art:null,related:[]}))
  }, [id])

  useEffect(() => {
    const fn = () => setTop(window.scrollY > 600)
    window.addEventListener('scroll', fn, {passive:true})
    return () => window.removeEventListener('scroll', fn)
  }, [])

  /* ── Labels ─────────────────────────────────────────────── */
  const L = {
    back:  {fr:'← Articles',en:'← Articles',ar:'← المقالات'}[lang],
    read:  {fr:'min de lecture',en:'min read',ar:'دقائق'}[lang],
    by:    {fr:'Par',en:'By',ar:'بقلم'}[lang],
    role:  {fr:'Directeur Technique · KICEKO CONSULTANT',en:'Technical Director · KICEKO CONSULTANT',ar:'المدير التقني · كيسيكو للاستشارات'}[lang],
    share: {fr:'Partager',en:'Share',ar:'مشاركة'}[lang],
    rel:   {fr:'Articles similaires',en:'Related articles',ar:'مقالات ذات صلة'}[lang],
    lire:  {fr:'Lire →',en:'Read →',ar:'← اقرأ'}[lang],
    empty: {fr:"Cet article n'a pas encore de contenu. Rédigez-le dans l'admin Django.",en:"No content yet. Write it in Django admin.",ar:"لا يوجد محتوى بعد."}[lang],
  }

  const { s, art, related } = state

  /* ── États ──────────────────────────────────────────────── */
  if (s==='load') return (
    <div className="mag-state">
      <div className="mag-spinner"/>
      <p style={{color:'rgba(255,255,255,.4)',fontSize:'.9rem'}}>Chargement…</p>
    </div>
  )
  if (s==='err') return (
    <div className="mag-state">
      <i className="fas fa-plug" style={{fontSize:'3rem',color:'rgba(248,113,113,.3)'}}/>
      <h2>Backend inaccessible</h2>
      <p>Lancez Django sur <code>localhost:8000</code></p>
      <button className="btn-gold" onClick={()=>navigate('/articles')}>{L.back}</button>
    </div>
  )
  if (s==='404') return (
    <div className="mag-state">
      <i className="fas fa-newspaper" style={{fontSize:'3.5rem',color:'rgba(245,197,24,.2)'}}/>
      <h2>Article introuvable</h2>
      <button className="btn-gold" onClick={()=>navigate('/articles')}>{L.back}</button>
    </div>
  )

  /* ── Données ─────────────────────────────────────────────── */
  const g = (f) => art[`${f}_${lang}`] || art[`${f}_fr`] || ''
  const title    = g('title')
  const subtitle = g('subtitle')
  const summary  = g('summary')
  const rawHtml  = g('content')
  const { html, toc } = prepareHtml(rawHtml)
  const icon  = ICONS[art.icon] || `fas ${art.icon}`
  const rt    = art.read_time || wpm(rawHtml)
  const cover = art.cover_image_url || art.cover_image || null

  return (
    <div className={`mag-page ${isRTL?'rtl':''}`}>
      <ReadBar target={bodyRef}/>

      {/* ════ HERO ═══════════════════════════════════════════ */}
      <header className="mag-hero" style={cover?{backgroundImage:`url(${cover})`}:{}}>
        <div className="mag-hero-overlay"/>
        {!cover && (
          <div className="mag-hero-pattern" aria-hidden>
            <span/><span/><span/><span/>
          </div>
        )}
        <div className="mag-hero-inner">
          <button className="mag-back" onClick={()=>navigate('/articles')}>
            {L.back}
          </button>

          {/* Méta */}
          <div className="mag-meta">
            <span className="mag-meta-cat"><i className={icon}/> {art.category}</span>
            <span className="mag-meta-sep"/>
            <span className="mag-meta-time"><i className="fas fa-clock"/> {rt} {L.read}</span>
            {art.published_date && <>
              <span className="mag-meta-sep"/>
              <span className="mag-meta-date"><i className="fas fa-calendar"/> {art.published_date}</span>
            </>}
          </div>

          {/* Grand titre */}
          <h1 className="mag-title">{title}</h1>

          {/* Sous-titre */}
          {subtitle && <p className="mag-subtitle">{subtitle}</p>}

          {/* Chapeau */}
          {summary && !subtitle && <p className="mag-subtitle">{summary}</p>}

          {/* Auteur + partage */}
          <div className="mag-byline">
            <div className="mag-author">
              <div className="mag-avatar">HPB</div>
              <div>
                <span className="mag-author-name">{L.by} <strong>Hilla Prince Bambé</strong></span>
                <span className="mag-author-role">{L.role}</span>
              </div>
            </div>
            <div className="mag-share">
              <span className="mag-share-label">{L.share}</span>
              <a className="mag-share-btn tw" target="_blank" rel="noreferrer"
                href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(window.location.href)}`}>
                <i className="fab fa-twitter"/><span>Twitter</span>
              </a>
              <a className="mag-share-btn li" target="_blank" rel="noreferrer"
                href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}`}>
                <i className="fab fa-linkedin-in"/><span>LinkedIn</span>
              </a>
              <CopyBtn lang={lang}/>
            </div>
          </div>
        </div>
      </header>

      {/* ════ CORPS ══════════════════════════════════════════ */}
      <div className="mag-body" ref={bodyRef}>

        {/* Sidebar */}
        <aside className="mag-aside">
          <TOC toc={toc} lang={lang}/>
          {/* Carte auteur */}
          <div className="mag-author-card">
            <div className="mag-author-card-av">HPB</div>
            <div>
              <strong>Hilla Prince Bambé</strong>
              <span>KICEKO CONSULTANT</span>
              <span>N'Djamena, Tchad</span>
            </div>
          </div>
        </aside>

        {/* Article */}
        <main className="mag-main">
          {html ? (
            <div className="mag-content" dangerouslySetInnerHTML={{__html:html}}/>
          ) : (
            <div className="mag-empty">
              <div className="mag-empty-icon"><i className="fas fa-pen-nib"/></div>
              <p>{L.empty}</p>
              <a href={`http://localhost:8000/admin/api/article/${id}/change/`}
                target="_blank" rel="noreferrer" className="btn-gold">
                <i className="fas fa-edit"/> Rédiger dans l'admin
              </a>
            </div>
          )}
        </main>
      </div>

      {/* ════ ARTICLES SIMILAIRES ════════════════════════════ */}
      {related.length > 0 && (
        <section className="mag-related">
          <div className="mag-related-wrap">
            <h2 className="mag-related-title">{L.rel}</h2>
            <div className="mag-related-grid">
              {related.map(a => {
                const t  = a[`title_${lang}`]   || a.title_fr   || ''
                const su = a[`summary_${lang}`] || a.summary_fr || ''
                const ic = ICONS[a.icon] || `fas ${a.icon}`
                const cv = a.cover_image_url || a.cover_image || null
                return (
                  <div key={a.id} className="mag-rel" onClick={()=>navigate(`/articles/${a.id}`)}>
                    {cv && <div className="mag-rel-cover" style={{backgroundImage:`url(${cv})`}}/>}
                    <div className="mag-rel-body">
                      <span className="mag-rel-cat"><i className={ic}/> {a.category}</span>
                      <h3>{t}</h3>
                      <p>{su}</p>
                      <span className="mag-rel-cta">{L.lire}</span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </section>
      )}

      {/* Scroll top */}
      {top && (
        <button className="mag-top" onClick={()=>window.scrollTo({top:0,behavior:'smooth'})}>
          <i className="fas fa-chevron-up"/>
        </button>
      )}
    </div>
  )
}
