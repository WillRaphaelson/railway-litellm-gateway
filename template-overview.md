# Deploy and Host LiteLLM Gateway on Railway

Deploy LiteLLM with PostgreSQL and Redis, a pinned container image, a model alias, and a configured model fallback.

## About Hosting LiteLLM Gateway

Railway runs the gateway and its supporting database and Redis. Supply your own OpenAI API key. The template generates separate gateway master and salt secrets. Inference is billed by OpenAI, and infrastructure is billed by Railway.

## Why Deploy LiteLLM Gateway on Railway

Keep your gateway configuration and persistent records in your own Railway project. Use private service references for database and Redis access.

## Common Use Cases

- Centralize model access for an application.
- Issue application virtual keys instead of distributing provider credentials.
- Configure and test model fallbacks.

## Dependencies for LiteLLM Gateway

### Deployment Dependencies

- An OpenAI API key with access to gpt-4o-mini and gpt-4.1-mini.
- Railway capacity for LiteLLM, PostgreSQL, and Redis.
- Backups, monitoring, and recovery configuration appropriate to your production requirements.
