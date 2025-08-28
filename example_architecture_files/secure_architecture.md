# Secure Architecture Example

## Services

| Name | Public | Authentication | Port |
|------|--------|----------------|------|
| web-server | Yes | Yes | 443 |
| api-server | Yes | Yes | 443 |
| internal-service | No | Yes | 8443 |

## Firewall Rules

| Source | Port | Protocol |
|--------|------|----------|
| 10.0.0.0/8 | 443 | HTTPS |
| 192.168.1.0/24 | 22 | SSH |

## Data Flows

| Source | Destination | Encrypted |
|--------|-------------|-----------|
| web-server | database | Yes |
| api-server | database | Yes |
| internal-service | cache | Yes |

## Databases

| Name | Data Types | Encrypted at Rest |
|------|------------|-------------------|
| user-db | user-data, logs | Yes |
| analytics-db | metrics, reports | Yes |

## IAM Policies

| Name | Actions | Resources |
|------|---------|-----------|
| web-policy | s3:GetObject | arn:aws:s3:::web-assets/* |
| api-policy | dynamodb:Query, dynamodb:GetItem | arn:aws:dynamodb:*:table/users |

## Storage

| Name | Public Read | Encryption |
|------|-------------|------------|
| private-bucket | No | Yes |
| backup-bucket | No | Yes |