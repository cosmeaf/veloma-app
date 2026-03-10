# CONSENTS MODULE SPEC

## Objective

Provide a system to manage client consent for accounting services,
including authorization for data processing and credential usage.

## Entities

### Consent

- id
- token
- owner
- created_by
- client_name
- client_email
- client_nif
- service_reference
- consent_text
- status
- accepted
- accepted_at
- revoked_at
- ip_address
- user_agent
- ipintel_data
- created_at

### ConsentCredential

- consent
- organ
- login_identifier
- secret_encrypted
- created_at

## States

PENDING → SIGNED → REVOKED

## API Endpoints

POST /api/consents  
GET /api/consents  
GET /api/consents/{id}  
PUT /api/consents/{id}  
PATCH /api/consents/{id}  
DELETE /api/consents/{id}

POST /api/consents/public/{token}

POST /api/consents/revoke/{token}

## Security

- unique tokens
- encrypted credentials
- IP logging
- user-agent logging
- ipintel integration

## Audit

Every consent must record:

- creation
- acceptance
- revocation
- technical metadata

## Architecture

Django  
DRF  
Celery  
Redis  
IPIntel  
Email Service