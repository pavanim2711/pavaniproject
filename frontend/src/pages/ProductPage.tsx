import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router'
import { theme } from '@styles/theme'
import { productService, Product } from '@services/productService'

const FALLBACK_PRODUCTS = [
  { id: 1, name: 'Camping Tent (4-person)', price_per_hour: 150, category: 'Outdoor', image_url: '/images/tent.jfif', description: 'Professional 4-person camping tent with waterproof fabric and easy setup. Perfect for outdoor adventures.' },
  { id: 2, name: 'Portable Bluetooth Speaker', price_per_hour: 80, category: 'Party', image_url: '/images/bluetooth speaker.jfif', description: 'High-quality portable speaker with 12-hour battery life. Great for parties and outdoor events.' },
  { id: 3, name: 'Power Drill Set', price_per_hour: 100, category: 'Tools', image_url: '/images/electric-drill-500x500.webp', description: 'Complete power drill set with multiple bits and accessories. Perfect for DIY projects.' },
  { id: 4, name: 'Trekking Backpack 60L', price_per_hour: 120, category: 'Outdoor', image_url: '/images/images.jfif', description: 'Spacious 60L hiking backpack with ergonomic design and multiple compartments.' },
  { id: 5, name: 'Folding Table (6-seater)', price_per_hour: 90, category: 'Party', image_url: '/images/folding table.webp', description: 'Portable folding table perfect for parties, picnics, and events.' },
  { id: 6, name: 'Ladder 8ft Aluminium', price_per_hour: 70, category: 'Tools', image_url: '/images/ladder.jpg', description: 'Sturdy 8-foot aluminum ladder suitable for various household projects.' },
  { id: 7, name: 'Action Camera + Mounts', price_per_hour: 200, category: 'Travel', image_url: '/images/action camera.jfif', description: 'Professional action camera with various mounting accessories for adventure videos.' },
  { id: 8, name: 'Badminton Set (full)', price_per_hour: 60, category: 'Sports', image_url: '/images/badmiton set.avif', description: 'Complete badminton set with rackets, shuttlecocks, and net.' }
]

export function ProductPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [product, setProduct] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (id) {
      fetchProduct(id)
    }
  }, [id])

  const fetchProduct = async (productId: string) => {
    try {
      setLoading(true)
      setError(null)
      const data = await productService.getProductById(productId)
      
      // Validate that we got valid data
      if (data && data.name && data.price_per_hour !== undefined) {
        setProduct(data)
      } else {
        // Fallback to mock data if API returns invalid data
        const fallbackId = parseInt(productId.replace('prod-', ''))
        const fallback = FALLBACK_PRODUCTS.find(p => p.id === fallbackId)
        if (fallback) {
          setProduct(fallback)
        } else {
          setError('Product not found')
        }
      }
    } catch (err) {
      console.error('Error fetching product:', err)
      // Fallback to mock data
      const fallbackId = parseInt(productId.replace('prod-', ''))
      const fallback = FALLBACK_PRODUCTS.find(p => p.id === fallbackId)
      if (fallback) {
        setProduct(fallback)
      } else {
        setError('Product not found')
      }
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div style={{ padding: theme.spacing.xl, minHeight: 'calc(100vh - 200px)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <p style={{ color: theme.colors.textSecondary }}>Loading product...</p>
      </div>
    )
  }

  if (error || !product) {
    return (
      <div style={{ padding: theme.spacing.xl, minHeight: 'calc(100vh - 200px)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <button
            onClick={() => navigate(-1)}
            style={{ background: 'none', border: 'none', color: theme.colors.primary, cursor: 'pointer', marginBottom: theme.spacing.lg, fontSize: theme.typography.fontSize.sm, fontWeight: 'bold' }}
          >
            ← Back
          </button>
          <h1 style={{ color: theme.colors.text }}>Product not found</h1>
        </div>
      </div>
    )
  }

  const price = product.price_per_hour ? Math.round(product.price_per_hour) : 0

  return (
    <div style={{ padding: theme.spacing.xl, minHeight: 'calc(100vh - 200px)', backgroundColor: theme.colors.background }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <button
          onClick={() => navigate(-1)}
          style={{ background: 'none', border: 'none', color: theme.colors.primary, cursor: 'pointer', marginBottom: theme.spacing.lg, fontSize: theme.typography.fontSize.sm, fontWeight: 'bold' }}
        >
          ← Back
        </button>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: theme.spacing.xl, alignItems: 'start' }}>
          {/* Product Image */}
          <div style={{
            backgroundColor: theme.colors.white,
            borderRadius: theme.borderRadius.lg,
            padding: theme.spacing.lg,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '400px',
          }}>
            <img
              src={product.image_url}
              alt={product.name}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                borderRadius: theme.borderRadius.md,
                maxHeight: '400px',
              }}
              onError={(e) => {
                e.currentTarget.style.display = 'none'
              }}
            />
          </div>

          {/* Product Details */}
          <div>
            <span style={{
              display: 'inline-block',
              padding: '4px 12px',
              backgroundColor: theme.colors.primaryLight,
              color: theme.colors.primary,
              borderRadius: theme.borderRadius.sm,
              fontSize: theme.typography.fontSize.sm,
              fontWeight: theme.typography.fontWeight.semibold,
              marginBottom: theme.spacing.md,
            }}>
              {product.category}
            </span>

            <h1 style={{ 
              fontSize: theme.typography.fontSize['3xl'], 
              fontWeight: theme.typography.fontWeight.bold, 
              color: theme.colors.text,
              marginBottom: theme.spacing.md,
              lineHeight: '1.2'
            }}>
              {product.name}
            </h1>

            <div style={{
              display: 'flex',
              alignItems: 'baseline',
              gap: theme.spacing.sm,
              marginBottom: theme.spacing.lg,
            }}>
              <span style={{
                fontSize: theme.typography.fontSize['2xl'],
                fontWeight: theme.typography.fontWeight.bold,
                color: theme.colors.primary,
              }}>
                ₹{price}
              </span>
              <span style={{
                fontSize: theme.typography.fontSize.md,
                color: theme.colors.textSecondary,
              }}>
                per hour
              </span>
            </div>

            <p style={{
              fontSize: theme.typography.fontSize.md,
              color: theme.colors.text,
              lineHeight: '1.6',
              marginBottom: theme.spacing.lg,
            }}>
              {product.description}
            </p>

            <div style={{
              backgroundColor: theme.colors.white,
              padding: theme.spacing.lg,
              borderRadius: theme.borderRadius.md,
              marginBottom: theme.spacing.lg,
              border: `1px solid ${theme.colors.border}`,
            }}>
              <h3 style={{ fontWeight: theme.typography.fontWeight.bold, marginBottom: theme.spacing.sm, color: theme.colors.text }}>
                Availability
              </h3>
              <p style={{ color: theme.colors.textSecondary }}>
                {product.availability?.is_available ? 'Available for daily rental' : 'Currently unavailable'}
              </p>
            </div>

            <button
              onClick={() => navigate(`/checkout/${product.id}`, { state: { product } })}
              style={{
                width: '100%',
                padding: `${theme.spacing.md} ${theme.spacing.xl}`,
                backgroundColor: theme.colors.primary,
                color: theme.colors.white,
                border: 'none',
                borderRadius: theme.borderRadius.md,
                fontSize: theme.typography.fontSize.md,
                fontWeight: theme.typography.fontWeight.bold,
                cursor: 'pointer',
              }}
            >
              Rent Now - ₹{price}/hour
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
