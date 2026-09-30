import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router'
import { useAuth } from '@contexts/AuthContext'
import { theme } from '@styles/theme'

export function Header() {
  const { user, isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()
  const [search, setSearch] = useState('')

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (search.trim()) navigate(`/products?q=${encodeURIComponent(search.trim())}`)
  }

  return (
    <header style={{
      position: 'sticky', top: 0, zIndex: 200,
      backgroundColor: theme.colors.white,
      borderBottom: `1px solid ${theme.colors.border}`,
      boxShadow: theme.shadows.xs,
    }}>
      <div style={{
        maxWidth: '1280px', margin: '0 auto',
        padding: `0 ${theme.spacing.md}`,
        height: '64px',
        display: 'flex', alignItems: 'center', gap: theme.spacing.md,
      }}>

        {/* Logo */}
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '6px', flexShrink: 0 }}>
          <span style={{
            fontSize: '26px', fontWeight: theme.typography.fontWeight.bold,
            color: theme.colors.accent, letterSpacing: '-1px',
          }}>Quick</span>
          <span style={{
            fontSize: '26px', fontWeight: theme.typography.fontWeight.bold,
            color: theme.colors.primary, letterSpacing: '-1px',
          }}>Tym</span>
        </Link>

        {/* Location chip */}
        <div style={{
          display: 'flex', flexDirection: 'column',
          borderLeft: `1px solid ${theme.colors.border}`,
          paddingLeft: theme.spacing.md, flexShrink: 0,
        }}>
          <span style={{ fontSize: theme.typography.fontSize.sm, fontWeight: theme.typography.fontWeight.bold, color: theme.colors.text }}>
            Delivery in 30 min
          </span>
          <span style={{ fontSize: theme.typography.fontSize.xs, color: theme.colors.textSecondary }}>
            Bengaluru, KA ▾
          </span>
        </div>

        {/* Search bar */}
        <form onSubmit={handleSearch} style={{ flex: 1, maxWidth: '600px' }}>
          <div style={{ position: 'relative' }}>
            <span style={{
              position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)',
              color: theme.colors.textMuted, fontSize: '16px', pointerEvents: 'none',
            }}>🔍</span>
            <input
              type="text"
              placeholder='Search "tent" or "camera"'
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{
                width: '100%',
                padding: `10px 12px 10px 36px`,
                borderRadius: theme.borderRadius.sm,
                border: `1px solid ${theme.colors.border}`,
                backgroundColor: theme.colors.background,
                fontSize: theme.typography.fontSize.base,
                color: theme.colors.text,
                outline: 'none',
              }}
            />
          </div>
        </form>

        {/* Nav actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: theme.spacing.sm, marginLeft: 'auto', flexShrink: 0 }}>
          {isAuthenticated && user ? (
            <>
              <span style={{ fontSize: theme.typography.fontSize.sm, color: theme.colors.textSecondary }}>
                Hi, {user.name.split(' ')[0]}
              </span>
              <button
                onClick={logout}
                style={{
                  padding: `8px ${theme.spacing.md}`,
                  border: `1px solid ${theme.colors.border}`,
                  borderRadius: theme.borderRadius.sm,
                  background: 'none',
                  cursor: 'pointer',
                  fontSize: theme.typography.fontSize.sm,
                  color: theme.colors.text,
                }}
              >Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" style={{
                padding: `8px ${theme.spacing.md}`,
                fontSize: theme.typography.fontSize.md,
                fontWeight: theme.typography.fontWeight.medium,
                color: theme.colors.text,
              }}>Login</Link>
              <Link to="/register" style={{
                padding: `9px ${theme.spacing.md}`,
                backgroundColor: theme.colors.primary,
                color: theme.colors.white,
                borderRadius: theme.borderRadius.sm,
                fontSize: theme.typography.fontSize.md,
                fontWeight: theme.typography.fontWeight.semibold,
              }}>Sign Up</Link>
            </>
          )}

          {/* Cart */}
          <button
            onClick={() => navigate('/cart')}
            style={{
              display: 'flex', alignItems: 'center', gap: '6px',
              padding: `9px ${theme.spacing.md}`,
              backgroundColor: theme.colors.primary,
              color: theme.colors.white,
              border: 'none', borderRadius: theme.borderRadius.sm,
              cursor: 'pointer',
              fontSize: theme.typography.fontSize.md,
              fontWeight: theme.typography.fontWeight.semibold,
            }}
          >
            🛒 My Cart
          </button>
        </div>
      </div>
    </header>
  )
}
