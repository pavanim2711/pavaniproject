# Utils, Hooks & Banners Setup

**Date:** August 14, 2026  
**Status:** ✅ Complete

---

## 📁 What Was Created

### 1. Utility Functions (`/frontend/src/utils/`)

#### **formatters.ts** - Data Formatting
- `formatPrice()` - Convert to ₹ format
- `formatDate()` - Human-readable dates
- `formatTime()` - Human-readable times
- `formatDateTime()` - Combined date & time
- `formatDuration()` - Convert hours to readable format
- `truncateText()` - Shorten long text
- `capitalize()` - Capitalize words
- `formatCategoryName()` - Format category names
- And more...

**Usage:**
```typescript
import { formatPrice, formatDate } from '@utils/formatters'

const price = formatPrice(150)  // ₹150
const date = formatDate(new Date())  // 14 Aug 2026
```

#### **validators.ts** - Input Validation
- `isValidEmail()` - Validate email
- `isValidPassword()` - Check password strength
- `isValidPhoneNumber()` - Validate phone
- `isEmpty()` - Check if empty
- `isValidPrice()` - Price in ₹50-₹500 range
- `isFutureDate()` - Check if date is future
- `isValidUrl()` - Validate URLs
- `validateForm()` - Validate entire form
- And more...

**Usage:**
```typescript
import { isValidEmail, validateForm } from '@utils/validators'

if (isValidEmail(email)) {
  // Process valid email
}

const { valid, errors } = validateForm({
  email: 'user@example.com',
  password: 'Pass123'
})
```

#### **helpers.ts** - General Utilities
- `getQueryParam()` - Get URL parameters
- `setQueryParam()` - Set URL parameters
- `deepClone()` - Deep copy objects
- `debounce()` - Debounce functions
- `throttle()` - Throttle functions
- `retry()` - Retry async operations
- `sleep()` - Sleep/delay
- `generateId()` - Generate random IDs
- `arrayDifference()` - Array operations
- `groupBy()` - Group array by key
- `sortBy()` - Sort array
- And more...

**Usage:**
```typescript
import { debounce, groupBy, sortBy } from '@utils/helpers'

const debouncedSearch = debounce(handleSearch, 300)
const grouped = groupBy(products, 'category')
const sorted = sortBy(users, 'name', true)
```

### 2. Custom Hooks (`/frontend/src/hooks/`)

#### **useAuth.ts** - Authentication Management
```typescript
const { user, token, isAuthenticated, login, logout } = useAuth()

// Login
login(userData, authToken)

// Logout
logout()

// Update user info
updateUser({ name: 'John' })
```

**Features:**
- Persist auth state to localStorage
- Auto-load from localStorage on mount
- Manage user & token
- Login/logout functions

#### **useFetch.ts** - API Data Fetching
```typescript
const { data, loading, error, refetch } = useFetch<Product[]>('/api/products')

if (loading) return <p>Loading...</p>
if (error) return <p>Error: {error.message}</p>
return <div>{data?.map(p => <div>{p.name}</div>)}</div>

// Refetch data
await refetch()
```

**Features:**
- Automatic data fetching
- Loading & error states
- Manual refetch capability
- Type-safe with generics

#### **useForm.ts** - Form Management
```typescript
const { values, errors, handleChange, handleSubmit } = useForm(
  { email: '', password: '' },
  async (values) => {
    await loginUser(values)
  }
)

return (
  <form onSubmit={handleSubmit}>
    <input name="email" value={values.email} onChange={handleChange} />
    {errors.email && <span>{errors.email}</span>}
    <button type="submit">Login</button>
  </form>
)
```

**Features:**
- Form state management
- Validation error tracking
- Submit handling
- Field-level control

#### **useLocalStorage.ts** - Browser Storage
```typescript
const [favorites, setFavorites] = useLocalStorage<Product[]>('favorites', [])

// Read from localStorage
console.log(favorites)

// Write to localStorage
setFavorites([...favorites, newProduct])
```

**Features:**
- Sync state with localStorage
- Type-safe storage
- Auto-persistence
- Default values

### 3. Banners Setup (`/frontend/public/banners/`)

#### README with instructions for:
- Where to add banner images
- Recommended banner sizes
- File format recommendations
- Free stock image resources

---

## 🚀 How to Use

### Example 1: Format and Display Product
```typescript
import { formatPrice, formatCategoryName } from '@utils'

export function ProductCard({ product }) {
  return (
    <div>
      <h2>{product.name}</h2>
      <p>{formatCategoryName(product.category)}</p>
      <span>{formatPrice(product.price_per_hour)}</span>
    </div>
  )
}
```

### Example 2: Validate and Submit Form
```typescript
import { useForm } from '@hooks'
import { isValidEmail } from '@utils'

export function LoginForm() {
  const { values, errors, handleChange, handleSubmit } = useForm(
    { email: '', password: '' },
    async (values) => {
      if (!isValidEmail(values.email)) {
        alert('Invalid email')
        return
      }
      // Call API
    }
  )

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" value={values.email} onChange={handleChange} />
      <input name="password" type="password" value={values.password} onChange={handleChange} />
      <button type="submit">Login</button>
    </form>
  )
}
```

### Example 3: Fetch Data with Loading State
```typescript
import { useFetch } from '@hooks'

export function ProductList() {
  const { data: products, loading, error } = useFetch('/api/v1/products/')

  if (loading) return <p>Loading products...</p>
  if (error) return <p>Error loading products</p>
  
  return (
    <div>
      {products?.map(p => (
        <div key={p.id}>{p.name}</div>
      ))}
    </div>
  )
}
```

### Example 4: Save User Preferences
```typescript
import { useLocalStorage } from '@hooks'

export function UserPreferences() {
  const [theme, setTheme] = useLocalStorage('theme', 'light')
  const [language, setLanguage] = useLocalStorage('language', 'en')

  return (
    <div>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Switch Theme
      </button>
    </div>
  )
}
```

---

## 📊 Files Created

```
frontend/src/
├── utils/
│   ├── index.ts              ← Central exports
│   ├── formatters.ts         ← 13 formatting functions
│   ├── validators.ts         ← 13 validation functions
│   └── helpers.ts            ← 18 helper functions
│
└── hooks/
    ├── index.ts              ← Central exports
    ├── useAuth.ts            ← Authentication management
    ├── useFetch.ts           ← API data fetching
    ├── useForm.ts            ← Form handling
    └── useLocalStorage.ts    ← Browser storage

frontend/public/
└── banners/
    └── README.md             ← Banner setup guide

Total: 44+ utility functions, 4 custom hooks
```

---

## ✅ Features Summary

| Category | Count | Examples |
|----------|-------|----------|
| Formatters | 13 | Price, Date, Time, Duration |
| Validators | 13 | Email, Password, Phone, Price |
| Helpers | 18 | Debounce, Throttle, Array ops |
| Hooks | 4 | Auth, Fetch, Form, Storage |

---

## 🎯 Next Steps

1. **Use in your components** - Import and use utilities
2. **Add banner images** - Follow the README in `/public/banners/`
3. **Extend as needed** - Add more utilities based on requirements

---

## 📚 Quick Import Reference

```typescript
// Utils
import { formatPrice, formatDate, isValidEmail } from '@utils'

// Hooks
import { useAuth, useFetch, useForm, useLocalStorage } from '@hooks'

// Or individual imports
import { useAuth } from '@hooks/useAuth'
import { formatPrice } from '@utils/formatters'
```

---

**Status:** ✅ Ready to use in your application!
