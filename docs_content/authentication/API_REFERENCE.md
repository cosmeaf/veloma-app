# Authentication API Reference
Veloma App

---

# Overview

This document describes the **Authentication API endpoints**.

All endpoints are prefixed with:

```
/api/v1/auth/
```

Authentication is based on **JWT tokens**.

---

# Authentication Endpoints

| Endpoint | Method | Description |
|--------|--------|-------------|
/auth/login | POST | Authenticate user |
/auth/logout | POST | Logout current session |
/auth/register | POST | Register new user |
/auth/otp-verify | POST | Verify OTP code |
/auth/recovery | POST | Request password recovery |
/auth/reset-password | POST | Reset password |
/auth/me | GET | Retrieve authenticated user |

---

# Login

Endpoint

```
POST /api/v1/auth/login
```

Payload

```
{
  "email": "user@example.com",
  "password": "secret"
}
```

Success Response

```
{
  "access": "jwt_token",
  "refresh": "jwt_refresh",
  "user": {
      "id": 1,
      "email": "user@example.com"
  }
}
```

Possible Errors

```
Invalid credentials
Account disabled
Too many attempts
```

---

# Logout

Endpoint

```
POST /api/v1/auth/logout
```

Headers

```
Authorization: Bearer <access_token>
```

Result

```
Session revoked
```

---

# Register

Endpoint

```
POST /api/v1/auth/register
```

Payload

```
{
  "email": "user@example.com",
  "password": "secret"
}
```

Result

```
User created
```

---

# OTP Verification

Endpoint

```
POST /api/v1/auth/otp-verify
```

Payload

```
{
  "code": "123456"
}
```

---

# Password Recovery

Endpoint

```
POST /api/v1/auth/recovery
```

Payload

```
{
  "email": "user@example.com"
}
```

---

# Reset Password

Endpoint

```
POST /api/v1/auth/reset-password
```

Payload

```
{
  "token": "...",
  "password": "new_password"
}
```

---

# Authenticated User

Endpoint

```
GET /api/v1/auth/me
```

Headers

```
Authorization: Bearer <access_token>
```

Response

```
{
  "id": 1,
  "email": "user@example.com"
}
```

---