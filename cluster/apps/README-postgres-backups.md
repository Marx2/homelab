# PostgreSQL Backup Configuration Notes

## Minio endpoint

pgbackrest is configured to use `minio.${SECRET_DOMAIN}` (the nginx-proxied HTTPS endpoint)
rather than the internal cluster DNS `minio.database.svc.cluster.local:9000`.

**Why:** pgbackrest has no option to use plain HTTP for S3 storage (as of v2.58). The internal
minio service on port 9000 serves plain HTTP, which causes a TLS handshake failure
("wrong version number" / "packet length too long"). The public domain endpoint goes through
nginx which handles TLS termination, so pgbackrest gets a valid HTTPS connection.

**What was tried and failed:**
- `repo1-storage-verify-tls=n` — disables cert verification only, not the TLS protocol itself
- `repo1-s3-https=n` — not a valid pgbackrest option (v2.58 warns and ignores it)
- `minio.database.svc.cluster.local:9000` — plain HTTP, breaks TLS handshake

**Affected clusters:** `home/postgres-home`, `media/postgres-media`, `pfire/postgres-pfire`
