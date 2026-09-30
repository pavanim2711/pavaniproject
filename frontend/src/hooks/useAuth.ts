import { useState, useEffect, useCallback } from 'react'

interface User {
  id: string
  email: string
  name?: string
  role?: 'customer' | 'partner' | 'admin'
}

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
  isAuthenticated: boolean
}

/**
 * Custom hook for authentication management
 * Handles login, logout, and auth state
 */
export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    isLoading: true,
    isAuthenticated: false,
  })

  // Initialize auth state from localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')

    if (storedToken && storedUser) {
      try {
        setAuthState({
          user: JSON.parse(storedUser),
          token: storedToken,
          isLoading: false,
          isAuthenticated: true,
        })
      } catch (error) {
        console.error('Failed to parse stored auth data:', error)
        setAuthState(prev => ({ ...prev, isLoading: false }))
      }
    } else {
      setAuthState(prev => ({ ...prev, isLoading: false }))
    }
  }, [])

  const login = useCallback((user: User, token: string) => {
    localStorage.setItem('user', JSON.stringify(user))
    localStorage.setItem('token', token)
    setAuthState({
      user,
      token,
      isLoading: false,
      isAuthenticated: true,
    })
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    setAuthState({
      user: null,
      token: null,
      isLoading: false,
      isAuthenticated: false,
    })
  }, [])

  const updateUser = useCallback((user: Partial<User>) => {
    setAuthState(prev => ({
      ...prev,
      user: prev.user ? { ...prev.user, ...user } : null,
    }))
    if (authState.user) {
      localStorage.setItem('user', JSON.stringify({ ...authState.user, ...user }))
    }
  }, [authState.user])

  return {
    ...authState,
    login,
    logout,
    updateUser,
  }
}
