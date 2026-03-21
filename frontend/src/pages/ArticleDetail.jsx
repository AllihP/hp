import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useLang } from '../context/LangContext'
import { getField } from '../hooks/useApi'
import { ARTICLES_CONTENT } from '../data/articlesContent'
import './ArticleDetail.css'

const ICON_MAP = {
  'fa-github': 'fab fa-github', 'fa-hat-cowboy': 'fas fa-hat-cowboy',
  'fa-cloud': 'fas fa-cloud', 'fa-map': 'fas fa-map',
  'fa-server': 'fas fa-server', 'fa-robot': 'fas fa-robot',
}

// Markdown-like renderer
function renderText(text) {
  if (!text) return null
  return text.split('\n').map((line, i) => {
    // Bold
    const parts = line.split(/\*\*(.*?)\*\*/g)
    const rendered = parts.map((p, j) =>
      j % 2 === 1 ? <strong key={j}>{p}</strong> : p
    )
    if (!line.trim()) return <br key={i} />
    if (line.startsWith('- ')) return (
      <li key={i}>{renderInline(line.slice(2))}</li>
    )
    return <span key={i}>{rendered}<br /></span>
  })
}

function renderInline(text) {
  const parts = text.split(/\*\*(.*?)\*\*/g)
  return parts.map((p, i) => i % 2 === 1 ? <strong key={i}>{p}</strong> : p)
}

// Section renderers
function SectionHeading({ section }) {
  return (
    <div className="art-section art-section--heading">
      <h2 className="art-h2">{section.title}</h2>
      <div className="art-prose">
        {section.content?.split('\n').some(l => l.startsWith('- '))
          ? <ul className="art-list">{renderText(section.content)}</ul>
          : <p>{renderText(section.content)}</p>
        }
      </div>
    </div>
  )
}

function SectionCode({ section }) {
  const [copied, setCopied] = useState(false)
  const copy = () => {
    navigator.clipboard.writeText(section.code || '')
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }
  return (
    <div className="art-section art-section--code">
      {section.title && <h3 className="art-h3">{section.title}</h3>}
      <div className="code-block">
        <div className="code-header">
          <div className="code-dots">
            <span className="dot dot--red" />
            <span className="dot dot--yellow" />
            <span className="dot dot--green" />
          </div>
          <span className="code-lang">{section.lang || 'code'}</span>
          <button className="code-copy" onClick={copy}>
            <i className={`fas ${copied ? 'fa-check' : 'fa-copy'}`} />
            {copied ? 'Copié!' : 'Copier'}
          </button>
        </div>
        <pre className="code-body"><code>{section.code}</code></pre>
      </div>
    </div>
  )
}

function SectionTip({ section }) {
  return (
    <div className="art-section art-section--tip">
      <div className="callout callout--tip">
        <div className="callout-icon"><i className="fas fa-lightbulb" /></div>
        <p>{renderText(section.content)}</p>
      </div>
    </div>
  )
}

function SectionWarning({ section }) {
  return (
    <div className="art-section art-section--warning">
      <div className="callout callout--warning">
        <div className="callout-icon"><i className="fas fa-triangle-exclamation" /></div>
        <p>{renderText(section.content)}</p>
      </div>
    </div>
  )
}

function SectionConclusion({ section }) {
  return (
    <div className="art-section art-section--conclusion">
      <div className="conclusion-block">
        <div className="conclusion-icon"><i className="fas fa-flag-checkered" /></div>
        <h3>{section.title}</h3>
        <p>{renderText(section.content)}</p>
      </div>
    </div>
  )
}

function renderSection(section, i) {
  switch (section.type) {
    case 'heading': return <SectionHeading key={i} section={section} />
    case 'code': return <SectionCode key={i} section={section} />
    case 'tip': return <SectionTip key={i} section={section} />
    case 'warning': return <SectionWarning key={i} section={section} />
    case 'conclusion': return <SectionConclusion key={i} section={section} />
    default: return null
  }
}

// Table of Contents
function TOC({ sections, activeIdx }) {
  const headings = sections.filter(s => s.type === 'heading' || s.type === 'conclusion')
  if (headings.length < 2) return null
  return (
    <nav className="art-toc">
      <p className="toc-title"><i className="fas fa-list" /> Sommaire</p>
      <ul>
        {headings.map((s, i) => (
          <li key={i} className={activeIdx === i ? 'active' : ''}>
            <a href={`#section-${i}`} onClick={e => {
              e.preventDefault()
              document.getElementById(`section-${i}`)?.scrollIntoView({ behavior: 'smooth' })
            }}>
              {s.title?.replace(/[🔧📄⏰🚀🔐🔄☁️📦🏗️🐘📥🌐🤖⚡🗺️🎩🎯]/u, '').trim()}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  )
}

export default function ArticleDetail({ articles }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const { lang, isRTL } = useLang()
  const [progress, setProgress] = useState(0)
  const [activeIdx, setActiveIdx] = useState(0)
  const [showScrollTop, setShowScrollTop] = useState(false)
  const articleRef = useRef(null)

  const article = (articles || []).find(a => String(a.id) === String(id))

  // Reading progress bar
  useEffect(() => {
    const onScroll = () => {
      const el = articleRef.current
      if (!el) return
      const { top, height } = el.getBoundingClientRect()
      const winH = window.innerHeight
      const scrolled = Math.max(0, Math.min(1, (-top) / (height - winH)))
      setProgress(scrolled * 100)
      setShowScrollTop(window.scrollY > 400)
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  // Scroll to top on mount
  useEffect(() => { window.scrollTo(0, 0) }, [id])

  if (!article) {
    return (
      <div className="art-notfound">
        <i className="fas fa-file-circle-xmark" />
        <h2>Article introuvable</h2>
        <Link to="/articles" className="btn-gold">← Retour aux articles</Link>
      </div>
    )
  }

  const title = getField(article, lang, 'title')
  const summary = getField(article, lang, 'summary')
  const iconClass = ICON_MAP[article.icon] || `fas ${article.icon}`
  const content = ARTICLES_CONTENT[article.id]?.[lang] || ARTICLES_CONTENT[article.id]?.fr
  const { readTime, intro, sections = [] } = content || {}

  // Related articles (same category, different id)
  const related = (articles || []).filter(a => a.category === article.category && String(a.id) !== String(id)).slice(0, 3)

  return (
    <div className={`art-page ${isRTL ? 'rtl' : ''}`} ref={articleRef}>
      {/* Reading progress bar */}
      <div className="art-progress-bar">
        <div className="art-progress-fill" style={{ width: `${progress}%` }} />
      </div>

      {/* Hero */}
      <header className="art-hero">
        <div className="art-hero__overlay" />
        <div className="art-hero__content">
          <Link to="/articles" className="art-back">
            <i className="fas fa-arrow-left" />
            {lang === 'ar' ? 'العودة إلى المقالات' : lang === 'en' ? 'Back to Articles' : 'Retour aux articles'}
          </Link>

          <div className="art-hero__meta">
            <span className="art-cat">
              <i className={iconClass} />
              {article.category}
            </span>
            <span className="art-dot" />
            <span className="art-time">
              <i className="fas fa-clock" /> {readTime || '10 min'}
            </span>
          </div>

          <h1 className="art-hero__title">{title}</h1>
          <p className="art-hero__summary">{summary}</p>

          <div className="art-hero__author">
            <div className="art-author-avatar">
              <i className="fas fa-user" />
            </div>
            <div>
              <span className="art-author-name">Hilla Prince Bambé</span>
              <span className="art-author-role">
                {lang === 'ar' ? 'المدير التقني — كيسيكو للاستشارات'
                : lang === 'en' ? 'Technical Director — KICEKO CONSULTANT'
                : 'Directeur Technique — KICEKO CONSULTANT'}
              </span>
            </div>
          </div>
        </div>

        {/* Hexagon deco */}
        <div className="art-hero__hex" aria-hidden>
          <div className="ahex ahex--1" />
          <div className="ahex ahex--2" />
          <div className="ahex ahex--3" />
        </div>
      </header>

      {/* Body */}
      <div className="art-body">
        {/* Sticky TOC */}
        <aside className="art-sidebar">
          <TOC sections={sections} activeIdx={activeIdx} />
          {/* Share */}
          <div className="art-share">
            <p className="share-title">
              {lang === 'ar' ? 'مشاركة' : lang === 'en' ? 'Share' : 'Partager'}
            </p>
            <div className="share-btns">
              <a href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}`}
                target="_blank" rel="noreferrer" className="share-btn share-btn--twitter">
                <i className="fab fa-twitter" />
              </a>
              <a href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}`}
                target="_blank" rel="noreferrer" className="share-btn share-btn--linkedin">
                <i className="fab fa-linkedin-in" />
              </a>
              <button className="share-btn share-btn--copy" onClick={() => navigator.clipboard.writeText(window.location.href)}>
                <i className="fas fa-link" />
              </button>
            </div>
          </div>
        </aside>

        {/* Main article content */}
        <article className="art-content">
          {/* Lead paragraph */}
          {intro && (
            <p className="art-intro">{intro}</p>
          )}

          {/* Sections */}
          {sections.map((s, i) => (
            <div key={i} id={`section-${i}`}>
              {renderSection(s, i)}
            </div>
          ))}

          {/* Tags */}
          <div className="art-tags">
            <span className="art-tag">{article.category}</span>
            <span className="art-tag">DevOps</span>
            <span className="art-tag">KICEKO</span>
            <span className="art-tag">Tchad</span>
          </div>
        </article>
      </div>

      {/* Related articles */}
      {related.length > 0 && (
        <section className="art-related">
          <div className="art-related__inner">
            <h2 className="art-related__title">
              {lang === 'ar' ? 'مقالات ذات صلة' : lang === 'en' ? 'Related Articles' : 'Articles similaires'}
            </h2>
            <div className="art-related__grid">
              {related.map(a => (
                <Link key={a.id} to={`/articles/${a.id}`} className="art-rel-card card">
                  <div className="arc-icon">
                    <i className={ICON_MAP[a.icon] || `fas ${a.icon}`} />
                  </div>
                  <span className="arc-cat">{a.category}</span>
                  <h3>{getField(a, lang, 'title')}</h3>
                  <span className="arc-more">
                    {lang === 'ar' ? 'اقرأ المزيد' : lang === 'en' ? 'Read more' : 'Lire plus'}
                    <i className="fas fa-arrow-right" />
                  </span>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Scroll to top */}
      {showScrollTop && (
        <button
          className="scroll-top"
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          aria-label="Scroll to top"
        >
          <i className="fas fa-chevron-up" />
        </button>
      )}
    </div>
  )
}
