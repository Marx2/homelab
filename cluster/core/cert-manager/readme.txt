How to prepare Issuer: https://cert-manager.io/docs/configuration/acme/dns01/cloudflare/


removing chart doesn't remove webhooks:
kubectl delete MutatingWebhookConfiguration cert-manager-cert-manager-webhook
kubectl delete  ValidatingWebhookConfiguration cert-manager-cert-manager-webhook