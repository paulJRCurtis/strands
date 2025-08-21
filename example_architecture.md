# Example Architecture

## Services

| Name | Public | Authentication | Port |
|------|--------|----------------|------|
| web-server | ✅ | ❌ | 80 |
| api-server | ✅ | ✅ | 443 |

## Firewall Rules

| Source | Port | Protocol |
|--------|------|----------|
| 0.0.0.0/0 | 80 | HTTP |
| 0.0.0.0/0 | 22 | SSH |

## Data Flows

| Source | Destination | Encrypted |
|--------|-------------|-----------|
| web-server | database | ❌ |

## Databases

| Name | Data Types | Encrypted at Rest |
|------|------------|-------------------|
| user-db | pii, credentials | ❌ |

## IAM Policies

| Name | Actions | Resources |
|------|---------|-----------|
| admin-policy | * | * |

## Storage

| Name | Public Read | Encryption |
|------|-------------|------------|
| public-bucket | ✅ | ❌ |