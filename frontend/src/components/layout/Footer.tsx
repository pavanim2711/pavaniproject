import React from 'react'
import { Link } from 'react-router'
import { theme } from '@styles/theme'

export function Footer() {
  return (
    <footer style={{
      borderTop: `1px solid ${theme.colors.border}`,
      backgroundColor: theme.colors.white,
      padding: `${theme.spacing.lg} ${theme.spacing.md}`,
    }}>
      <div style={{
        maxWidth: '1280px', margin: '0 auto',
        display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start',
        flexWrap: 'wrap', gap: theme.spacing.lg,
      }}>
        {/* Brand */}
        <div>
          <div style={{ display: 'flex', gap: '4px', marginBottom: theme.spacing.xs }}>
            <span style={{ fontWeight: theme.typography.fontWeight.bold, color: theme.colors.accent, fontSize: theme.typography.fontSize.lg }}>Quick</span>
            <span style={{ fontWeight: theme.typography.fontWeight.bold, color: theme.colors.primary, fontSize: theme.typography.fontSize.lg }}>Tym</span>
          </div>
          <p style={{ color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.sm }}>Rent it. Use it. Return it.</p>
        </div>

        {/* Links */}
        <div style={{ display: 'flex', gap: theme.spacing.xl, flexWrap: 'wrap' }}>
          {[['About', '/about'], ['Contact', '/contact'], ['Privacy Policy', '/privacy'], ['Terms of Service', '/terms']].map(([label, href]) => (
            <Link key={label} to={href} style={{ color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.sm }}>
              {label}
            </Link>
          ))}
        </div>
      </div>
      <div style={{ textAlign: 'center', marginTop: theme.spacing.lg, color: theme.colors.textMuted, fontSize: theme.typography.fontSize.xs }}>
        © {new Date().getFullYear()} Quick Tym. All rights reserved.
      </div>
    </footer>
  )
}
