import React, { useState } from 'react'
import { useNavigate } from 'react-router'
import { theme } from '@styles/theme'

export function ForgotPassword() {
  const [email, setEmail] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const apiURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
      const res = await fetch(`${apiURL}/auth/forgot-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      })
      if (!res.ok) throw new Error('Failed to send reset email')
      const data = await res.json()
      // For MVP testing, log the reset token
      console.log('Reset token:', data.token_for_mvp_testing)
      setSuccess(true)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to send reset email')
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

        {success ? (
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '48px', marginBottom: theme.spacing.md }}>📧</div>
            <h2 style={{ fontSize: theme.typography.fontSize.xl, fontWeight: theme.typography.fontWeight.bold, color: theme.colors.text, marginBottom: theme.spacing.sm }}>
              Reset Link Sent!
            </h2>
            <p style={{ color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.md, marginBottom: theme.spacing.lg }}>
              We've sent a password reset link to {email}. Please check your email for further instructions.
            </p>
            <button
              onClick={() => navigate('/login')}
              style={{
                padding: '12px 24px', backgroundColor: theme.colors.primary,
                color: theme.colors.white, border: 'none',
                borderRadius: theme.borderRadius.sm,
                fontWeight: theme.typography.fontWeight.bold,
                fontSize: theme.typography.fontSize.md,
                cursor: 'pointer',
              }}
            >
              Back to Login
            </button>
          </div>
        ) : (
          <>
            <h2 style={{ fontSize: theme.typography.fontSize.xl, fontWeight: theme.typography.fontWeight.bold, color: theme.colors.text, marginBottom: theme.spacing.lg }}>
              Forgot Password?
            </h2>
            <p style={{ color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.md, marginBottom: theme.spacing.lg }}>
              Enter your email address and we'll send you instructions to reset your password.
            </p>

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
                {loading ? 'Sending...' : 'Send Reset Link'}
              </button>
            </form>

            <p style={{ textAlign: 'center', marginTop: theme.spacing.lg, color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.sm }}>
              Remember your password?{' '}
              <button onClick={() => navigate('/login')} style={{ color: theme.colors.primary, fontWeight: theme.typography.fontWeight.semibold, border: 'none', backgroundColor: 'transparent', cursor: 'pointer' }}>
                Login here
              </button>
            </p>
          </>
        )}
      </div>
    </div>
  )
}