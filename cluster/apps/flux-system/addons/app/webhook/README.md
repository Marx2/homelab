# Flux GitHub Webhook Receiver

Triggers instant Flux reconciliation on `git push` instead of waiting for the polling interval.

## How it works

GitHub sends a push event → `flux-webhook.${SECRET_DOMAIN}` → `webhook-receiver` service (port 80) → notification-controller verifies HMAC signature → reconciles `flux-system` GitRepository immediately.

## Secret setup

Add entry to KeePass:

| Field    | Value                          |
|----------|--------------------------------|
| Title    | `BOOTSTRAP_WEBHOOK_TOKEN`      |
| Password | output of `openssl rand -hex 20` |

Then regenerate SOPS.

## GitHub webhook configuration

After deploying, get the receiver path:
```bash
kubectl get receiver github-receiver -n flux-system \
  -o jsonpath='{.status.webhookPath}'
```

In GitHub repo → Settings → Webhooks → Add webhook:
- **Payload URL**: `https://flux-webhook.<your-domain>/hook/<hash>`
- **Content type**: `application/json`
- **Secret**: value of `BOOTSTRAP_WEBHOOK_TOKEN` from KeePass
- **Events**: `Just the push event`
