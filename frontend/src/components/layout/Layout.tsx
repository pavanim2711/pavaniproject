import React from 'react'
import { useLocation } from 'react-router'
import { Header } from './Header'
import { Footer } from './Footer'

interface LayoutProps { children: React.ReactNode }

export function Layout({ children }: LayoutProps) {
  const { pathname } = useLocation()
  const isAuth = pathname === '/login' || pathname === '/register'

  if (isAuth) {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: '#f8f8f8', display: 'flex', flexDirection: 'column' }}>
        {children}
      </div>
    )
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header />
      <main style={{ flex: 1 }}>{children}</main>
      <Footer />
    </div>
  )
}
