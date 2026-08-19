# PocketID OIDC Setup

PocketID is an OIDC provider with passkey login, managed by pocket-id-operator.
UI: `https://pocket-id.${SECRET_DOMAIN}`

## First Boot

There is no setup page. PocketID uses a Static API User (created by the operator) to bootstrap.

1. Get the static API username:
   ```bash
   kubectl -n networking get secret pocket-id-static-api-key -o jsonpath='{.data.token}' | base64 -d | \
     xargs -I{} curl -s https://pocket-id.${SECRET_DOMAIN}/api/users -H "X-API-KEY: {}" | \
     python3 -m json.tool | grep username
   ```

2. Generate a one-time login URL (valid 1 hour):
   ```bash
   kubectl -n networking exec deploy/pocket-id -- /app/pocket-id one-time-access-token <username-from-above>
   ```

3. Open the URL — you're logged in as admin (Static API User).

4. Go to Users → create your personal admin account and register your passkey.

5. The operator API key is needed for the operator to manage OIDC clients as CRDs.
   Create it: UI → Settings → API Keys → New key → copy value
6. Store it in a secret:
   ```bash
   kubectl -n networking create secret generic pocket-id-operator-api-key \
     --from-literal=api-key=<paste-key>
   ```

## Protecting an App with PocketID (nginx ingress)

Add these annotations to the app's Ingress:

```yaml
nginx.ingress.kubernetes.io/auth-url: "https://pocket-id.${SECRET_DOMAIN}/oauth2/auth"
nginx.ingress.kubernetes.io/auth-signin: "https://pocket-id.${SECRET_DOMAIN}/oauth2/start?rd=$escaped_request_uri"
```

## Registering an OIDC Client (via CRD)

Create a `PocketIDOIDCClient` CR in the `networking` namespace:

```yaml
apiVersion: pocketid.internal/v1alpha1
kind: PocketIDOIDCClient
metadata:
  name: my-app
  namespace: networking
spec:
  pocketIDInstanceRef:
    name: pocket-id
  name: My App
  callbackURLs:
    - https://my-app.${SECRET_DOMAIN}/callback
  logoutURLs:
    - https://my-app.${SECRET_DOMAIN}/logout
```

The operator creates the client in PocketID and writes credentials to a secret
`<cr-name>-oidc-credentials` with keys `clientId` and `clientSecret`.

## LDAP (lldap)

Users are sourced from lldap (`ldap://lldap.networking.svc.cluster.local:3890`).
Manage users at `https://lldap.${SECRET_DOMAIN}` (admin / `${LLDAP_LDAP_USER_PASS}`).

LDAP config is stored in PocketID's DB — env vars only apply on first boot if the DB is empty.
Configure via UI: Settings → Application Configuration → LDAP section.

### Working configuration for this cluster

| Field | Value |
|---|---|
| **LDAP URL** | `ldap://lldap.networking.svc.cluster.local:3890` |
| **LDAP Bind DN** | `uid=admin,ou=people,dc=home,dc=local` |
| **LDAP Bind Password** | `${LLDAP_LDAP_USER_PASS}` |
| **LDAP Base DN** | `dc=home,dc=local` |
| **User Search Filter** | `(&(objectClass=person)(!(uid=admin)))` |
| **Groups Search Filter** | `(objectClass=groupOfUniqueNames)` |
| **Admin Group Name** | `lldap_admin` |

### Attribute mapping (leave defaults, except)

| Field | Value |
|---|---|
| **Group Members Attribute** | `uniqueMember` |
| **Group Unique Identifier Attribute** | `cn` |
| **Group RDN Attribute (in DN)** | `cn` |

### Sync

LDAP syncs automatically every hour. A CronJob (`pocket-id-ldap-sync`) also triggers sync every 5 minutes via the API.

Manual sync:
```bash
kubectl -n networking get secret pocket-id-static-api-key -o jsonpath='{.data.token}' | base64 -d | \
  xargs -I{} curl -sf -X POST https://pocket-id.${SECRET_DOMAIN}/api/application-configuration/sync-ldap \
  -H "X-API-KEY: {}"
```

## Potential Integrations

Apps that support deeper OIDC integration (user identity, groups, roles passed to the app).

### Native OIDC

| App | Namespace | Config |
|-----|-----------|--------|
| **Immich** | media | Env vars: `OAUTH_ENABLED=true`, `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, `OAUTH_ISSUER_URL`. Secret already has `OAUTH_CLIENT_SECRET`. |
| **Grafana** | monitoring | `grafana.ini` → `[auth.generic_oauth]`. Supports `groups_attribute_path` and `role_attribute_path` for group/role mapping. |
| **Weave GitOps** | flux-system | `oidc-auth` secret with `issuerURL`, `clientID`, `clientSecret`, `redirectURL`. Uses Kubernetes RBAC impersonation — OIDC groups map to cluster roles. |
| **Endurain** | home | Settings → Identity Providers → add provider. Supports OIDC with PKCE. |

### Proxy Headers (no native OIDC)

| App | Namespace | Headers |
|-----|-----------|---------|
| **Frigate** | home | `x-forwarded-user` (username), `x-forwarded-groups` (roles). Role mapping via `proxy.header_map.role_map` in Frigate config. |
| **Calibre-Web** | media | `Remote-User`, `Remote-Groups`, `Remote-Name`, `Remote-Email`. Requires `Reverse Proxy Authentication` enabled in Calibre-Web config. |
