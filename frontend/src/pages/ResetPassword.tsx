import React, { useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router'
import { theme } from '@styles/theme'

export function ResetPassword() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token') || ''
  const email = searchParams.get('email') || ''
  
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match')
      return
    }
    
    if (newPassword.length < 8) {
      setError('Password must be at least 8 characters')
      return
    }
    
    setLoading(true)
    try {
      const apiURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
      const res = await fetch(`${apiURL}/auth/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, token, new_password: newPassword }),
      })
      if (!res.ok) throw new Error('Failed to reset password')
      setSuccess(true)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to reset password')
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
            <div style={{ fontSize: '48px', marginBottom: theme.spacing.md }}>🔒</div>
            <h2 style={{ fontSize: theme.typography.fontSize.xl, fontWeight: theme.typography.fontWeight.bold, color: theme.colors.text, marginBottom: theme.spacing.sm }}>
              Password Reset!
            </h2>
            <p style={{ color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.md, marginBottom: theme.spacing.lg }}>
              Your password has been successfully reset. You can now login with your new password.
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
              Go to Login
            </button>
          </div>
        ) : (
          <>
            <h2 style={{ fontSize: theme.typography.fontSize.xl, fontWeight: theme.typography.fontWeight.bold, color: theme.colors.text, marginBottom: theme.spacing.lg }}>
              Reset Password
            </h2>
            <p style={{ color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.md, marginBottom: theme.spacing.lg }}>
              Enter your new password below.
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
              <input type="hidden" value={email} />
              <input type="hidden" value={token} />
              
              <div>
                <label style={{ display: 'block', marginBottom: '6px', fontSize: theme.typography.fontSize.sm, fontWeight: theme.typography.fontWeight.medium, color: theme.colors.text }}>
                  New Password
                </label>
                <input 
                  type="password" 
                  value={newPassword} 
                  onChange={e => setNewPassword(e.target.value)} 
                  required 
                  style={inp} 
                  placeholder="New password (min 8 characters)"
                  minLength={8}
                />
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '6px', fontSize: theme.typography.fontSize.sm, fontWeight: theme.typography.fontWeight.medium, color: theme.colors.text }}>
                  Confirm Password
                </label>
                <input 
                  type="password" 
                  value={confirmPassword} 
                  onChange={e => setConfirmPassword(e.target.value)} 
                  required 
                  style={inp} 
                  placeholder="Confirm your new password"
                  minLength={8}
                />
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
                {loading ? 'Resetting...' : 'Reset Password'}
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  )
}