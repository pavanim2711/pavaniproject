import React, { useState } from 'react'
import { useParams, useNavigate, useLocation } from 'react-router'
import { theme } from '@styles/theme'

export function RentalCheckout() {
  const { id } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const product = location.state?.product

  const [formData, setFormData] = useState({
    rentalHours: 1,
    startDate: new Date().toISOString().split('T')[0],
    fullName: '',
    email: '',
    phone: '',
    address: '',
    notes: '',
  })

  const [step, setStep] = useState<'details' | 'payment' | 'confirmation'>('details')

  if (!product) {
    return (
      <div style={{ padding: theme.spacing.xl, minHeight: 'calc(100vh - 200px)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <button
            onClick={() => navigate(-1)}
            style={{ background: 'none', border: 'none', color: theme.colors.primary, cursor: 'pointer', marginBottom: theme.spacing.lg, fontSize: theme.typography.fontSize.sm, fontWeight: 'bold' }}
          >
            ← Back
          </button>
          <h1 style={{ color: theme.colors.text }}>Product not found</h1>
        </div>
      </div>
    )
  }

  const pricePerHour = product.price_per_hour || 0
  const totalPrice = pricePerHour * formData.rentalHours

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'rentalHours' ? parseInt(value) : value,
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (step === 'details') {
      setStep('payment')
    } else if (step === 'payment') {
      setStep('confirmation')
    }
  }

  const handleConfirm = () => {
    alert('✅ Booking Confirmed!\n\nRental Order #12345\n\nThank you for using QuickTym!')
    navigate('/')
  }

  return (
    <div style={{ padding: theme.spacing.xl, minHeight: 'calc(100vh - 200px)', backgroundColor: theme.colors.background }}>
      <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
        <button
          onClick={() => navigate(-1)}
          style={{ background: 'none', border: 'none', color: theme.colors.primary, cursor: 'pointer', marginBottom: theme.spacing.lg, fontSize: theme.typography.fontSize.sm, fontWeight: 'bold' }}
        >
          ← Back
        </button>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: theme.spacing.xl }}>
          {/* Left: Product Summary */}
          <div style={{
            backgroundColor: theme.colors.white,
            borderRadius: theme.borderRadius.lg,
            padding: theme.spacing.lg,
            height: 'fit-content',
          }}>
            <h2 style={{ fontSize: theme.typography.fontSize.lg, fontWeight: theme.typography.fontWeight.bold, marginBottom: theme.spacing.md, color: theme.colors.text }}>
              Order Summary
            </h2>

            <img
              src={product.image_url}
              alt={product.name}
              style={{
                width: '100%',
                height: '200px',
                objectFit: 'cover',
                borderRadius: theme.borderRadius.md,
                marginBottom: theme.spacing.md,
              }}
            />

            <h3 style={{ fontWeight: theme.typography.fontWeight.bold, marginBottom: theme.spacing.sm, color: theme.colors.text }}>
              {product.name}
            </h3>

            <div style={{ marginBottom: theme.spacing.lg }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: theme.spacing.sm }}>
                <span style={{ color: theme.colors.textSecondary }}>Price per hour:</span>
                <span style={{ fontWeight: theme.typography.fontWeight.semibold }}>₹{Math.round(pricePerHour)}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: theme.spacing.sm }}>
                <span style={{ color: theme.colors.textSecondary }}>Rental hours:</span>
                <span style={{ fontWeight: theme.typography.fontWeight.semibold }}>{formData.rentalHours} hours</span>
              </div>
              <div style={{ height: '1px', backgroundColor: theme.colors.border, margin: `${theme.spacing.sm} 0` }} />
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ fontWeight: theme.typography.fontWeight.bold, fontSize: theme.typography.fontSize.lg }}>Total:</span>
                <span style={{ fontWeight: theme.typography.fontWeight.bold, fontSize: theme.typography.fontSize.lg, color: theme.colors.primary }}>₹{Math.round(totalPrice)}</span>
              </div>
            </div>

            {/* Step Indicator */}
            <div style={{ display: 'flex', gap: theme.spacing.sm }}>
              <div style={{
                flex: 1,
                height: '4px',
                backgroundColor: step !== 'details' ? theme.colors.primary : theme.colors.border,
                borderRadius: theme.borderRadius.xs,
              }} />
              <div style={{
                flex: 1,
                height: '4px',
                backgroundColor: step === 'confirmation' ? theme.colors.primary : theme.colors.border,
                borderRadius: theme.borderRadius.xs,
              }} />
              <div style={{
                flex: 1,
                height: '4px',
                backgroundColor: step === 'confirmation' ? theme.colors.primary : theme.colors.border,
                borderRadius: theme.borderRadius.xs,
              }} />
            </div>
          </div>

          {/* Right: Form */}
          <div>
            {step === 'details' && (
              <form onSubmit={handleSubmit} style={{
                backgroundColor: theme.colors.white,
                borderRadius: theme.borderRadius.lg,
                padding: theme.spacing.lg,
              }}>
                <h2 style={{ fontSize: theme.typography.fontSize.lg, fontWeight: theme.typography.fontWeight.bold, marginBottom: theme.spacing.lg, color: theme.colors.text }}>
                  Rental Details
                </h2>

                <div style={{ marginBottom: theme.spacing.md }}>
                  <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: theme.typography.fontWeight.semibold, color: theme.colors.text }}>
                    Rental Duration (hours)
                  </label>
                  <input
                    type="number"
                    name="rentalHours"
                    min="1"
                    max="24"
                    value={formData.rentalHours}
                    onChange={handleInputChange}
                    style={{
                      width: '100%',
                      padding: theme.spacing.sm,
                      border: `1px solid ${theme.colors.border}`,
                      borderRadius: theme.borderRadius.sm,
                      fontSize: theme.typography.fontSize.md,
                    }}
                  />
                </div>

                <div style={{ marginBottom: theme.spacing.md }}>
                  <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: theme.typography.fontWeight.semibold, color: theme.colors.text }}>
                    Start Date
                  </label>
                  <input
                    type="date"
                    name="startDate"
                    value={formData.startDate}
                    onChange={handleInputChange}
                    style={{
                      width: '100%',
                      padding: theme.spacing.sm,
                      border: `1px solid ${theme.colors.border}`,
                      borderRadius: theme.borderRadius.sm,
                      fontSize: theme.typography.fontSize.md,
                    }}
                  />
                </div>

                <div style={{ marginBottom: theme.spacing.md }}>
                  <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: theme.typography.fontWeight.semibold, color: theme.colors.text }}>
                    Full Name
                  </label>
                  <input
                    type="text"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleInputChange}
                    required
                    style={{
                      width: '100%',
                      padding: theme.spacing.sm,
                      border: `1px solid ${theme.colors.border}`,
                      borderRadius: theme.borderRadius.sm,
                      fontSize: theme.typography.fontSize.md,
                    }}
                  />
                </div>

                <div style={{ marginBottom: theme.spacing.md }}>
                  <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: theme.typography.fontWeight.semibold, color: theme.colors.text }}>
                    Email
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    style={{
                      width: '100%',
                      padding: theme.spacing.sm,
                      border: `1px solid ${theme.colors.border}`,
                      borderRadius: theme.borderRadius.sm,
                      fontSize: theme.typography.fontSize.md,
                    }}
                  />
                </div>

                <div style={{ marginBottom: theme.spacing.md }}>
                  <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: theme.typography.fontWeight.semibold, color: theme.colors.text }}>
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    required
                    style={{
                      width: '100%',
                      padding: theme.spacing.sm,
                      border: `1px solid ${theme.colors.border}`,
                      borderRadius: theme.borderRadius.sm,
                      fontSize: theme.typography.fontSize.md,
                    }}
                  />
                </div>

                <button
                  type="submit"
                  style={{
                    width: '100%',
                    padding: theme.spacing.md,
                    backgroundColor: theme.colors.primary,
                    color: theme.colors.white,
                    border: 'none',
                    borderRadius: theme.borderRadius.md,
                    fontWeight: theme.typography.fontWeight.bold,
                    fontSize: theme.typography.fontSize.md,
                    cursor: 'pointer',
                  }}
                >
                  Continue to Payment
                </button>
              </form>
            )}

            {step === 'payment' && (
              <form onSubmit={handleSubmit} style={{
                backgroundColor: theme.colors.white,
                borderRadius: theme.borderRadius.lg,
                padding: theme.spacing.lg,
              }}>
                <h2 style={{ fontSize: theme.typography.fontSize.lg, fontWeight: theme.typography.fontWeight.bold, marginBottom: theme.spacing.lg, color: theme.colors.text }}>
                  Payment Details
                </h2>

                <div style={{ marginBottom: theme.spacing.md }}>
                  <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: theme.typography.fontWeight.semibold, color: theme.colors.text }}>
                    Card Number
                  </label>
                  <input
                    type="text"
                    placeholder="1234 5678 9012 3456"
                    style={{
                      width: '100%',
                      padding: theme.spacing.sm,
                      border: `1px solid ${theme.colors.border}`,
                      borderRadius: theme.borderRadius.sm,
                      fontSize: theme.typography.fontSize.md,
                    }}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: theme.spacing.sm, marginBottom: theme.spacing.md }}>
                  <div>
                    <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: theme.typography.fontWeight.semibold, color: theme.colors.text }}>
                      Expiry Date
                    </label>
                    <input
                      type="text"
                      placeholder="MM/YY"
                      style={{
                        width: '100%',
                        padding: theme.spacing.sm,
                        border: `1px solid ${theme.colors.border}`,
                        borderRadius: theme.borderRadius.sm,
                        fontSize: theme.typography.fontSize.md,
                      }}
                    />
                  </div>
                  <div>
                    <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: theme.typography.fontWeight.semibold, color: theme.colors.text }}>
                      CVV
                    </label>
                    <input
                      type="text"
                      placeholder="123"
                      style={{
                        width: '100%',
                        padding: theme.spacing.sm,
                        border: `1px solid ${theme.colors.border}`,
                        borderRadius: theme.borderRadius.sm,
                        fontSize: theme.typography.fontSize.md,
                      }}
                    />
                  </div>
                </div>

                <div style={{ marginBottom: theme.spacing.lg }}>
                  <div style={{
                    padding: theme.spacing.md,
                    backgroundColor: theme.colors.background,
                    borderRadius: theme.borderRadius.sm,
                    marginBottom: theme.spacing.md,
                  }}>
                    <p style={{ color: theme.colors.textSecondary, fontSize: theme.typography.fontSize.sm }}>
                      Total Amount to Pay: <span style={{ fontWeight: theme.typography.fontWeight.bold, color: theme.colors.text }}>₹{Math.round(totalPrice)}</span>
                    </p>
                  </div>
                </div>

                <button
                  type="submit"
                  style={{
                    width: '100%',
                    padding: theme.spacing.md,
                    backgroundColor: theme.colors.primary,
                    color: theme.colors.white,
                    border: 'none',
                    borderRadius: theme.borderRadius.md,
                    fontWeight: theme.typography.fontWeight.bold,
                    fontSize: theme.typography.fontSize.md,
                    cursor: 'pointer',
                  }}
                >
                  Confirm & Pay ₹{Math.round(totalPrice)}
                </button>
              </form>
            )}

            {step === 'confirmation' && (
              <div style={{
                backgroundColor: theme.colors.white,
                borderRadius: theme.borderRadius.lg,
                padding: theme.spacing.lg,
                textAlign: 'center',
              }}>
                <div style={{ fontSize: '48px', marginBottom: theme.spacing.md }}>✅</div>
                <h2 style={{ fontSize: theme.typography.fontSize.lg, fontWeight: theme.typography.fontWeight.bold, marginBottom: theme.spacing.md, color: theme.colors.primary }}>
                  Booking Confirmed!
                </h2>
                <p style={{ color: theme.colors.textSecondary, marginBottom: theme.spacing.md }}>
                  Your rental order has been successfully created.
                </p>

                <div style={{
                  backgroundColor: theme.colors.background,
                  padding: theme.spacing.md,
                  borderRadius: theme.borderRadius.sm,
                  marginBottom: theme.spacing.lg,
                  textAlign: 'left',
                }}>
                  <p style={{ marginBottom: theme.spacing.sm }}><strong>Order ID:</strong> #12345</p>
                  <p style={{ marginBottom: theme.spacing.sm }}><strong>Product:</strong> {product.name}</p>
                  <p style={{ marginBottom: theme.spacing.sm }}><strong>Duration:</strong> {formData.rentalHours} hours</p>
                  <p style={{ marginBottom: theme.spacing.sm }}><strong>Total Amount:</strong> ₹{Math.round(totalPrice)}</p>
                  <p><strong>Status:</strong> Confirmed</p>
                </div>

                <button
                  onClick={handleConfirm}
                  style={{
                    width: '100%',
                    padding: theme.spacing.md,
                    backgroundColor: theme.colors.primary,
                    color: theme.colors.white,
                    border: 'none',
                    borderRadius: theme.borderRadius.md,
                    fontWeight: theme.typography.fontWeight.bold,
                    fontSize: theme.typography.fontSize.md,
                    cursor: 'pointer',
                  }}
                >
                  Back to Home
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
