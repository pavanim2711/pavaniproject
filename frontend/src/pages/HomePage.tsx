import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router'
import { theme } from '@styles/theme'
import { productService, Product } from '@services/productService'

// Category emoji mapping
const getCategoryEmoji = (category: string): string => {
  const emojiMap: Record<string, string> = {
    'Outdoor': '🏕️',
    'Indoor': '🏠',
    'Sports': '⚽',
    'Tools': '🔧',
    'Party': '🎉',
    'Travel': '✈️',
  }
  return emojiMap[category] || '📦'
}

const getEmojiForCategory = (category: string): string => getCategoryEmoji(category)

const CATEGORIES = [
  { label: 'Outdoor', emoji: '🏕️' },
  { label: 'Indoor',  emoji: '🏠' },
  { label: 'Sports',  emoji: '⚽' },
  { label: 'Tools',   emoji: '🔧' },
  { label: 'Party',   emoji: '🎉' },
  { label: 'Travel',  emoji: '✈️' },
]

const PROMO_CARDS = [
  {
    title: 'Outdoor Adventure Gear',
    subtitle: 'Tents, hiking gear, camping essentials & more',
    bg: 'linear-gradient(135deg, #1a5e20 0%, #2e7d32 100%)',
    emoji: '🏕️',
    btn: 'Rent Now',
    category: 'Outdoor',
  },
  {
    title: 'Party & Event Supplies',
    subtitle: 'Sound systems, decor, chairs & tables',
    bg: 'linear-gradient(135deg, #e65100 0%, #f57c00 100%)',
    emoji: '🎉',
    btn: 'Book Now',
    category: 'Party',
  },
  {
    title: 'Need tools for a project?',
    subtitle: 'Drills, ladders, painting kits & more',
    bg: 'linear-gradient(135deg, #1565c0 0%, #1976d2 100%)',
    emoji: '🔧',
    btn: 'Rent Now',
    category: 'Tools',
  },
]

// ─── HOW TO ADD REAL IMAGES ───────────────────────────────────────────────
// 1. Drop your photo into:  frontend/public/images/<filename>.jpg
// 2. Set  image: '/images/<filename>.jpg'  on the product below
// 3. Save — Vite reloads instantly, no server restart needed
// 4. Leave image undefined (or remove it) to keep the emoji fallback
// ──────────────────────────────────────────────────────────────────────────
const MOCK_PRODUCTS = [
  { id: 1, name: 'Camping Tent (4-person)', price_per_hour: 150, category: 'Outdoor', image_url: '/images/tent.jfif', emoji: '🏕️' },
  { id: 2, name: 'Portable Bluetooth Speaker', price_per_hour: 80,  category: 'Party', image_url: '/images/bluetooth speaker.jfif', emoji: '🔊'},
  { id: 3, name: 'Power Drill Set',            price_per_hour: 100, category: 'Tools',   image_url: '/images/electric-drill-500x500.webp', emoji: '🔧' },
  { id: 4, name: 'Trekking Backpack 60L',      price_per_hour: 120, category: 'Outdoor', image_url: '/images/outdoor picture.jfif'},
  { id: 5, name: 'Folding Table (6-seater)',   price_per_hour: 90,  category: 'Party', image_url:'/images/folding table.webp'},
  { id: 6, name: 'Ladder 8ft Aluminium',       price_per_hour: 70,  category: 'Tools', image_url: '/images/ladder.jpg', emoji: '🪜' },
  { id: 7, name: 'Action Camera + Mounts',     price_per_hour: 200, category: 'Travel', image_url: '/images/action camera.jfif', emoji: '📷'},
  { id: 8, name: 'Badminton Set (full)',        price_per_hour: 60,  category: 'Sports', image_url: '/images/badmiton set.avif', emoji: '🏸'}
]

export function HomePage() {
  const navigate = useNavigate()
  const [activeCategory, setActiveCategory] = useState<string | null>(null)
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      setLoading(true)
      setError(null)
      console.log('Fetching products from API...')
      const data = await productService.getAllProducts()
      console.log('Products fetched successfully:', data)
      setProducts(Array.isArray(data) && data.length > 0 ? data : MOCK_PRODUCTS as any)
    } catch (err) {
      console.error('Error fetching products, using mock data:', err)
      // Always use mock products as fallback
      setProducts(MOCK_PRODUCTS as any)
    } finally {
      setLoading(false)
    }
  }

  const filtered = activeCategory
    ? products.filter(p => p.category === activeCategory)
    : products

  return (
    <div style={{ backgroundColor: theme.colors.background, minHeight: '100vh' }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: `${theme.spacing.lg} ${theme.spacing.md}` }}>

        {/* ── Hero banner ── */}
        <div style={{
          borderRadius: theme.borderRadius.lg,
          background: 'linear-gradient(135deg, #0c831f 0%, #1a7a2e 60%, #2e7d32 100%)',
          padding: `${theme.spacing.xl} ${theme.spacing.xl}`,
          marginBottom: theme.spacing.md,
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          overflow: 'hidden', position: 'relative', minHeight: '200px',
        }}>
          <div style={{ zIndex: 1 }}>
            <h1 style={{
              color: theme.colors.white, fontSize: theme.typography.fontSize['2xl'],
              fontWeight: theme.typography.fontWeight.bold, lineHeight: '1.25',
              marginBottom: theme.spacing.sm, maxWidth: '440px',
            }}>
              Rent anything, anytime in Bengaluru
            </h1>
            <p style={{
              color: 'rgba(255,255,255,0.85)', fontSize: theme.typography.fontSize.md,
              marginBottom: theme.spacing.lg, maxWidth: '380px',
            }}>
              Tents, tools, party gear, sports equipment & more — delivered in 30 min
            </p>
            <button
              onClick={() => navigate('/products')}
              style={{
                padding: `12px ${theme.spacing.xl}`,
                backgroundColor: theme.colors.white,
                color: theme.colors.primary,
                border: 'none', borderRadius: theme.borderRadius.sm,
                fontWeight: theme.typography.fontWeight.bold,
                fontSize: theme.typography.fontSize.md,
                cursor: 'pointer',
              }}
            >Browse Products</button>
          </div>
          <div style={{
            fontSize: '110px', position: 'absolute', right: '40px', bottom: '-10px',
            opacity: 0.35, userSelect: 'none',
          }}>🏕️</div>
        </div>

        {/* ── 3 promo cards ── */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
          gap: theme.spacing.md,
          marginBottom: theme.spacing.xl,
        }}>
          {PROMO_CARDS.map(card => (
            <div
              key={card.title}
              onClick={() => navigate(`/products?category=${card.category}`)}
              style={{
                background: card.bg,
                borderRadius: theme.borderRadius.md,
                padding: theme.spacing.lg,
                cursor: 'pointer',
                position: 'relative', overflow: 'hidden', minHeight: '160px',
                display: 'flex', flexDirection: 'column', justifyContent: 'flex-end',
                transition: 'transform 0.15s',
              }}
              onMouseOver={e => (e.currentTarget.style.transform = 'translateY(-3px)')}
              onMouseOut={e  => (e.currentTarget.style.transform = 'translateY(0)')}
            >
              <div style={{ position: 'absolute', right: '16px', top: '12px', fontSize: '52px', opacity: 0.6 }}>
                {card.emoji}
              </div>
              <h3 style={{ color: '#fff', fontWeight: theme.typography.fontWeight.bold, fontSize: theme.typography.fontSize.lg, marginBottom: '4px' }}>
                {card.title}
              </h3>
              <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: theme.typography.fontSize.sm, marginBottom: theme.spacing.sm }}>
                {card.subtitle}
              </p>
              <button style={{
                alignSelf: 'flex-start',
                padding: `7px ${theme.spacing.md}`,
                backgroundColor: theme.colors.white,
                color: '#1c1c1c',
                border: 'none', borderRadius: theme.borderRadius.xs,
                fontWeight: theme.typography.fontWeight.semibold,
                fontSize: theme.typography.fontSize.sm, cursor: 'pointer',
              }}>
                {card.btn}
              </button>
            </div>
          ))}
        </div>

        {/* ── Category chips ── */}
        <h2 style={{ fontSize: theme.typography.fontSize.xl, fontWeight: theme.typography.fontWeight.bold, color: theme.colors.text, marginBottom: theme.spacing.md }}>
          Browse by Category
        </h2>
        <div style={{ display: 'flex', gap: theme.spacing.sm, flexWrap: 'wrap', marginBottom: theme.spacing.xl }}>
          <button
            onClick={() => setActiveCategory(null)}
            style={{
              padding: `8px ${theme.spacing.md}`,
              borderRadius: theme.borderRadius.full,
              border: `2px solid ${activeCategory === null ? theme.colors.primary : theme.colors.border}`,
              backgroundColor: activeCategory === null ? theme.colors.primaryLight : theme.colors.white,
              color: activeCategory === null ? theme.colors.primary : theme.colors.text,
              fontWeight: theme.typography.fontWeight.medium,
              fontSize: theme.typography.fontSize.sm, cursor: 'pointer',
            }}
          >All</button>
          {CATEGORIES.map(cat => (
            <button
              key={cat.label}
              onClick={() => setActiveCategory(cat.label)}
              style={{
                padding: `8px ${theme.spacing.md}`,
                borderRadius: theme.borderRadius.full,
                border: `2px solid ${activeCategory === cat.label ? theme.colors.primary : theme.colors.border}`,
                backgroundColor: activeCategory === cat.label ? theme.colors.primaryLight : theme.colors.white,
                color: activeCategory === cat.label ? theme.colors.primary : theme.colors.text,
                fontWeight: theme.typography.fontWeight.medium,
                fontSize: theme.typography.fontSize.sm, cursor: 'pointer',
                display: 'flex', alignItems: 'center', gap: '6px',
              }}
            >
              <span>{cat.emoji}</span> {cat.label}
            </button>
          ))}
        </div>

        {/* ── Product grid ── */}
        <h2 style={{ fontSize: theme.typography.fontSize.xl, fontWeight: theme.typography.fontWeight.bold, color: theme.colors.text, marginBottom: theme.spacing.md }}>
          {activeCategory ? `${activeCategory} Rentals` : 'Popular Rentals'}
        </h2>
        
        {loading ? (
          <div style={{ textAlign: 'center', padding: theme.spacing.xl }}>
            <p style={{ color: theme.colors.textSecondary }}>Loading products...</p>
          </div>
        ) : error ? (
          <div style={{ textAlign: 'center', padding: theme.spacing.xl }}>
            <p style={{ color: theme.colors.textSecondary }}>{error}</p>
            <button
              onClick={fetchProducts}
              style={{
                marginTop: theme.spacing.md,
                padding: `8px ${theme.spacing.md}`,
                backgroundColor: theme.colors.primary,
                color: theme.colors.white,
                border: 'none',
                borderRadius: theme.borderRadius.sm,
                cursor: 'pointer',
              }}
            >
              Retry
            </button>
          </div>
        ) : filtered.length === 0 ? (
          <div style={{ textAlign: 'center', padding: theme.spacing.xl }}>
            <p style={{ color: theme.colors.textSecondary }}>No products found in this category</p>
          </div>
        ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(210px, 1fr))',
          gap: theme.spacing.md,
        }}>
          {filtered.map(product => (
            <div
              key={product.id}
              onClick={() => navigate(`/products/${product.id}`)}
              style={{
                backgroundColor: theme.colors.white,
                borderRadius: theme.borderRadius.md,
                border: `1px solid ${theme.colors.border}`,
                padding: theme.spacing.md,
                cursor: 'pointer',
                transition: 'box-shadow 0.15s, transform 0.15s',
                display: 'flex', flexDirection: 'column', gap: theme.spacing.sm,
              }}
              onMouseOver={e => {
                e.currentTarget.style.boxShadow = theme.shadows.md
                e.currentTarget.style.transform = 'translateY(-2px)'
              }}
              onMouseOut={e => {
                e.currentTarget.style.boxShadow = 'none'
                e.currentTarget.style.transform = 'translateY(0)'
              }}
            >
              {/* Product image */}
              {product.image_url ? (
                <img
                  src={product.image_url}
                  alt={product.name}
                  style={{
                    width: '100%', height: '130px',
                    objectFit: 'cover',
                    borderRadius: theme.borderRadius.sm,
                    backgroundColor: theme.colors.background,
                  }}
                  onError={(e) => {
                    // Show emoji fallback if image fails to load
                    e.currentTarget.style.display = 'none'
                    const container = e.currentTarget.parentElement
                    if (container) {
                      const emoji = document.createElement('div')
                      emoji.style.height = '130px'
                      emoji.style.backgroundColor = theme.colors.background
                      emoji.style.borderRadius = theme.borderRadius.sm
                      emoji.style.display = 'flex'
                      emoji.style.alignItems = 'center'
                      emoji.style.justifyContent = 'center'
                      emoji.style.fontSize = '52px'
                      emoji.textContent = getEmojiForCategory(product.category)
                      container.appendChild(emoji)
                    }
                  }}
                />
              ) : null}

              <span style={{
                display: 'inline-block', alignSelf: 'flex-start',
                padding: '2px 8px',
                backgroundColor: theme.colors.primaryLight,
                color: theme.colors.primary,
                borderRadius: theme.borderRadius.xs,
                fontSize: theme.typography.fontSize.xs,
                fontWeight: theme.typography.fontWeight.medium,
              }}>
                {product.category}
              </span>

              <p style={{ fontSize: theme.typography.fontSize.md, fontWeight: theme.typography.fontWeight.semibold, color: theme.colors.text, lineHeight: '1.3' }}>
                {product.name}
              </p>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 'auto' }}>
                <div>
                  <span style={{ fontSize: theme.typography.fontSize.lg, fontWeight: theme.typography.fontWeight.bold, color: theme.colors.text }}>
                    ₹{Math.round(product.price_per_hour)}
                  </span>
                  <span style={{ fontSize: theme.typography.fontSize.xs, color: theme.colors.textSecondary }}>/hr</span>
                </div>
                <button
                  onClick={e => { e.stopPropagation(); navigate(`/products/${product.id}`) }}
                  style={{
                    padding: `6px 14px`,
                    backgroundColor: theme.colors.primary,
                    color: theme.colors.white,
                    border: 'none', borderRadius: theme.borderRadius.xs,
                    fontWeight: theme.typography.fontWeight.semibold,
                    fontSize: theme.typography.fontSize.sm, cursor: 'pointer',
                  }}
                >Rent</button>
              </div>
            </div>
          ))}
        </div>
        )}

      </div>
    </div>
  )
}
