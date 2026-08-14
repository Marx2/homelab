# PocketID OIDC Setup

PocketID is an OIDC provider with passkey login, managed by pocket-id-operator.
UI: `https://pocket-id.${SECRET_DOMAIN}`

## First Boot

1. Open the UI — set up admin account on first visit
2. The operator API key is needed for the operator to manage OIDC clients as CRDs.
   Create it: UI → Settings → API Keys → New key → copy value
3. Store it in a secret:
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

## LDAP

Users are sourced from lldap (`ldap://lldap.networking.svc.cluster.local:3890`).
Manage users at `https://lldap.${SECRET_DOMAIN}` (admin / `${LLDAP_LDAP_USER_PASS}`).
