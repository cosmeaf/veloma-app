# Authentication Flow
Veloma App

---

# Overview

This document describes the **complete authentication flow** of the system.

The authentication architecture follows a **service-based design**, where each component has a specific responsibility.

The flow ensures:

• secure authentication  
• session tracking  
• suspicious login detection  
• audit logging  

---

# High-Level Login Flow

User Login Request

↓

AuthService.login()

↓

LoginAttemptService.guard()

↓

IPIntelligenceService.investigate()

↓

Django authenticate()

↓

TokenService.create()

↓

SessionService.create()

↓

LoginAuditService.register()

↓

LoginSecurityService.check()

↓

Return JWT tokens

---

# Step-by-Step Flow

## Step 1 — Login Request

User sends credentials to:

```
POST /api/v1/auth/login
```

Payload example:

```
{
  "email": "user@example.com",
  "password": "********"
}
```

---

## Step 2 — Request Context Extraction

Context is extracted using:

```
get_login_context(request)
```

Context fields include:

- IP address
- country
- browser
- OS
- device
- user_agent

---

## Step 3 — Brute Force Protection

Service:

```
LoginAttemptService
```

Checks:

- number of attempts
- blocked IPs
- blocked accounts

If attempts exceed threshold:

Login is blocked.

---

## Step 4 — IP Intelligence Analysis

Service:

```
IPIntelligenceService
```

Analyzes:

- country
- ASN
- datacenter usage
- proxy/VPN detection
- risk_score

These values are added to login context.

---

## Step 5 — User Authentication

Using Django authentication:

```
authenticate(request, username=email, password=password)
```

If authentication fails:

- login attempt recorded
- audit event created

---

## Step 6 — Token Generation

Service:

```
TokenService
```

Creates:

- access token
- refresh token
- token_jti

These tokens are JWT-based.

---

## Step 7 — Session Creation

Service:

```
SessionService.create()
```

Creates a record in:

```
UserSession
```

Stored data:

- user
- device_hash
- ip
- browser
- device
- risk_score

Session limits are enforced here.

---

## Step 8 — Login Event Audit

Service:

```
LoginAuditService
```

Stores a login record in:

```
LoginEvent
```

Fields recorded:

- user
- ip
- country
- browser
- device
- success
- timestamp

---

## Step 9 — Suspicious Login Detection

Service:

```
LoginSecurityService
```

Analyzes:

- IP changes
- country changes
- browser changes
- device changes
- VPN usage
- TOR usage
- proxy usage
- risk score

If suspicious:

Email alert is sent.

---

# Final Response

If login succeeds:

```
{
  "access": "...jwt...",
  "refresh": "...jwt...",
  "user": {...}
}
```

---

# Security Layers

The authentication system includes multiple security layers:

Layer 1  
Brute force protection

Layer 2  
IP reputation analysis

Layer 3  
Session management

Layer 4  
Suspicious login detection

Layer 5  
Email alerts

---

# Diagram Summary

```
Login Request
     │
     ▼
AuthService
     │
     ▼
LoginAttemptService
     │
     ▼
IPIntelligenceService
     │
     ▼
Django Authentication
     │
     ▼
TokenService
     │
     ▼
SessionService
     │
     ▼
LoginAuditService
     │
     ▼
LoginSecurityService
     │
     ▼
Response
```

---