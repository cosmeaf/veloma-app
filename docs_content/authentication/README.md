# Authentication Module Documentation
Project: Veloma App
Module: authentication

------------------------------------------------------------
OVERVIEW
------------------------------------------------------------

The authentication module is responsible for handling:

- User login
- Session management
- Device identification
- Security verification
- Brute force protection
- Login auditing
- Token generation
- OTP verification
- Password recovery

The system was designed with a modular architecture to allow
high security, auditability, and scalability.

------------------------------------------------------------
MAIN LOGIN FLOW
------------------------------------------------------------

User Login Request
        │
        ▼
AuthService.login()
        │
        ▼
LoginAttemptService.guard()
(brute force protection)
        │
        ▼
IPIntelligenceService.investigate()
(IP risk analysis)
        │
        ▼
authenticate()
(Django authentication)
        │
        ▼
SessionService.create()
(session creation + session limit policy)
        │
        ▼
TokenService.create()
(JWT token generation)
        │
        ▼
LoginAuditService.register()
(login history record)
        │
        ▼
LoginSecurityService.check()
(suspicious login detection)
        │
        ▼
Return Access + Refresh Token


------------------------------------------------------------
SERVICES ARCHITECTURE
------------------------------------------------------------

authentication/services/

auth_service.py
    Main login orchestrator.

session_service.py
    Responsible for:
    - session creation
    - session validation
    - session expiration
    - session revocation
    - session activity updates

device_service.py
    Responsible for device fingerprinting and device detection.

token_service.py
    Responsible for generating and validating JWT tokens.

login_attempt_service.py
    Protects against brute force attacks.

login_audit_service.py
    Stores login history for auditing.

login_security_service.py
    Detects suspicious login behavior and triggers alerts.

ip_intelligence_service.py
    Analyzes IP reputation and geolocation.

otp_service.py
    Handles One-Time Password verification.

password_service.py
    Handles password changes and validation.

recovery_service.py
    Handles password recovery workflows.

register_service.py
    Handles new user registration.

security_settings_service.py
    Provides security configuration per user.


------------------------------------------------------------
SESSION MANAGEMENT
------------------------------------------------------------

Sessions are stored in the model:

authentication.models.UserSession

Each session stores:

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


SessionService responsibilities:

• enforce session limits
• revoke old sessions automatically
• update last_seen activity
• validate expiration rules
• support logout and logout-all


------------------------------------------------------------
SESSION EXPIRATION RULES
------------------------------------------------------------

Configured in:

SecuritySettings

Fields:

max_devices
    Maximum active devices allowed.

idle_session_timeout_minutes
    Session expires after inactivity.

absolute_session_timeout_minutes
    Maximum lifetime of a session.


Example:

idle timeout: 1440 minutes
absolute timeout: 10080 minutes


------------------------------------------------------------
DEVICE IDENTIFICATION
------------------------------------------------------------

Each device generates a fingerprint:

device_hash = SHA256(
    ip + browser + os + device
)

This allows the system to:

- identify device changes
- detect unusual logins
- enforce device limits


------------------------------------------------------------
SUSPICIOUS LOGIN DETECTION
------------------------------------------------------------

Implemented in:

LoginSecurityService

The system analyzes login context and compares it with
previous login events.

Factors analyzed:

• IP address change
• country change
• browser change
• operating system change
• device change
• VPN / TOR / Proxy detection
• risk_score from IP intelligence


A login is classified as suspicious if:

- behavioral changes are detected
OR
- risk_score >= 70
OR
- VPN/TOR/Proxy is detected


------------------------------------------------------------
LOGIN ALERT SYSTEM
------------------------------------------------------------

If a suspicious login is detected:

LoginSecurityService.send_alert()

An email alert is sent using:

EmailService

Template used:

login_alert


Alert email contains:

- IP address
- country
- browser
- device
- risk score


------------------------------------------------------------
LOGIN EVENT HISTORY
------------------------------------------------------------

Stored in:

LoginEvent model

Information stored:

- user
- ip
- country
- browser
- os
- device
- success
- created_at

This history is used for:

• suspicious login detection
• security auditing
• behavioral analysis


------------------------------------------------------------
BRUTE FORCE PROTECTION
------------------------------------------------------------

Implemented in:

LoginAttemptService

Tracks login attempts by:

- email
- IP address

If threshold exceeded:

Account temporarily blocked.


------------------------------------------------------------
SECURITY DESIGN GOALS
------------------------------------------------------------

The authentication module was designed to provide:

• auditability
• attack detection
• brute force protection
• session control
• device tracking
• suspicious login alerts


------------------------------------------------------------
FUTURE SECURITY IMPROVEMENTS
------------------------------------------------------------

Possible future improvements:

• Impossible travel detection
• Advanced device fingerprinting
• Session hijacking detection
• Risk scoring engine
• Alert cooldown mechanism
• Behavioral baseline detection


------------------------------------------------------------
END OF DOCUMENT
------------------------------------------------------------