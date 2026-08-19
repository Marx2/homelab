# User Management

User lifecycle is managed through LLDAP (users/groups) + PocketID (OIDC access control).

## Protecting an App with PocketID

### Ingress Annotations

Add these annotations to the app's Ingress:

```yaml
nginx.ingress.kubernetes.io/auth-url: "https://pocket-id.${SECRET_DOMAIN}/oauth2/auth"
nginx.ingress.kubernetes.io/auth-signin: "https://pocket-id.${SECRET_DOMAIN}/oauth2/start?rd=$escaped_request_uri"
```

### Register an OIDC Client

Every app needs a `PocketIDOIDCClient` CR in the `networking` namespace:

```yaml
apiVersion: pocketid.internal/v1alpha1
kind: PocketIDOIDCClient
metadata:
  name: cyberchef
  namespace: networking
spec:
  pocketIDInstanceRef:
    name: pocket-id
  name: CyberChef
  callbackURLs:
    - https://cyberchef.${SECRET_DOMAIN}/callback
  logoutURLs:
    - https://cyberchef.${SECRET_DOMAIN}/logout
```

Without this CRD, the initial login flow fails — PocketID cannot generate the authorization redirect URL (no `client_id`, `redirect_uri`, etc.). The auth subrequest (`/oauth2/auth`) only checks session validity, so users with an active PocketID session from another app would pass, but unauthenticated users would get stuck.

### Unrestricted vs Restricted Access

- **Unrestricted** (no `allowedUserGroups`): any authenticated PocketID user can access the app — same behavior as oauth2-proxy + Dex.
- **Restricted** (`allowedUserGroups` set): only users in the listed LLDAP groups can complete the OIDC flow.

### Adding a New App to the Cluster

| Step | Description |
|------|-------------|
| 1 | Add PocketID ingress annotations (replace old auth annotations) |
| 2 | Create `PocketIDOIDCClient` CRD (always required) |
| 3 | Create LLDAP group (only if access needs restriction) |
| 4 | Add app to `admin-all` group's `allowedOIDCClients` (only if restricted) |

Steps 3-4 are skipped for apps accessible to all authenticated users.

## User Source of Truth

LLDAP is the single source of truth. The LDAP sync is one-way: **LLDAP → PocketID**. PocketID never writes users back to LLDAP.

Users created directly in PocketID (via `PocketIDUser` CRD or UI) exist only in PocketID's own database and won't appear in LLDAP. Since this cluster has `LDAP_ENABLED=true`, always create users in LLDAP to maintain a consistent user directory.

## Creating a User

1. Go to `https://lldap.${SECRET_DOMAIN}` (admin / `${LLDAP_LDAP_USER_PASS}`)
2. Users → Create User
3. User sets their display name, email, and initial password
4. User logs in to PocketID (`https://pocket-id.${SECRET_DOMAIN}`) and registers a passkey

## Invitation Link

PocketID can generate a one-time login URL that bypasses passkey requirement — useful for first-time setup or new users without a passkey yet.

```bash
kubectl -n networking exec deploy/pocket-id -- \
  /app/pocket-id one-time-access-token <username>
```

The URL is valid for 1 hour. Send it to the user so they can log in and register their passkey.

## Access Rights

Access is controlled via **LLDAP groups** and **PocketID's `allowedUserGroups`** on each OIDC client.

### Group Strategy (Option B — group-centric)

Each app defines its own group (e.g., `cyberchef-users`, `grafana-users`). A special `admin-all` group grants access to every app by listing all OIDC clients.

**Per-app groups** are set on the `PocketIDOIDCClient` CRD:

```yaml
apiVersion: pocketid.internal/v1alpha1
kind: PocketIDOIDCClient
metadata:
  name: cyberchef
  namespace: networking
spec:
  pocketIDInstanceRef:
    name: pocket-id
  name: CyberChef
  callbackURLs:
    - https://cyberchef.${SECRET_DOMAIN}/callback
  logoutURLs:
    - https://cyberchef.${SECRET_DOMAIN}/logout
  allowedUserGroups:
    - name: cyberchef-users
    - name: admin-all    # admin access
```

**Admin group** is defined as a `PocketIDUserGroup` CRD:

```yaml
apiVersion: pocketid.internal/v1alpha1
kind: PocketIDUserGroup
metadata:
  name: admin-all
  namespace: networking
spec:
  friendlyName: "Full Access"
  allowedOIDCClients:
    - name: cyberchef
    - name: grafana
    - name: nextcloud
    # ... list every OIDC client here
```

### Adding a New User to an App

1. Create the user in LLDAP (or they self-register if enabled)
2. Add them to the appropriate LLDAP group (e.g., `cyberchef-users`)
3. They can now access the app — no other configuration needed

### Granting Admin Access

Add the user to the `admin-all` group in LLDAP. They now have access to every OIDC client listed in `PocketIDUserGroup.admin-all.spec.allowedOIDCClients`.

## Blocking a User

### Block at LLDAP level (suspends all access)

1. Go to `https://lldap.${SECRET_DOMAIN}`
2. Users → select user → disable or delete

The user loses access after the next LDAP sync (up to 5 minutes via CronJob). PocketID session becomes invalid on the following auth check after sync completes.

### Block from a specific app only

Remove the user from that app's LLDAP group (e.g., remove from `cyberchef-users`). Their access to other apps remains unaffected.
