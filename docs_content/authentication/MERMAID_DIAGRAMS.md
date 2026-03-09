# Mermaid Diagrams

```mermaid
flowchart TD

Client --> API
API --> LoginView
LoginView --> AuthService

AuthService --> SessionService
AuthService --> TokenService
AuthService --> LoginSecurityService
AuthService --> LoginAuditService
```