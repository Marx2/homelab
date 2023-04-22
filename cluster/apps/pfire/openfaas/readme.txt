create secret:

kubectl create secret generic basic-auth \
  -n pfire \
  --output=yaml \
  --dry-run=client \
  --from-literal basic-auth-user=admin \
  --from-literal basic-auth-password=$(openssl rand -base64 32) > basic_auth.yaml
