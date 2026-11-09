import { defineRailway, github, postgres, project, redis, service } from "railway/iac";

export default defineRailway(() => {
  const db = postgres("postgres");
  const cache = redis("redis");
  const gateway = service("litellm", {
    source: github("WillRaphaelson/railway-litellm-gateway"),
    healthcheck: "/health/readiness",
    healthcheckTimeout: 300,
    env: {
      PORT: "4000",
      DATABASE_URL: db.env.DATABASE_URL,
      REDIS_HOST: cache.env.REDISHOST,
      REDIS_PORT: cache.env.REDISPORT,
      REDIS_PASSWORD: cache.env.REDISPASSWORD,
      STORE_MODEL_IN_DB: "True",
    },
  });
  return project("railway-litellm-gateway", { resources: [db, cache, gateway] });
});
