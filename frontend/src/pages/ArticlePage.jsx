import { useState, useEffect, useRef, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useLang } from '../context/LangContext'
import axios from 'axios'
import './ArticlePage.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

/* ── Helpers ─────────────────────────────────────────────── */
const g = (o, l, f) => !o ? '' : o[`${f}_${l}`] || o[`${f}_fr`] || ''
const kws = str => (str||'').split(',').map(s=>s.trim()).filter(Boolean)

/* ── Barre de lecture ──────────────────────────────────────*/
function ReadBar({ target }) {
  const [pct, set] = useState(0)
  useEffect(() => {
    const fn = () => {
      const el = target.current; if (!el) return
      const { top, height } = el.getBoundingClientRect()
      set(Math.min(100, Math.max(0, -top / (height - window.innerHeight) * 100)))
    }
    window.addEventListener('scroll', fn, { passive: true })
    return () => window.removeEventListener('scroll', fn)
  }, [])
  return <div className="arb"><div className="arb-fill" style={{ width: `${pct}%` }} /></div>
}

/* ── TOC latéral ───────────────────────────────────────────*/
function TOC({ secs, lang, cur, go, open, setOpen }) {
  const tl = { fr:'Sommaire', en:'Contents', ar:'المحتويات' }[lang]
  const rl = { fr:'Références', en:'References', ar:'المراجع' }[lang]
  if (!secs.length) return null
  return (
    <aside className={`ar-toc${open ? ' ar-toc--open' : ''}`}>
      {open && <button className="ar-toc-close" onClick={()=>setOpen(false)}>✕</button>}
      <p className="ar-toc-head">{tl}</p>
      <nav className="ar-toc-nav">
        {secs.map((s,i) => (
          <a key={i} href={`#${s.slug}`}
            className={`ar-toc-a${cur===s.slug?' ar-toc-a--on':''}`}
            onClick={e=>{e.preventDefault();go(s.slug)}}>
            <b className="ar-toc-n">{s.order}</b>
            <span>{g(s,lang,'title')||s.title_fr}</span>
          </a>
        ))}
        <a href="#references"
          className={`ar-toc-a${cur==='references'?' ar-toc-a--on':''}`}
          onClick={e=>{e.preventDefault();go('references')}}>
          <b className="ar-toc-n"><i className="fas fa-book-open" /></b>
          <span>{rl}</span>
        </a>
      </nav>
    </aside>
  )
}

/* ── Onglets résumé ────────────────────────────────────────*/
function Abstract({ art, lang }) {
  const [tab, setTab] = useState(lang)
  const tabs = [{c:'fr',f:'🇫🇷',l:'Résumé'},{c:'en',f:'🇬🇧',l:'Abstract'},{c:'ar',f:'🇸🇦',l:'الملخص'}]
    .filter(t => !!art[`abstract_${t.c}`])
  if (!tabs.length) return null
  return (
    <div className="ar-abs">
      <div className="ar-abs-tabs">
        {tabs.map(t=>(
          <button key={t.c} className={`ar-abs-btn${tab===t.c?' on':''}`} onClick={()=>setTab(t.c)}>
            {t.f} {t.l}
          </button>
        ))}
      </div>
      <p className="ar-abs-txt" dir={tab==='ar'?'rtl':'ltr'}>
        {art[`abstract_${tab}`] || art.abstract_fr}
      </p>
    </div>
  )
}

/* ── Stats ─────────────────────────────────────────────────*/
function Stats({ items }) {
  if (!items?.length) return null
  return (
    <div className="ar-stats">
      {items.map((m,i)=>(
        <div key={i} className="ar-stat">
          {m.icon && <span className="ar-stat-ico">{m.icon}</span>}
          <span className="ar-stat-val">{m.value}{m.unit&&<small> {m.unit}</small>}</span>
          <span className="ar-stat-lbl">{m.label}</span>
        </div>
      ))}
    </div>
  )
}

/* ══════════════════════════════════════════════════════════
   PAGE ARTICLE
══════════════════════════════════════════════════════════ */
export default function ArticlePage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { lang, isRTL } = useLang()

  const [art,    setArt]    = useState(null)
  const [rel,    setRel]    = useState([])
  const [phase,  setPhase]  = useState('load')
  const [err,    setErr]    = useState('')
  const [tocOpen,setTocOpen]= useState(false)
  const [active, setActive] = useState('')
  const [top,    setTop]    = useState(false)
  const [copied, setCopied] = useState(false)
  const [big,    setBig]    = useState(false)
  const bodyRef = useRef(null)

  /* fetch */
  useEffect(() => {
    window.scrollTo({ top:0, behavior:'instant' })
    setPhase('load'); setArt(null)
    axios.get(`${API}/articles/${id}/`, { timeout:10000 })
      .then(r => {
        setArt(r.data); setPhase('ok')
        document.title = (r.data.title_fr||'Article') + ' | Portfolio HPB'
        axios.get(`${API}/articles/${id}/related/`, { timeout:5000 })
          .then(rr => setRel(rr.data||[])).catch(()=>{})
      })
      .catch(e => {
        if (e.response?.status === 404) { setPhase('404'); setErr("Article introuvable ou non publié.") }
        else if (!e.response) { setPhase('err'); setErr('Django inaccessible — lancez le serveur sur localhost:8000') }
        else { setPhase('err'); setErr(`Erreur ${e.response.status} — vérifiez : python manage.py migrate`) }
      })
  }, [id])

  /* scroll spy */
  useEffect(() => {
    if (!art) return
    const fn = () => {
      let c = ''
      document.querySelectorAll('.ar-sec').forEach(n => { if (window.scrollY+120 >= n.offsetTop) c = n.id })
      setActive(c)
    }
    window.addEventListener('scroll', fn, { passive:true }); fn()
    return () => window.removeEventListener('scroll', fn)
  }, [art])

  useEffect(() => {
    const fn = () => setTop(window.scrollY > 600)
    window.addEventListener('scroll', fn, { passive:true })
    return () => window.removeEventListener('scroll', fn)
  }, [])

  const go = useCallback(slug => {
    document.getElementById(slug)?.scrollIntoView({ behavior:'smooth', block:'start' })
    setActive(slug); setTocOpen(false)
  }, [])

  const copy = txt => { navigator.clipboard.writeText(txt); setCopied(true); setTimeout(()=>setCopied(false),2500) }

  /* ── Labels ─────────────────────────────────────────────*/
  const T = (fr, en, ar) => ({fr,en,ar})[lang]

  /* ─────────────── ÉTAT CHARGEMENT ───────────────────────*/
  if (phase === 'load') return (
    <section className={`article-page section ${isRTL?'rtl':''}`}>
      <div className="ar-state">
        <div className="ar-spinner" />
        <p>{T('Chargement…','Loading…','جارٍ التحميل…')}</p>
      </div>
    </section>
  )

  /* ─────────────── ÉTAT ERREUR ────────────────────────────*/
  if (phase === 'err' || phase === '404') return (
    <section className={`article-page section ${isRTL?'rtl':''}`}>
      <div className="ar-state">
        <span className="ar-state-ico">{phase==='404'?'📄':'🔌'}</span>
        <h2 className={phase==='err'?'ar-err':'ar-404'}>
          {phase==='404' ? T('Article introuvable','Article not found','المقال غير موجود')
                         : T('Backend inaccessible','Backend unreachable','الخادم غير متاح')}
        </h2>
        <p className="ar-state-msg">{err}</p>
        <div className="ar-state-btns">
          {phase==='err' && <button className="btn-gold" onClick={()=>window.location.reload()}>🔄 Réessayer</button>}
          <button className="btn-gold" onClick={()=>navigate('/articles')}>
            {T('← Articles','← Articles','← المقالات')}
          </button>
        </div>
      </div>
    </section>
  )

  if (!art) return null

  /* ─────────────── DONNÉES ────────────────────────────────*/
  const title    = g(art, lang, 'title')
  const subtitle = g(art, lang, 'subtitle')
  const tags     = kws(art[`keywords_${lang}`] || art.keywords_fr)
  const secs     = Array.isArray(art.content_sections) ? art.content_sections : []
  const metrics  = Array.isArray(art.key_metrics) ? art.key_metrics : []
  const refs     = Array.isArray(art.references) ? art.references : []
  const authors  = Array.isArray(art.authors) ? art.authors : []
  const imgUrl   = art.og_image_url || null
  const firstA   = authors[0]?.author
  const citeStr  = firstA
    ? `${firstA.last_name}, ${(firstA.first_name||'').charAt(0)}. (${art.year}). ${title}. ${art.journal_name}, ${art.volume}. DOI: ${art.doi}`
    : `(${art.year}). ${title}. ${art.journal_name}. DOI: ${art.doi}`

  /* ─────────────── RENDU ──────────────────────────────────*/
  return (
    <section className={`article-page section ${isRTL?'rtl':''}`}>

      <ReadBar target={bodyRef} />

      {/* ── CONTENU CENTRÉ ── */}
      <div className="ar-wrap">

        {/* FIL D'ARIANE */}
        <nav className="ar-bread">
          <button className="ar-bread-btn" onClick={()=>navigate('/articles')}>
            <i className="fas fa-arrow-left" />
            {T(' Articles',' Articles',' المقالات')}
          </button>
          {art.journal_name && <><span className="ar-bread-sep">/</span><span className="ar-bread-item">{art.journal_name}</span></>}
          {art.year && <><span className="ar-bread-sep">/</span><span className="ar-bread-item">{art.year}</span></>}
          {art.doi && <span className="ar-bread-doi">DOI&nbsp;{art.doi}</span>}
        </nav>

        {/* TITRE + IMAGE */}
        <div className="ar-hero">
          <div className="ar-hero-text">
            <h1 className="ar-title">{title}</h1>
            {subtitle && <p className="ar-subtitle">{subtitle}</p>}
          </div>

          {imgUrl && (
            <button className={`ar-thumb${big?' ar-thumb--open':''}`}
              onClick={()=>setBig(!big)} aria-label="Couverture">
              <img src={imgUrl} alt={title} />
              <span className="ar-thumb-hint">{big?'✕':'⛶'}</span>
            </button>
          )}
        </div>

        {/* IMAGE AGRANDIE */}
        {imgUrl && big && (
          <div className="ar-lightbox" onClick={()=>setBig(false)}>
            <img src={imgUrl} alt={title} />
          </div>
        )}

        {/* AUTEURS */}
        {authors.length > 0 && (
          <div className="ar-authors">
            {authors.map((aa,i) => (
              <div key={i} className="ar-author">
                {aa.author.photo_url
                  ? <img src={aa.author.photo_url} className="ar-av ar-av--img" alt="" />
                  : <div className="ar-av">
                      {(aa.author.first_name||'?')[0]}{(aa.author.last_name||'?')[0]}
                    </div>
                }
                <div className="ar-author-info">
                  {aa.author.title && <span className="ar-author-t">{aa.author.title}</span>}
                  <span className="ar-author-name">{aa.author.first_name} {aa.author.last_name}</span>
                  {aa.author.affiliation && <span className="ar-author-af">{aa.author.affiliation}</span>}
                  {aa.author.is_corresponding && <span className="ar-author-mail">✉</span>}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* MOTS-CLÉS */}
        {tags.length > 0 && (
          <div className="ar-kws">
            <span className="ar-kws-lbl">{T('Mots-clés','Keywords','كلمات مفتاحية')} :</span>
            {tags.map((k,i) => <span key={i} className="ar-kw">{k}</span>)}
          </div>
        )}

        {/* META */}
        <div className="ar-meta">
          {art.published_at && (
            <span><i className="fas fa-calendar-alt" /> {new Date(art.published_at).toLocaleDateString(lang==='ar'?'ar-DZ':lang)}</span>
          )}
          {art.view_count > 0 && <span><i className="fas fa-eye" /> {art.view_count} {T('vues','views','مشاهدة')}</span>}
        </div>

        {/* RÉSUMÉS */}
        <Abstract art={art} lang={lang} />

        {/* STATISTIQUES */}
        <Stats items={metrics} />

        {/* BOUTON MOBILE TOC */}
        <button className="ar-toc-mob-btn btn-gold" onClick={()=>setTocOpen(true)}>
          <i className="fas fa-list-ol" /> {T('Sommaire','Contents','فهرس')}
        </button>

        {/* CORPS : TOC + CONTENU */}
        <div className="ar-body" ref={bodyRef}>

          <TOC secs={secs} lang={lang} cur={active} go={go}
            open={tocOpen} setOpen={setTocOpen} />

          <div className="ar-main">

            {/* SECTIONS */}
            {secs.length > 0 ? secs.map((s,i) => {
              const html   = s[`content_${lang}`] || s.content_fr || ''
              const sTitle = g(s,lang,'title') || s.title_fr || ''
              return (
                <div key={i} id={s.slug} className="ar-sec">
                  <h2 className="ar-sec-h">
                    <span className="ar-sec-n">{s.order}</span>
                    {sTitle}
                  </h2>
                  <div className="ar-sec-body"
                    dangerouslySetInnerHTML={{ __html: html ||
                      '<p class="ar-empty">Contenu à rédiger dans l\'admin Django…</p>' }} />
                </div>
              )
            }) : (
              <div className="ar-no-content">
                <i className="fas fa-pen-nib" />
                <p>{T("Aucune section rédigée. Remplissez « Sections de l'article » dans l'admin.",
                       "No sections yet. Fill in 'content_sections' JSON in Django admin.",
                       'لا توجد أقسام بعد.')}</p>
                <a href={`http://localhost:8000/admin/api/article/${art.id}/change/`}
                  target="_blank" rel="noreferrer" className="btn-gold">
                  <i className="fas fa-edit" /> {T("Rédiger dans l'admin","Edit in admin","تحرير")}
                </a>
              </div>
            )}

            {/* RÉFÉRENCES */}
            {refs.length > 0 && (
              <div id="references" className="ar-sec ar-refs">
                <h2 className="ar-sec-h">
                  <span className="ar-sec-n"><i className="fas fa-book-open" /></span>
                  {T('Références bibliographiques','References','المراجع')}
                </h2>
                {refs.map((r,i) => (
                  <div key={i} className="ar-ref">
                    <span className="ar-ref-n">[{i+1}]</span>
                    <span className="ar-ref-txt">{r}</span>
                  </div>
                ))}
              </div>
            )}

            {/* ACTIONS */}
            <div className="ar-actions">
              <button className="btn-gold" onClick={()=>window.print()}>
                <i className="fas fa-print" /> {T('Imprimer','Print','طباعة')}
              </button>
              <button className={`btn-gold${copied?' ar-copied':''}`} onClick={()=>copy(art.doi||'')}>
                <i className={`fas ${copied?'fa-check':'fa-link'}`} />
                {copied ? T('Copié !','Copied!','تم!') : 'DOI'}
              </button>
              {art.attachments?.length > 0 && (
                <a className="btn-gold" href={art.attachments[0].file_url} target="_blank" rel="noreferrer">
                  <i className="fas fa-file-pdf" /> PDF
                </a>
              )}
              <button className="ar-btn-back" onClick={()=>navigate('/articles')}>
                {T('← Retour','← Back','عودة ←')}
              </button>
            </div>

            {/* CITATION */}
            <div className="ar-cite">
              <p className="ar-cite-lbl">
                <i className="fas fa-quote-left" /> {T('Comment citer cet article','How to cite','كيفية الاقتباس')}
              </p>
              <div className="ar-cite-box">
                <p className="ar-cite-txt">{citeStr}</p>
                <button className="ar-cite-copy" onClick={()=>copy(citeStr)} title="Copier">
                  <i className="fas fa-copy" />
                </button>
              </div>
            </div>

          </div>{/* ar-main */}
        </div>{/* ar-body */}

        {/* ARTICLES ASSOCIÉS */}
        {rel.length > 0 && (
          <div className="ar-related">
            <h2 className="section-title">{T('Articles associés','Related articles','مقالات ذات صلة')}</h2>
            <div className="ar-related-grid">
              {rel.map(a => {
                const t  = g(a,lang,'title')
                const su = (g(a,lang,'abstract')||'').replace(/<[^>]+>/g,'')
                return (
                  <div key={a.id} className="card ar-rel" onClick={()=>navigate(`/articles/${a.id}`)}>
                    {a.og_image_url && <div className="ar-rel-img" style={{backgroundImage:`url(${a.og_image_url})`}} />}
                    <div className="ar-rel-body">
                      <span className="ar-rel-year">{a.year}</span>
                      <h3 className="ar-rel-title">{t}</h3>
                      {su && <p className="ar-rel-sum">{su.substring(0,110)}…</p>}
                      <span className="ar-rel-cta">{T('Lire →','Read →','← اقرأ')}</span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}

      </div>{/* ar-wrap */}

      {/* BOUTON HAUT */}
      {top && (
        <button className="ar-totop btn-gold" onClick={()=>window.scrollTo({top:0,behavior:'smooth'})}>
          <i className="fas fa-chevron-up" />
        </button>
      )}

    </section>
  )
}
