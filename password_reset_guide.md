# Password Reset System - Quick Tym

## Overview

Quick Tym implements a secure password management system with the following features:

### What You Can Do (Without Password Retrieval)

1. **View User Details** - Email, name, role, phone number (password NOT stored in readable form)
2. **Reset User Password** - Through the forgot password flow
3. **Change Password** - For authenticated users

### Password Storage

Passwords are stored using **bcrypt hashing** (one-way encryption):
- Hashed with 12 rounds of bcrypt
- Never stored in plain text
- Cannot be decrypted or retrieved

## Available Endpoints

### 1. Forgot Password (`/api/v1/auth/forgot-password`)
```
POST /api/v1/auth/forgot-password
Body: {"email": "user@example.com"}

Response:
{
  "message": "If email exists, reset instructions have been sent",
  "token_for_mvp_testing": "reset_token_here"  // Remove in production
}
```

### 2. Reset Password (`/api/v1/auth/reset-password`)
```
POST /api/v1/auth/reset-password
Body: {
  "email": "user@example.com",
  "token": "reset_token",
  "new_password": "new_secure_password"
}

Response:
{
  "message": "Password reset successfully"
}
```

## How Users Can Reset Forgotten Password

### Step 1: Request Reset
User enters their email address on the frontend:
```
POST http://localhost:8000/api/v1/auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}
```

The system:
- Checks if email exists (doesn't reveal if user exists)
- Generates a secure reset token
- Logs the token (in production, sends email)

### Step 2: Reset Password
User receives reset token and enters new password:
```
POST http://localhost:8000/api/v1/auth/reset-password
Content-Type: application/json

{
  "email": "user@example.com",
  "token": "token_received",
  "new_password": "MyNewPassword123!"
}
```

## Testing the Password Reset Flow

### Test via API

**Request Password Reset:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/forgot-password" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"email":"test@example.com"}'
```

**Reset Password:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/reset-password" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{
    "email": "test@example.com",
    "token": "token_from_forgot_password",
    "new_password": "NewSecurePassword123!"
  }'
```

### Test via Swagger UI
1. Navigate to: http://localhost:8000/docs
2. Expand "Authentication" section
3. Use the "POST /api/v1/auth/forgot-password" and "POST /api/v1/auth/reset-password" endpoints

## Security Notes

1. **Password Hashing**: All passwords use bcrypt with 12 rounds
2. **Token Security**: Reset tokens are 32-character secure random strings
3. **Email Privacy**: System doesn't reveal if email exists (prevents email enumeration)
4. **Token Validation**: Token must be at least 32 characters (MVP basic check)

## Frontend Integration

### Forgot Password Page
```tsx
const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await fetch("/api/v1/auth/forgot-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    });
    const data = await response.json();
    setMessage(data.message);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
        required
      />
      <button type="submit">Send Reset Link</button>
      {message && <p>{message}</p>}
    </form>
  );
};
```

### Reset Password Page
```tsx
const ResetPassword = () => {
  const [email, setEmail] = useState("");
  const [token, setToken] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await fetch("/api/v1/auth/reset-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, token, new_password: password })
    });
    const data = await response.json();
    setMessage(data.message);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="text"
        value={token}
        onChange={(e) => setToken(e.target.value)}
        placeholder="Reset Token"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="New Password"
        required
      />
      <button type="submit">Reset Password</button>
      {message && <p>{message}</p>}
    </form>
  );
};
```

## Current Database Users

To view registered users (email only, no passwords):

```python
# Run in backend directory
python -c "
from app.db.session import SessionLocal
from app.models.user import User

db = SessionLocal()
users = db.query(User).all()
print('Registered Users:')
for user in users:
    print(f'  Email: {user.email}')
    print(f'  Name: {user.name}')
    print(f'  Role: {user.role}')
    print(f'  Phone: {user.phone}')
    print('---')
db.close()
"
```