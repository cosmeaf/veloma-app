# Security Model
Veloma App Authentication

---

# Overview

The authentication system uses a **layered security model** to detect and mitigate security threats.

The system protects against:

• brute-force attacks  
• credential stuffing  
• suspicious login behavior  
• session abuse  
• unauthorized device access  

---

# Security Components

The authentication module contains several security mechanisms.

---

# 1 — Brute Force Protection

Service:

```
LoginAttemptService
```

Tracks login attempts by:

- email
- IP address

If the number of attempts exceeds a threshold:

The account or IP is temporarily blocked.

---

# 2 — IP Intelligence

Service:

```
IPIntelligenceService
```

Analyzes:

- country
- ASN
- datacenter hosting
- proxy usage
- TOR usage
- VPN usage
- risk score

Example output:

```
{
  "country": "PT",
  "vpn": false,
  "proxy": false,
  "risk_score": 10
}
```

---

# 3 — Session Security

Sessions are stored in:

```
UserSession
```

Each session contains:

- user
- device_hash
- IP
- browser
- device
- risk_score
- timestamps

Session states:

Active

Revoked

Expired

---

# 4 — Session Expiration

Two expiration mechanisms exist:

Idle Timeout

Session expires if inactive.

Absolute Timeout

Session expires after maximum lifetime.

Configured in:

```
SecuritySettings
```

---

# 5 — Device Tracking

Each login generates a:

```
device_hash
```

Used to detect:

- new devices
- device changes
- unusual login patterns

---

# 6 — Suspicious Login Detection

Implemented by:

```
LoginSecurityService
```

Compares current login with previous login.

Analyzed parameters:

- IP
- country
- browser
- operating system
- device

If a change occurs:

Login is marked suspicious.

---

# 7 — Risk Score Detection

If:

```
risk_score ≥ 70
```

Login is considered high risk.

---

# 8 — VPN / TOR / Proxy Detection

If detected:

Login is classified as suspicious.

---

# 9 — Login Alerts

When suspicious login is detected:

An email alert is sent to the user.

Alert includes:

- IP
- country
- device
- browser

---

# 10 — Login Event History

All login attempts are stored.

Model:

```
LoginEvent
```

This enables:

- security auditing
- forensic analysis
- anomaly detection

---

# Security Philosophy

The authentication system follows these principles:

Defense in depth

Behavior-based detection

Full auditability

Device awareness

User notification

---

# Future Security Enhancements

The system can be extended with:

Impossible travel detection

Example:

Login from Portugal → login from Japan in 5 minutes.

Session hijacking detection

Detects IP changes during active sessions.

Advanced device fingerprinting

Using hardware characteristics.

Behavioral analysis

Learning typical user patterns.

---

# Summary

The authentication module implements a **multi-layer security model** designed to detect suspicious activity and protect user accounts.

Key features include:

• brute-force protection  
• IP intelligence  
• session tracking  
• device detection  
• suspicious login alerts  
• security auditing  

---