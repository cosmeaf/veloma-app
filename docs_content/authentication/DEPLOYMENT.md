# Authentication Deployment Guide
Veloma App

---

# Overview

This document describes how to deploy the authentication module in production.

---

# Required Environment Variables

```
SECRET_KEY
JWT_SECRET
EMAIL_HOST
EMAIL_USER
EMAIL_PASSWORD
```

---

# JWT Configuration

Example

```
JWT_ACCESS_TOKEN_LIFETIME=15m
JWT_REFRESH_TOKEN_LIFETIME=7d
```

---

# Email Configuration

Required for:

• password recovery  
• suspicious login alerts  

Example

```
EMAIL_HOST=smtp.mailserver.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

---

# Database Requirements

Authentication tables must exist.

Required tables

```
UserSession
LoginEvent
LoginAttempt
SecuritySettings
OTPCode
ResetPasswordToken
```

---

# Security Configuration

Ensure:

• HTTPS enabled  
• secure cookies enabled  
• CSRF protection enabled  

---

# Monitoring

Monitor authentication logs.

Example

```
/var/log/veloma/django.log
```

---

# Deployment Checklist

[ ] Database migrations applied

[ ] Environment variables configured

[ ] Email service configured

[ ] JWT secret configured

[ ] Logs enabled

---