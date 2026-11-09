# LiteLLM gateway on Railway

A self-hosted LiteLLM proxy with PostgreSQL and Redis. Railway hosts the services; LiteLLM handles the model API, virtual keys, and configured routing.

## Configuration

The Dockerfile pins LiteLLM v1.108.3-stable. `config.yaml` exposes `chat` (OpenAI gpt-4o-mini) and `backup` (OpenAI gpt-4.1-mini), with a configured model fallback. This example changes models on fallback; test both against your application requirements. It is not independent-provider redundancy.

Supply `OPENAI_API_KEY`, a strong `LITELLM_MASTER_KEY` beginning with `sk-`, and a permanent random `LITELLM_SALT_KEY`. Never commit these values. Do not rotate the salt casually: it protects stored credentials. The IaC definition references PostgreSQL and Redis variables rather than copying their credentials.

## Infrastructure as code

Install the Railway CLI, authenticate, create a dedicated project, then run `npm ci` and `npm run check`. Preview the infrastructure with `railway config plan` and apply it with `railway config apply`. Supply secrets using Railway variables before expecting the proxy to start. Generate a public domain targeting port 4000. The readiness path is `/health/readiness`.

Use the master key only for administration. Create an application virtual key restricted to the required model aliases. Send application requests to `/v1/chat/completions` with that virtual key, using the `chat` model alias.

## Production scope

This is a starting stack, not a highly available database architecture. Configure backups and restoration, continuous monitoring, resource capacity, log retention, and access policies before serving production traffic. Redis shares routing state; response caching is not enabled by this example. Adding proxy replicas does not make PostgreSQL highly available.

Deployment test observations and template URL will be recorded after verification.
