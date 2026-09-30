import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router'
import { theme } from '@styles/theme'

export function LoginPage() {
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')
  const [error, setError]       = useState<string | null>(null)
  const [loading, setLoading]   = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const res = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      if (!res.ok) throw new Error('Invalid email or password')
      const data = await res.json()
      localStorage.setItem('token', data.access_token)
      navigate('/')
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const inp: React.CSSProperties = {
    width: '100%', padding: '11px 14px',
    border: `1.5px solid ${theme.colors.border}`,
    borderRadius: theme.borderRadius.sm,
    fontSize: theme.typography.fontSize.md,
    color: theme.colors.text, outline: 'none',
    backgroundColor: theme.colors.white,
    transition: 'border-color 0.2s',
    boxSizing: 'border-box',
  }

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      backgroundColor: theme.colors.background, padding: theme.spacing.md,
    }}>
      <div style={{
        width: '100%', maxWidth: '420px',
        backgroundColor: theme.colors.white,
        borderRadius: theme.borderRadius.lg,
        boxShadow: theme.shadows.md,
        padding: theme.spacing.xl,
      }}>
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: theme.spacing.lg }}>
          <div style={{ display: 'inline-flex', gap: '4px', marginBottom: '4px' }}>
            <span style={{ fontSize: '28px', fontWeight: theme.typography.fontWeight.bold, color: theme.colors.accent }}>Quick</span>
            <span style={{ fontSize: '28px', fontWeight: theme.typography.fontWeight.bold, color: theme.colors.primary }}>Tym</span>
          </div>
          <p style={{ color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.sm }}>Rent it. Use it. Return it.</p>
        </div>

        <h2 style={{ fontSize: theme.typography.fontSize.xl, fontWeight: theme.typography.fontWeight.bold, color: theme.colors.text, marginBottom: theme.spacing.lg }}>
          Login to your account
        </h2>

        {error && (
          <div style={{
            backgroundColor: '#fff0f0', border: `1px solid ${theme.colors.danger}`,
            borderRadius: theme.borderRadius.sm, padding: theme.spacing.sm,
            marginBottom: theme.spacing.md, color: theme.colors.danger,
            fontSize: theme.typography.fontSize.sm,
          }}>{error}</div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: theme.spacing.md }}>
          <div>
            <label style={{ display: 'block', marginBottom: '6px', fontSize: theme.typography.fontSize.sm, fontWeight: theme.typography.fontWeight.medium, color: theme.colors.text }}>
              Email address
            </label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={inp} placeholder="you@example.com" />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '6px', fontSize: theme.typography.fontSize.sm, fontWeight: theme.typography.fontWeight.medium, color: theme.colors.text }}>
              Password
            </label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={inp} placeholder="Your password" />
          </div>
          <button
            type="submit"
            disabled={loading}
            style={{
              padding: '12px', backgroundColor: theme.colors.primary,
              color: theme.colors.white, border: 'none',
              borderRadius: theme.borderRadius.sm,
              fontWeight: theme.typography.fontWeight.bold,
              fontSize: theme.typography.fontSize.md,
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.7 : 1, marginTop: '4px',
            }}
          >
            {loading ? 'Logging in…' : 'Login'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: theme.spacing.lg, color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.sm }}>
          New to Quick Tym?{' '}
          <Link to="/register" style={{ color: theme.colors.primary, fontWeight: theme.typography.fontWeight.semibold }}>
            Create account
          </Link>
        </p>
        
        <p style={{ textAlign: 'center', marginTop: theme.spacing.md, color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.sm }}>
          <Link to="/forgot-password" style={{ color: theme.colors.primary, fontWeight: theme.typography.fontWeight.semibold }}>
            Forgot password?
          </Link>
        </p>
      </div>
    </div>
  )
}
