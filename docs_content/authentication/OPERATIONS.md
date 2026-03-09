# Authentication Operations Guide
Veloma App

---

# Overview

This document describes how to **operate, monitor, and troubleshoot** the authentication module in production.

It is intended for:

• DevOps engineers  
• backend developers  
• security engineers  
• incident response teams  

The goal is to ensure the authentication system can be **monitored, maintained, and investigated efficiently**.

---

# Authentication Services

Core services involved in authentication:

AuthService  
SessionService  
TokenService  
LoginAttemptService  
LoginAuditService  
LoginSecurityService  
IPIntelligenceService  

Each service produces logs that can be used for monitoring and debugging.

---

# Important Logs

Authentication logs are critical for security monitoring.

Typical log events include:

Login success  
Login failure  
Brute-force detection  
Suspicious login detection  
Session revocation  
Email alerts  

Example log entries:

```
Login successful | user_id=45 ip=185.44.x.x
```

```
Suspicious login detected | user_id=45 country=RU
```

```
Session revoked automatically | session_id=8f3c9d
```

Logs should be collected by the central logging system.

---

# Log Locations

Depending on deployment configuration, logs may be available in:

Application logs

```
/var/log/veloma/django.log
```

Container logs

```
docker logs veloma-api
```

Central logging systems

Example:

ELK stack  
Grafana Loki  
Cloud logging services  

---

# Monitoring Authentication

The following metrics should be monitored.

Login Success Rate

Number of successful logins.

Login Failure Rate

Number of failed login attempts.

Suspicious Login Alerts

Triggered by LoginSecurityService.

Session Count

Number of active sessions.

Brute-force Blocks

Triggered by LoginAttemptService.

---

# Investigating Login Issues

When users report login problems, follow these steps.

Step 1 — Check application logs.

Look for:

```
Login failed
Invalid credentials
Blocked login attempts
```

Step 2 — Check brute-force protection.

Inspect LoginAttempt table.

Possible issues:

Too many login attempts from same IP.

Step 3 — Check account status.

Verify:

```
user.is_active
```

Step 4 — Check suspicious login detection.

Look for:

```
Suspicious login detected
```

Step 5 — Verify session state.

Inspect UserSession table.

Look for:

```
is_active
revoked_at
```

---

# Revoking Sessions

Administrators may revoke sessions manually.

Using Django admin:

Authentication → User Sessions.

Actions available:

Revoke sessions  
Reactivate sessions  

Using management shell:

```
UserSession.objects.filter(user=user).update(is_active=False)
```

---

# Forcing Logout from All Devices

Use SessionService.

Example:

```
SessionService.revoke_all(user)
```

This logs the user out from every device.

---

# Investigating Suspicious Login

When suspicious login alerts occur:

Check login event history.

Table:

```
LoginEvent
```

Compare:

IP addresses

Countries

Browsers

Devices

Determine whether the login was legitimate.

---

# Security Incident Response

If an account compromise is suspected:

Step 1

Revoke all sessions.

Step 2

Force password reset.

Step 3

Check login history.

Step 4

Review suspicious IP addresses.

Step 5

Block malicious IP if necessary.

---

# Database Tables Used

Authentication module uses the following tables.

UserSession

Stores active sessions.

LoginEvent

Stores login history.

LoginAttempt

Stores brute-force tracking.

SecuritySettings

Stores security policies.

OTPCode

Stores MFA codes.

ResetPasswordToken

Stores password reset tokens.

---

# Backup and Recovery

Authentication tables must be included in regular database backups.

Critical tables:

UserSession

LoginEvent

LoginAttempt

ResetPasswordToken

Backup schedule should follow system policy.

---

# Recommended Monitoring Alerts

Recommended alerts for production monitoring.

High login failure rate.

Spike in suspicious login alerts.

Unusual session growth.

Excessive password reset requests.

These may indicate security attacks.

---

# Performance Considerations

Authentication endpoints are frequently used.

Ensure:

Database indexes are present.

Session queries are optimized.

Caching is enabled for session validation if needed.

---

# Operational Best Practices

Rotate application logs regularly.

Monitor login activity patterns.

Keep authentication dependencies updated.

Review suspicious login alerts.

Regularly audit active sessions.

---

# Conclusion

The authentication module is designed to provide strong security and operational visibility.

By monitoring logs, tracking sessions, and responding quickly to suspicious activity, administrators can maintain a secure authentication environment.

---