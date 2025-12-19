# Диаграммы (Mermaid)

## Общая схема (упрощённо)

```mermaid
flowchart LR
  U[Пользователь] -->|HTTP| API[FastAPI + RateLimit]
  API -->|Cache| R[(Redis)]
  API -->|DB ops| P[(PostgreSQL)]
  API -->|External fetch| EXT[External APIs]
  LEG[Legacy утилита (CSV/XLSX)] --> P
  LEG -->|CSV/XLSX| FS[(Файлы)]
```

## Слои приложения

```mermaid
flowchart TB
  routes --> handlers --> services --> clients
  services --> repo
  repo --> config
  handlers --> domain
  services --> domain
```

## Rate-Limit (Token Bucket)

```mermaid
sequenceDiagram
  participant C as Client
  participant A as API
  participant R as Redis
  C->>A: Request
  A->>R: EVAL (token bucket)
  alt token available
    R-->>A: allowed=1
    A-->>C: 200 OK
  else no tokens
    R-->>A: allowed=0
    A-->>C: 429 Too Many Requests
  end
```
