import api from './api'

export interface Product {
  id: string
  name: string
  description: string
  category: string
  price_per_hour: number
  min_rental_hours: number
  max_rental_hours: number
  specifications: Record<string, any>
  features: string[]
  image_url: string
  gallery_urls: string[]
  availability: {
    is_available: boolean
    available_from: string | null
    available_until: string | null
  }
  location: string
  rating: number
  review_count: number
  created_at: string
}

export interface ProductFilter {
  category?: string
  min_price?: number
  max_price?: number
  location?: string
  availability?: 'available' | 'unavailable'
}

export const productService = {
  getAllProducts: async (filters?: ProductFilter) => {
    const params = new URLSearchParams()
    if (filters?.category) params.append('category', filters.category)
    if (filters?.min_price) params.append('min_price', filters.min_price.toString())
    if (filters?.max_price) params.append('max_price', filters.max_price.toString())
    if (filters?.location) params.append('location', filters.location)
    if (filters?.availability) params.append('availability', filters.availability)

    const response = await api.get('/products', { params })
    return response.data
  },

  getProductById: async (id: string) => {
    const response = await api.get(`/products/${id}`)
    return response.data
  },

  searchProducts: async (query: string) => {
    const response = await api.get('/products/search', { params: { q: query } })
    return response.data
  },
}
