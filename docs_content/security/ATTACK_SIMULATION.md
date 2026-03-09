# Authentication Attack Simulation
Veloma App

---

# Overview

This document describes simulated attacks used to test the authentication system.

Purpose:

• validate security controls  
• test detection mechanisms  
• improve incident response  

---

# Attack Scenario 1

Brute Force Attack

Simulation

Send repeated login attempts.

Example:

```
POST /auth/login
email: victim@example.com
password: wrongpassword
```

Expected Result

```
LoginAttemptService blocks further attempts
```

---

# Attack Scenario 2

Credential Stuffing

Simulation

Use leaked credentials.

Expected Result

Suspicious login detection triggered.

User receives alert.

---

# Attack Scenario 3

Suspicious Location Login

Simulation

Login from different country.

Example:

```
Previous login: Portugal
New login: Russia
```

Expected Result

```
LoginSecurityService detects anomaly
```

Email alert sent.

---

# Attack Scenario 4

Session Abuse

Simulation

Login from multiple devices.

Expected Result

Session limit enforced.

Old sessions revoked.

---

# Attack Scenario 5

Token Replay

Simulation

Reuse old JWT token.

Expected Result

Session validation rejects token.

---

# Attack Scenario 6

VPN Login

Simulation

Login using VPN IP.

Expected Result

Risk score increases.

Suspicious login detection triggered.

---

# Monitoring Attack Tests

During simulations monitor:

• authentication logs  
• suspicious login alerts  
• session creation events  

---

# Safety Rules

Run simulations only in:

• staging environment  
• isolated testing environments  

Never run attack simulations in production.

---

# Conclusion

Regular attack simulations ensure the authentication system remains resilient against real-world threats.