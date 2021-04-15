How to prepare Issuer: https://cert-manager.io/docs/configuration/acme/dns01/cloudflare/
kubeseal <cloudflare-api-token-secret-org.yaml >cloudflare-api-token-secret.yaml --format yaml


removing chart doesn't remove webhooks:
kubectl delete MutatingWebhookConfiguration cert-manager-cert-manager-webhook
kubectl delete  ValidatingWebhookConfiguration cert-manager-cert-manager-webhook