Create a new secret with the following command:
openssl rand -base64 32 | head -c 32 | base64

kubeseal <oauth2-proxy-helm-values-org.yaml >oauth2-proxy-helm-values.yaml --format yaml