# Authentication Data Model
Veloma App

---

# Overview

The authentication module relies on several database models to track user activity, security events and authentication state.

---

# UserSession

Represents an active login session.

Fields

| Field | Description |
|------|-------------|
id | Session UUID |
user | Related user |
token_jti | JWT identifier |
device_hash | Device fingerprint |
ip_address | Login IP |
country | Login country |
browser | Browser |
os | Operating system |
device | Device type |
risk_score | Risk score |
created_at | Session creation time |
last_seen | Last activity |
revoked_at | Revocation timestamp |
is_active | Session state |

Purpose

• track active sessions  
• enforce session limits  
• detect suspicious logins  

---

# LoginEvent

Tracks login history.

Fields

| Field | Description |
|------|-------------|
user | User |
ip | Login IP |
country | Country |
browser | Browser |
os | Operating system |
device | Device type |
success | Login success |
created_at | Timestamp |

Purpose

• auditing  
• suspicious login detection  

---

# LoginAttempt

Tracks failed login attempts.

Fields

| Field | Description |
|------|-------------|
email | Login email |
ip_address | IP |
attempts | Attempt count |
blocked_until | Block expiration |
last_attempt_at | Last attempt |

Purpose

• brute force protection  

---

# SecuritySettings

Stores security configuration per user.

Fields

| Field | Description |
|------|-------------|
max_devices | Maximum devices |
idle_session_timeout_minutes | Idle timeout |
absolute_session_timeout_minutes | Max session lifetime |
otp_enabled | OTP enabled |
require_otp_for_new_device | OTP for new device |
block_high_risk_login | Block high risk |
max_risk_score | Risk threshold |

---

# OTPCode

Stores OTP codes.

Purpose

• MFA verification

---

# ResetPasswordToken

Stores password reset tokens.

Purpose

• secure password recovery

---