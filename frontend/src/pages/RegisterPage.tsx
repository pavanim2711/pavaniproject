import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router'
import { theme } from '@styles/theme'

export function RegisterPage() {
  const [name, setName]         = useState('')
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole]         = useState('Customer')
  const [error, setError]       = useState<string | null>(null)
  const [loading, setLoading]   = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const res = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, role }),
      })
      if (!res.ok) {
        const d = await res.json()
        throw new Error(d.detail || 'Registration failed')
      }
      navigate('/login')
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Registration failed')
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
    boxSizing: 'border-box',
  }
  const lbl: React.CSSProperties = {
    display: 'block', marginBottom: '6px',
    fontSize: theme.typography.fontSize.sm,
    fontWeight: theme.typography.fontWeight.medium,
    color: theme.colors.text,
  }

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      backgroundColor: theme.colors.background, padding: theme.spacing.md,
    }}>
      <div style={{
        width: '100%', maxWidth: '440px',
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
          Create your account
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
            <label style={lbl}>Full name</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} required style={inp} placeholder="John Doe" />
          </div>
          <div>
            <label style={lbl}>Email address</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={inp} placeholder="you@example.com" />
          </div>
          <div>
            <label style={lbl}>Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={inp} placeholder="Min 8 chars, A-Z, a-z, 0-9" />
          </div>
          <div>
            <label style={lbl}>I want to</label>
            <div style={{ display: 'flex', gap: theme.spacing.sm }}>
              {[['Customer', 'Rent products 🛒'], ['Delivery_Partner', 'Deliver products 🛵']].map(([val, label]) => (
                <button
                  key={val}
                  type="button"
                  onClick={() => setRole(val)}
                  style={{
                    flex: 1, padding: '10px 8px',
                    border: `2px solid ${role === val ? theme.colors.primary : theme.colors.border}`,
                    borderRadius: theme.borderRadius.sm,
                    backgroundColor: role === val ? theme.colors.primaryLight : theme.colors.white,
                    color: role === val ? theme.colors.primary : theme.colors.text,
                    fontWeight: theme.typography.fontWeight.medium,
                    fontSize: theme.typography.fontSize.sm, cursor: 'pointer',
                    transition: 'all 0.15s',
                  }}
                >{label}</button>
              ))}
            </div>
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
            {loading ? 'Creating account…' : 'Create account'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: theme.spacing.lg, color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.sm }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: theme.colors.primary, fontWeight: theme.typography.fontWeight.semibold }}>
            Login
          </Link>
        </p>
      </div>
    </div>
  )
}
