FROM ghcr.io/berriai/litellm:v1.108.3-stable
WORKDIR /app
COPY config.yaml /app/config.yaml
EXPOSE 4000
CMD ["--config", "/app/config.yaml", "--port", "4000", "--num_workers", "1"]
