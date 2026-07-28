# Firecrawl — In-Cluster Integration Guide

## Service Endpoint

```
http://firecrawl-api.home.svc.cluster.local:3002
```

No authentication required (`USE_DB_AUTHENTICATION: false`).

## MCP Integration

Firecrawl exposes an MCP server. Add to your agent's MCP config:

```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_URL": "http://firecrawl-api.home.svc.cluster.local:3002",
        "FIRECRAWL_API_KEY": "any-value"
      }
    }
  }
}
```

> `FIRECRAWL_API_KEY` is required by the MCP client but not validated by this deployment.

## REST API Quick Reference

### Scrape a URL → Markdown

```bash
curl -X POST http://firecrawl-api.home.svc.cluster.local:3002/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "formats": ["markdown"]}'
```

### Crawl a site

```bash
curl -X POST http://firecrawl-api.home.svc.cluster.local:3002/v1/crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "limit": 10, "scrapeOptions": {"formats": ["markdown"]}}'
```

### Check crawl status

```bash
curl http://firecrawl-api.home.svc.cluster.local:3002/v1/crawl/<job-id>
```

### Health check

```bash
curl http://firecrawl-api.home.svc.cluster.local:3002/v0/health/liveness
# {"status":"ok"}
```

## Components

| Pod | Role |
|-----|------|
| `firecrawl-api` | HTTP API, port 3002 |
| `firecrawl-worker` | Queue worker (BullMQ) |
| `firecrawl-nuq-worker` | NUQ queue worker (postgres-backed) |
| `firecrawl-playwright-service` | Headless browser, port 3000 (internal only) |
| `firecrawl-redis` | Queue store (emptyDir — not persistent) |

## Notes

- Redis is **not persistent** — in-flight jobs are lost on redis pod restart. Acceptable for scraping workloads.
- NUQ schema lives in `postgres-home` cluster, `firecrawl` database, `nuq` schema. Re-applied automatically by `firecrawl-nuq-schema` Job on each Flux reconcile.
- `pg_cron` maintenance jobs (index reindex, queue cleanup) are **not installed** — crunchy postgres does not support `cron.database_name` config. Queues self-clean via application logic.
- Playwright runs with `readOnlyRootFilesystem: true`; node cache mounted as emptyDir at `/home/node/.cache`.
