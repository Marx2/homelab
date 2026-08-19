---
name: homelab-deploy
description: Use when deploying or modifying any app in the homelab k8s cluster — new service, HelmRelease, secrets, postgres user, ingress, KEDA scaling, or FluxCD Kustomization.
---

# Homelab Deployment Pattern

## Namespaces

| Namespace | KEDA | Postgres |
|-----------|------|----------|
| `default` | yes (scale-to-zero) | per-app |
| `home` | no (`replicas: 1`) | namespace-level (`postgres-home`) |
| `media` | no | namespace-level (`postgres-media`) |

## `default` namespace (KEDA scale-to-zero)

Every app needs 4 files in `app/`:

- `helmrelease.yaml` — `replicas: 0`, driftDetection ignores `/spec/replicas` on Deployment and `/spec/containers/resources/limits` on Pod
- `interceptor-service.yaml` — ExternalName pointing to `keda-add-ons-http-interceptor-proxy.networking.svc.cluster.local:8080` (copy verbatim)
- `httpscaledobject.yaml` — `min: 0`, `max: 1`, `scaledownPeriod: 300`
- Ingress service: `keda-http-interceptor-proxy:8080`, NOT the app's own service

## `home` / `media` namespace (no KEDA)

- `replicas: 1` in HelmRelease
- Ingress service: app's own service identifier
- driftDetection ignores only `/spec/containers/resources/limits` on Pod (no `/spec/replicas`)

## Standard ks.yaml

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: &app <appname>
  namespace: flux-system
spec:
  targetNamespace: <namespace>
  commonMetadata:
    labels:
      app.kubernetes.io/name: *app
  path: ./cluster/apps/<namespace>/<appname>/app
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
  wait: true
  interval: 30m
  retryInterval: 1m
  timeout: 15m
  postBuild:
    substitute:
      APP: *app
```

## CrunchyData PostgreSQL (namespace-level)

One `PostgresCluster` per namespace (e.g. `postgres-home`, `postgres-media`).
Add new apps as extra users/databases in the same cluster.

Files at namespace level (NOT inside app subdir):
- `postgrescluster-<ns>.yaml` — the PostgresCluster CR
- `crunchy-postgres-secret.yaml` — pgBackRest S3/Minio creds (uses `${MINIO_S3_ACCESS_KEY}` / `${MINIO_S3_SECRET_KEY}` already in cluster-secrets)

Both files go in `cluster/apps/<namespace>/kustomization.yaml` resources.

Operator-generated secret name: `<cluster-name>-pguser-<username>`
Keys: `host`, `port`, `dbname`, `user`, `password`, `uri`

Primary service DNS: `<cluster-name>-primary.<namespace>.svc.cluster.local`

Postgres 18 image: `registry.developers.crunchydata.com/crunchydata/crunchy-postgres:ubi9-18.4-2621`

## Secrets workflow (SOPS)

Two-layer substitution:
1. `tmpl/cluster-secrets.yaml` maps `VAR: ${BOOTSTRAP_VAR}` → generates `cluster/config/cluster-secrets.sops.yaml`
2. Flux postBuild substitutes `${VAR}` in manifests from that secret

New app secrets:
1. Add to `tmpl/cluster-secrets.yaml`: `MY_VAR: ${MY_KEEPASS_TITLE}`
2. Add entry to `~/marx.kdbx` with **Title = `MY_KEEPASS_TITLE`** (exact match — encode.py does `kp.find_entries(title=g)`)
3. Run `python3 encode.py` — regenerates and re-encrypts `cluster-secrets.sops.yaml`
4. **Do not git push until encode.py has been run.**

**Crunchy postgres passwords: never put in KeePass.** The operator generates `<cluster>-pguser-<user>` automatically. Use `valueFrom.secretKeyRef` with key `uri` (full connection string) or `password` directly in the HelmRelease. No encode.py step needed.

For app-specific secrets (not in cluster-secrets), use Flux postBuild substitution:
```yaml
# endurain-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: endurain-secrets
  namespace: home
stringData:
  SECRET_KEY: ${ENDURAIN_SECRET_KEY}
  FERNET_KEY: ${ENDURAIN_FERNET_KEY}
```
This gets substituted at reconcile time — no plaintext in git, no per-file SOPS.

## Standard HelmRelease scaffold (no KEDA)

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/bjw-s/helm-charts/main/charts/other/app-template/schemas/helmrelease-helm-v2.schema.json
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: &app <appname>
spec:
  interval: 15m
  chart:
    spec:
      chart: app-template
      version: 5.0.1
      interval: 15m
      sourceRef:
        kind: HelmRepository
        name: bjw-s
        namespace: flux-system
  install:
    remediation:
      retries: 3
  upgrade:
    cleanupOnFail: true
    remediation:
      strategy: rollback
      retries: 3
  driftDetection:
    mode: enabled
    ignore:
      - paths: [/spec/containers/resources/limits]
        target:
          kind: Pod
  values:
    ...
```

## Ingress auth annotations (nginx oauth2-proxy)

```yaml
nginx.ingress.kubernetes.io/auth-url: "https://auth.${SECRET_DOMAIN}/oauth2/auth"
nginx.ingress.kubernetes.io/auth-signin: https://auth.${SECRET_DOMAIN}/oauth2/start
```
