# Docker Deployment Guide

## Quick Start with Docker

### Using Docker Compose (Recommended)

1. **Build the image:**
   ```bash
   docker-compose build
   ```

2. **Create `.env` file:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Run the agent:**
   ```bash
   docker-compose up -d
   ```

4. **View logs:**
   ```bash
   docker-compose logs -f
   ```

5. **Stop the agent:**
   ```bash
   docker-compose down
   ```

### Run Single Analysis

```bash
docker-compose --profile single run --rm portfolio-agent-single
```

### Using Docker Directly

1. **Build:**
   ```bash
   docker build -t ai-portfolio-manager .
   ```

2. **Run:**
   ```bash
   docker run -d \
     --name portfolio-agent \
     --env-file .env \
     -v $(pwd)/portfolio.json:/app/portfolio.json:ro \
     -v $(pwd)/output:/app/output \
     -v $(pwd)/logs:/app/logs \
     ai-portfolio-manager
   ```

3. **View logs:**
   ```bash
   docker logs -f portfolio-agent
   ```

4. **Stop:**
   ```bash
   docker stop portfolio-agent
   docker rm portfolio-agent
   ```

## Environment Variables

Pass via `.env` file or `-e` flag:

```bash
docker run -d \
  -e GEMINI_API_KEY=your_key \
  -e UPDATE_INTERVAL_SECONDS=60 \
  -e CONFIDENCE_THRESHOLD=70 \
  ...
```

## Volumes

### Recommended Mounts

- `./portfolio.json:/app/portfolio.json:ro` - Portfolio config (read-only)
- `./output:/app/output` - Recommendations output
- `./logs:/app/logs` - Application logs

### Example with Custom Portfolio

```bash
docker run -d \
  --env-file .env \
  -v /path/to/custom_portfolio.json:/app/portfolio.json:ro \
  -v /path/to/output:/app/output \
  ai-portfolio-manager
```

## Production Deployment

### Docker Swarm

```bash
docker stack deploy -c docker-compose.yml portfolio-stack
```

### Kubernetes

Create a deployment (example):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portfolio-agent
spec:
  replicas: 1
  selector:
    matchLabels:
      app: portfolio-agent
  template:
    metadata:
      labels:
        app: portfolio-agent
    spec:
      containers:
      - name: agent
        image: ai-portfolio-manager:latest
        envFrom:
        - secretRef:
            name: portfolio-secrets
        volumeMounts:
        - name: portfolio-config
          mountPath: /app/portfolio.json
          subPath: portfolio.json
        - name: output
          mountPath: /app/output
      volumes:
      - name: portfolio-config
        configMap:
          name: portfolio-config
      - name: output
        persistentVolumeClaim:
          claimName: portfolio-output
```

## Troubleshooting

### Container exits immediately
Check logs:
```bash
docker logs portfolio-agent
```

Common issues:
- Missing GEMINI_API_KEY
- Invalid portfolio.json
- Network connectivity

### Can't access output files
Ensure volume mounts have correct permissions:
```bash
chmod -R 755 output logs
```

### High memory usage
Reduce number of tickers in portfolio or increase container memory limit:
```bash
docker run -m 512m ...
```

## Best Practices

1. **Use docker-compose** for easier management
2. **Mount volumes** to persist data
3. **Use .env file** for configuration
4. **Enable restart policy** for production
5. **Monitor logs** regularly
6. **Update images** periodically

## Security

1. **Never commit .env** to version control
2. **Use secrets management** in production
3. **Run as non-root** user (add to Dockerfile):
   ```dockerfile
   USER 1000:1000
   ```
4. **Scan images** for vulnerabilities
5. **Use specific tags** instead of `latest`
