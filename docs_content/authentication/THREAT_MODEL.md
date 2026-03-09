# Threat Model
Veloma App Authentication

---

# Overview

This document describes the **security threat model** for the authentication system.

A threat model identifies:

• possible attacks  
• attack vectors  
• system vulnerabilities  
• mitigation strategies  

The goal is to ensure the authentication system is resilient against common security threats.

---

# Assets Protected

The authentication system protects the following assets:

User accounts

Authentication tokens

Active sessions

Password credentials

User identity

Account recovery mechanisms

---

# Attack Surface

The authentication module exposes the following entry points:

API endpoints

POST /api/v1/auth/login

POST /api/v1/auth/logout

POST /api/v1/auth/register

POST /api/v1/auth/recovery

POST /api/v1/auth/reset-password

POST /api/v1/auth/otp-verify

Session validation middleware

JWT token validation

Database access through ORM

---

# Threat Categories

The system considers several classes of attacks.

---

# Brute Force Attack

Description:

An attacker repeatedly tries different passwords to gain access.

Attack vector:

Repeated login attempts.

Example:

```
email: victim@example.com
password: 123456
password: password
password: qwerty
```

Mitigation:

LoginAttemptService

Tracks attempts per:

• email  
• IP address  

After threshold exceeded:

Login is temporarily blocked.

---

# Credential Stuffing

Description:

Attackers use leaked credentials from other breaches.

Example:

```
email: victim@example.com
password: password123
```

Mitigation:

Brute-force protection

Suspicious login detection

Email alerts for unusual logins

---

# Session Hijacking

Description:

An attacker steals a user's session token.

Attack vector:

- token leakage
- XSS attacks
- network interception

Mitigation:

Session tracking using:

UserSession model

Each session is associated with:

• device  
• IP  
• browser  

Sessions can be revoked.

Session expiration rules are enforced.

---

# Suspicious Login

Description:

An attacker logs in from a different location or device.

Example:

```
Login 1:
Portugal
Chrome
Windows

Login 2:
Russia
Firefox
Linux
```

Mitigation:

LoginSecurityService compares:

• IP
• country
• browser
• OS
• device

If changes are detected:

User receives a security alert.

---

# VPN / Proxy Abuse

Description:

Attackers hide their identity using VPN or proxy networks.

Mitigation:

IPIntelligenceService detects:

• VPN usage  
• proxy usage  
• TOR nodes  

High risk scores trigger suspicious login alerts.

---

# Token Abuse

Description:

An attacker tries to reuse stolen JWT tokens.

Mitigation:

TokenService generates tokens with unique:

token_jti

Sessions are stored in:

UserSession

If session is revoked:

Token becomes invalid.

---

# Session Abuse

Description:

A user shares account access across many devices.

Mitigation:

SessionService enforces limits using:

SecuritySettings

Example:

```
max_devices = 3
```

Old sessions are revoked automatically.

---

# Account Enumeration

Description:

An attacker tries to discover valid accounts.

Example:

```
Login failed: user does not exist
Login failed: wrong password
```

Mitigation:

Generic error messages.

Example:

```
"Invalid credentials"
```

The system does not reveal if the email exists.

---

# Email Abuse

Description:

Attackers trigger excessive alert emails.

Mitigation:

Alerts only triggered on suspicious behavior.

Future improvements may include:

Alert cooldown.

---

# Password Reset Abuse

Description:

An attacker repeatedly triggers password reset emails.

Mitigation:

Reset tokens are:

• time-limited  
• single-use  

Stored in:

ResetPasswordToken model.

---

# Logging and Monitoring

Security events are logged using the logging system.

Logged events include:

• login success  
• login failure  
• suspicious login detection  
• session revocation  
• security alerts  

These logs support:

Security monitoring

Incident investigation

Forensic analysis

---

# Security Principles

The authentication module follows these principles.

Defense in Depth

Multiple layers of security protect user accounts.

Least Privilege

Sessions grant only necessary access.

Auditability

Security events are recorded.

User Awareness

Users are notified about suspicious logins.

---

# Future Threat Mitigations

The system may be extended with:

Impossible travel detection

Example:

Login in Portugal followed by login in Japan within minutes.

Session hijacking detection

Detect IP changes during active sessions.

Device fingerprinting improvements

Using hardware and browser signals.

Behavioral authentication

Detect anomalies in user behavior.

Rate limiting at API gateway level.

---

# Conclusion

The authentication module incorporates multiple defensive layers to mitigate modern authentication threats.

Security controls include:

• brute force protection  
• suspicious login detection  
• session control  
• IP intelligence  
• audit logging  

These mechanisms significantly reduce the risk of unauthorized access.

---