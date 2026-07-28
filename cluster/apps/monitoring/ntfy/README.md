# ntfy + apprise

Push notifications to Android via ntfy, routed through Apprise.

## Architecture

```
any service → POST /notify → Apprise → ntfy → Android app
```

## ntfy

**URL:** https://ntfy.k.homylab.com  
**Credentials:** see `NTFY_ADMIN_USER` / `NTFY_ADMIN_PASSWORD` in KeePass

### Android setup

1. Install [ntfy app](https://play.google.com/store/apps/details?id=io.heckel.ntfy)
2. Add server: `https://ntfy.k.homylab.com`
3. Login with KeePass credentials
4. Subscribe to topic: `alerts` (or any topic you configure in Apprise)

### Send a test notification directly

```bash
curl -u marx:PASSWORD -d "test message" https://ntfy.k.homylab.com/alerts
```

### Create additional topics/users

```bash
kubectl exec -n monitoring deploy/ntfy -- ntfy user add --role=user myuser
kubectl exec -n monitoring deploy/ntfy -- ntfy access myuser alerts rw
```

## Apprise

**URL:** https://apprise.k.homylab.com  
**Config:** `cluster/apps/monitoring/apprise/app/apprise-secret.yaml`

Pre-configured to route to ntfy topic `alerts` via in-cluster URL:
```
ntfy://ntfy.monitoring.svc.cluster.local/alerts
```

For authenticated ntfy calls update the URL to:
```
ntfy://marx:PASSWORD@ntfy.monitoring.svc.cluster.local/alerts
```

### Send notification via Apprise API

```bash
# fire-and-forget to all configured URLs
curl -X POST http://apprise.monitoring.svc.cluster.local:8000/notify \
  -H "Content-Type: application/json" \
  -d '{"title": "Alert", "body": "Something happened"}'

# target a specific config key
curl -X POST http://apprise.monitoring.svc.cluster.local:8000/notify/apprise \
  -H "Content-Type: application/json" \
  -d '{"title": "Alert", "body": "Something happened"}'
```

### Add more notification channels

Edit `apprise-secret.yaml` and add URLs under `urls:`:

```yaml
urls:
  - ntfy://marx:PASSWORD@ntfy.monitoring.svc.cluster.local/alerts
  - discord://webhook_id/webhook_token
  - tgram://bot_token/chat_id
```

Full list of supported services: https://github.com/caronc/apprise/wiki
