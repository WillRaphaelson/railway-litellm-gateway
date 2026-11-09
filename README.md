# LiteLLM gateway on Railway

A self-hosted LiteLLM proxy with PostgreSQL and Redis. Railway hosts the services; LiteLLM handles the model API, virtual keys, and configured routing.

## Configuration

The Dockerfile pins LiteLLM v1.108.3. `config.yaml` exposes `chat` (OpenAI gpt-4o-mini) and `backup` (OpenAI gpt-4.1-mini), with a configured model fallback. This example changes models on fallback; test both against your application requirements. It is not independent-provider redundancy.

Supply `OPENAI_API_KEY`, a strong `LITELLM_MASTER_KEY` beginning with `sk-`, and a permanent random `LITELLM_SALT_KEY`. Never commit these values. Do not rotate the salt casually: it protects stored credentials. The IaC definition references PostgreSQL and Redis variables rather than copying their credentials.

## Infrastructure as code

Install the Railway CLI, authenticate, create a dedicated project, then run `npm ci` and `npm run check`. Preview the infrastructure with `railway config plan` and apply it with `railway config apply`. Supply secrets using Railway variables before expecting the proxy to start. Generate a public domain targeting port 4000. The readiness path is `/health/readiness`.

Use the master key only for administration. Create an application virtual key restricted to the required model aliases. Send application requests to `/v1/chat/completions` with that virtual key, using the `chat` model alias.

## Production scope

This is a starting stack, not a highly available database architecture. Configure backups and restoration, continuous monitoring, resource capacity, log retention, and access policies before serving production traffic. Redis shares routing state; response caching is not enabled by this example. Adding proxy replicas does not make PostgreSQL highly available.

[Deploy the LiteLLM gateway stack on Railway](https://railway.com/deploy/railway-litellm-gateway-guide). The template creates the three services, generates gateway/database secrets, and requires your OpenAI API key. `PRIMARY_API_BASE` defaults to `https://api.openai.com/v1`.

Verified November 9, 2026 on the dedicated project and a fresh published-template deployment: database-aware readiness, unauthenticated model access rejection, restricted virtual-key creation, real inference, and temporary-key revocation. A controlled invalid primary API path on the dedicated project returned a real completion from the configured backup model, verified by its model ID in response headers. Both models use OpenAI; this is not a cross-provider outage test. No load or cost benchmark was performed.

Run `smoke.py` with `GATEWAY_URL` and `LITELLM_MASTER_KEY` set in your environment. It makes one small billable inference request. `EXPECT_FALLBACK=1` additionally asserts the backup model ID; use that only after deliberately breaking the primary route in a non-production project. Restore the primary endpoint afterward. Never print or commit the master key.
