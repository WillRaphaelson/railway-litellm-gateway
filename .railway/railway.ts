import { defineRailway, github, postgres, preserve, project, redis, service } from "railway/iac";

export default defineRailway(() => {
  const db = postgres("postgres");
  const cache = redis("redis");
  const gateway = service("litellm", {
    source: github("WillRaphaelson/railway-litellm-gateway"),
    healthcheck: "/health/readiness",
    healthcheckTimeout: 300,
    env: {
      PORT: "4000",
      PRIMARY_API_BASE: "https://api.openai.com/v1",
      DATABASE_URL: db.env.DATABASE_URL,
      REDIS_HOST: cache.env.REDISHOST,
      REDIS_PORT: cache.env.REDISPORT,
      REDIS_PASSWORD: cache.env.REDISPASSWORD,
      STORE_MODEL_IN_DB: "True",
      OPENAI_API_KEY: preserve(),
      LITELLM_MASTER_KEY: preserve(),
      LITELLM_SALT_KEY: preserve(),
    },
  });
  return project("railway-litellm-gateway", { resources: [db, cache, gateway] });
});
