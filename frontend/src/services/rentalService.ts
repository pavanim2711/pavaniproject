import api from './api'

export interface RentalSession {
  id: string
  user_id: string
  product_id: string
  status: 'pending' | 'active' | 'completed' | 'cancelled' | 'overdue' | 'paid'
  start_time: string | null
  end_time: string | null
  total_seconds: number | null
  billable_seconds: number | null
  base_amount: number
  tax_amount: number
  delivery_fee: number
  cleaning_fee: number
  security_deposit: number
  deposit_returned: boolean
  total_amount: number
  location: string
  delivery_address: Record<string, any>
  pickup_address: Record<string, any> | null
  created_at: string
  updated_at: string
}

export interface RentalRequest {
  product_id: string
  location: string
  delivery_address: Record<string, any>
  pickup_address?: Record<string, any>
}

export const rentalService = {
  createRentalSession: async (data: RentalRequest) => {
    const response = await api.post('/rentals', data)
    return response.data
  },

  getRentalSession: async (id: string) => {
    const response = await api.get(`/rentals/${id}`)
    return response.data
  },

  getRentalSessionByProduct: async (productId: string) => {
    const response = await api.get(`/rentals/product/${productId}`)
    return response.data
  },

  requestPickup: async (rentalId: string) => {
    const response = await api.post(`/rentals/${rentalId}/pickup`)
    return response.data
  },

  extendRental: async (rentalId: string, additional_hours: number) => {
    const response = await api.post(`/rentals/${rentalId}/extend`, { additional_hours })
    return response.data
  },
}
