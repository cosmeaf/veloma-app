# Authentication Architecture
Veloma App

---

# Overview

This document describes the internal architecture of the **authentication module**.

The module follows a **service-oriented architecture**, separating responsibilities into dedicated components.

Goals of this design:

• modularity  
• maintainability  
• security  
• auditability  
• scalability  

The module handles:

- authentication
- session control
- device identification
- suspicious login detection
- security auditing
- brute-force protection
- OTP verification
- password recovery

---

# High-Level Architecture

```
Client
   │
   ▼
Authentication API
   │
   ▼
Views
   │
   ▼
AuthService
   │
   ├── LoginAttemptService
   ├── IPIntelligenceService
   ├── TokenService
   ├── SessionService
   ├── LoginAuditService
   └── LoginSecurityService
   │
   ▼
Database
```

---

# Module Components

authentication/

```
models/
services/
middleware/
views/
serializers/
dto/
admin.py
signals.py
urls.py
```

---

# Models Layer

The **models layer** stores all authentication-related data.

Key models:

### UserSession

Represents a user login session.

Fields:

- user
- token_jti
- device_hash
- ip_address
- country
- browser
- os
- device
- risk_score
- created_at
- last_seen
- revoked_at
- is_active

Purpose:

- track active sessions
- enforce session limits
- support logout from devices
- detect session abuse

---

### LoginEvent

Stores login history.

Fields:

- user
- ip
- country
- browser
- os
- device
- success
- created_at

Purpose:

- security auditing
- suspicious login detection
- behavioral analysis

---

### LoginAttempt

Stores failed login attempts.

Purpose:

- brute-force protection

Tracks:

- email
- ip_address
- attempt_count
- blocked_until

---

### SecuritySettings

Per-user security configuration.

Fields:

- max_devices
- idle_session_timeout_minutes
- absolute_session_timeout_minutes
- otp_enabled
- require_otp_for_new_device
- block_high_risk_login
- max_risk_score
- allowed_countries

Purpose:

- enforce customizable security policies

---

### OTPCode

Stores One-Time Password codes.

Used for:

- multi-factor authentication
- account recovery

---

### ResetPasswordToken

Stores password recovery tokens.

Used for:

- secure password reset flow

---

# Services Layer

Services contain **business logic**.

Each service has a focused responsibility.

---

## AuthService

Central authentication orchestrator.

Responsibilities:

- authenticate credentials
- coordinate login flow
- generate tokens
- create sessions
- trigger security checks

---

## SessionService

Manages user sessions.

Responsibilities:

- create session
- enforce session limits
- revoke sessions
- validate session
- update activity timestamp

---

## TokenService

Handles JWT token operations.

Responsibilities:

- create access tokens
- create refresh tokens
- validate tokens
- manage token identifiers (JTI)

---

## LoginAttemptService

Protects against brute-force attacks.

Responsibilities:

- track failed attempts
- block suspicious login activity

---

## LoginAuditService

Stores login events.

Responsibilities:

- record login success
- record login failure

---

## LoginSecurityService

Detects suspicious logins.

Checks for:

- IP changes
- country changes
- browser changes
- device changes
- VPN / proxy detection
- high risk score

If suspicious:

Alert email is sent.

---

## IPIntelligenceService

Analyzes IP reputation.

Extracts:

- country
- ASN
- datacenter usage
- VPN detection
- risk_score

---

## OTPService

Handles OTP verification.

Used for:

- MFA login
- account recovery

---

## PasswordService

Handles password management.

Responsibilities:

- password validation
- password change logic

---

## RecoveryService

Handles password recovery flow.

Responsibilities:

- generate reset tokens
- validate reset requests

---

## RegisterService

Handles new user registration.

Responsibilities:

- create user
- initialize security settings

---

## SecuritySettingsService

Manages security policies.

Responsibilities:

- retrieve user security settings
- enforce policy rules

---

# Middleware Layer

Session validation is enforced by middleware.

File:

```
middleware/session_validation.py
```

Responsibilities:

- validate active session
- detect revoked sessions
- enforce idle timeout
- enforce absolute timeout

This ensures that expired or revoked sessions cannot access protected endpoints.

---

# Device Identification

Devices are identified using a fingerprint:

```
device_hash = SHA256(ip + browser + os + device)
```

Purpose:

- detect new devices
- identify unusual login patterns
- enforce device limits

---

# Security Layers

The authentication module implements **multiple security layers**.

Layer 1  
Brute-force protection

Layer 2  
IP reputation analysis

Layer 3  
Session management

Layer 4  
Suspicious login detection

Layer 5  
Security alerts

This layered approach improves resilience against attacks.

---

# Security Logging

Security events are logged using:

```
logging
```

Events logged:

- login success
- login failure
- suspicious login
- alert email sent
- security anomalies

These logs support:

- monitoring
- investigation
- incident response

---

# Database Interaction

Services interact with the database via Django ORM.

Typical flow:

```
AuthService
   │
   ▼
SessionService
   │
   ▼
UserSession.objects.create()
```

ORM ensures:

- data consistency
- transactional safety
- easy migrations

---

# Extensibility

The architecture allows easy integration of additional security features.

Possible extensions:

• impossible travel detection  
• session hijacking detection  
• behavioral login analysis  
• adaptive risk scoring  
• WebAuthn / passkeys  

---

# Summary

The authentication module provides a **robust, modular and secure architecture**.

Key characteristics:

• service-oriented design  
• session-based security  
• behavioral login detection  
• audit-ready logging  
• extensible security model  

This architecture ensures the authentication system remains scalable and secure as the application evolves.

---