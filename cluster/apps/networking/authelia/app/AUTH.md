# Authelia Auth Guide

## 1. Forward-auth (protect apps without native auth)

Add to app's Ingress annotations:
```yaml
nginx.ingress.kubernetes.io/auth-url: "https://authelia.${SECRET_DOMAIN}/api/authz/forward-auth"
nginx.ingress.kubernetes.io/auth-signin: "https://authelia.${SECRET_DOMAIN}?rd=$scheme://$host$request_uri"
nginx.ingress.kubernetes.io/auth-response-headers: "Remote-User,Remote-Groups,Remote-Name,Remote-Email"
```

## 2. OIDC clients (apps with native OIDC support)

Add to `configmap.yaml` under `identity_providers.oidc.clients`:
```yaml
- client_id: myapp
  client_name: My App
  client_secret: '$pbkdf2-sha512$...'  # docker run --rm authelia/authelia:latest authelia crypto hash generate pbkdf2 --password secret
  redirect_uris:
    - https://myapp.${SECRET_DOMAIN}/oauth2/callback
  scopes: [openid, profile, email, groups]
  grant_types: [authorization_code, refresh_token]
  response_types: [code]
  authorization_policy: one_factor
```

Discovery: `https://authelia.${SECRET_DOMAIN}/.well-known/openid-configuration`

## 3. Operator CRDs (declarative OIDC clients)

```yaml
apiVersion: authelia.milas.dev/v1alpha1
kind: OIDCClient
metadata:
  name: myapp
  namespace: networking
spec:
  client_id: myapp
  client_name: My App
  redirect_uris:
    - https://myapp.${SECRET_DOMAIN}/callback
  scopes: [openid, profile, email]
```

List: `kubectl get oidcclient,oidcprovider -n networking`

## 4. /userinfo endpoint

- URL: `https://authelia.${SECRET_DOMAIN}/api/oidc/userinfo`
- Requires Bearer token: `curl -H "Authorization: Bearer <token>" <url>`
- Returns: `sub`, `name`, `email`, `groups`, `preferred_username`

## 5. JWT access tokens

Enable in `configmap.yaml`:
```yaml
identity_providers:
  oidc:
    enable_jwt_access_token_stateless_introspection: true
    clients:
      - client_id: myapp
        access_token_signed_response_alg: RS256
```

JWKS: `https://authelia.${SECRET_DOMAIN}/jwks.json`

## Verification

```bash
kubectl get pods -n networking
curl https://authelia.${SECRET_DOMAIN}/api/health
curl https://authelia.${SECRET_DOMAIN}/.well-known/openid-configuration
kubectl get oidcclient,oidcprovider -n networking
```

## Secrets setup

Add to KeePass + run `python3 encode.py`:

| KeePass entry | How to generate | Notes |
|---|---|---|
| `AUTHELIA_ADMIN_USER` | e.g. `admin` | plaintext |
| `AUTHELIA_ADMIN_PASSWORD_HASH` | `docker run --rm authelia/authelia:latest authelia crypto hash generate argon2 --password 'yourpassword'` | plaintext, starts with `$argon2id$` |
| `AUTHELIA_ADMIN_EMAIL` | your email | plaintext |
| `AUTHELIA_OIDC_PRIVATE_KEY` | `openssl genrsa 4096 \| base64 -w0` | **must be base64-encoded single line** — stored in `data:` field |

**Not needed** (chart auto-generates via its own secret):
- ~~`AUTHELIA_SESSION_SECRET`~~ — chart injects via `AUTHELIA_SESSION_SECRET_FILE`
- ~~`AUTHELIA_STORAGE_ENCRYPTION_KEY`~~ — chart injects via `AUTHELIA_STORAGE_ENCRYPTION_KEY_FILE`
- ~~`AUTHELIA_OIDC_HMAC_SECRET`~~ — OIDC not configured in configmap (operator manages it)

Add to `tmpl/cluster-secrets.yaml`:
```yaml
AUTHELIA_ADMIN_USER: ${AUTHELIA_ADMIN_USER}
AUTHELIA_ADMIN_PASSWORD_HASH: ${AUTHELIA_ADMIN_PASSWORD_HASH}
AUTHELIA_ADMIN_EMAIL: ${AUTHELIA_ADMIN_EMAIL}
AUTHELIA_OIDC_PRIVATE_KEY: ${AUTHELIA_OIDC_PRIVATE_KEY}
```

## Re-installing from scratch

If the storage encryption key changes (e.g. after helm uninstall), the SQLite DB must be wiped:

```bash
kubectl run -n networking tmp-cleanup --rm -i --restart=Never \
  --image=busybox \
  --overrides='{"spec":{"volumes":[{"name":"pvc","persistentVolumeClaim":{"claimName":"config-authelia-pvc"}}],"containers":[{"name":"tmp-cleanup","image":"busybox","command":["sh","-c","rm -f /config/db.sqlite3 /config/notification.txt && echo done"],"volumeMounts":[{"name":"pvc","mountPath":"/config"}]}]}}'
```
