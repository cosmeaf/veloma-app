# Enterprise Architecture

## Deployment Model

Client
 ↓
Load Balancer
 ↓
Django API
 ↓
Authentication Services
 ↓
Database + Cache

The authentication service is designed to be stateless and horizontally scalable.