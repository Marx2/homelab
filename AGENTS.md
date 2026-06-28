# Agent Configuration

This file contains configuration and instructions for AI agents working in this project.

## Project Context

It's a directory containing kubernetes configuration managed with gitops approach using FluxCD,
updated with Renovate bot.

## Documentation (context7 MCP)

Use the context7 MCP server to fetch up-to-date documentation for the following libraries used in this project:

- **FluxCD**: `/websites/fluxcd_io_flux` (3233 snippets) — GitOps, HelmRelease, Kustomization, reconciliation
- **bjw-s App Template helm chart**: `/websites/bjw-s-labs_github_io_helm-charts` (110 snippets) — universal Helm chart used by most deployments
- **Renovate**: `/websites/renovatebot` (3308 snippets) — automated dependency update configuration

Always prefer context7 docs over web search or training data for these libraries.

## Agent Behaviors

Do not make any changes until you have 95% confidence in what you need to build. Ask me
follow-up questions until you reach that confidence.

### Code Style

- subfolders contains namespaces configurations
- subfolders in namespace contains definition of deployment of specific service
- most deployments uses universal App Template helm chart, which documentation is available
  at: https://bjw-s-labs.github.io/helm-charts/docs/app-template/

## Deployment Standards (default namespace)

Every service follows this structure:

```
cluster/apps/default/
├── kustomization.yaml          ← add {app}/ks.yaml here
└── {app}/
    ├── ks.yaml
    └── app/
        ├── kustomization.yaml
        ├── helmrelease.yaml
        ├── interceptor-service.yaml
        └── httpscaledobject.yaml
```

### ks.yaml

- `dependsOn: [{name: keda-http}]` — always
- `interval: 30m`, `retryInterval: 1m`, `timeout: 15m`
- `prune: true`, `wait: true`
- `postBuild.substitute.APP: *app`
- YAML anchor `&app` on metadata.name, reused as label value

### helmrelease.yaml

- Chart: `app-template` v5.0.1 from `bjw-s` HelmRepository
- `interval: 15m`
- `install.remediation.retries: 3`
- `upgrade.cleanupOnFail: true`, strategy `rollback`, retries 3
- `driftDetection.mode: enabled` — always ignore `/spec/replicas` on Deployment and `/spec/containers/resources/limits` on Pod
- `replicas: 0` — KEDA manages scaling, Flux must not fight it
- Ingress: `className: nginx`, auth annotations pointing to `auth.${SECRET_DOMAIN}`, hajimari annotations
- Ingress service: always `keda-http-interceptor-proxy:8080`, NOT the app's own service
- Hostname pattern: `{{ .Release.Name }}.${SECRET_DOMAIN}`

### interceptor-service.yaml

Identical for every app in default namespace — copy verbatim:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: keda-http-interceptor-proxy
  namespace: default
spec:
  type: ExternalName
  externalName: keda-add-ons-http-interceptor-proxy.networking.svc.cluster.local
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
```

### httpscaledobject.yaml

- `replicas.min: 0`, `replicas.max: 1`
- `scaledownPeriod: 300`
- `scaleTargetRef.service` must match the app's Service name

### Variable substitution

Available cluster-wide vars: `${SECRET_DOMAIN}`, `${TZ}`. Secrets go in `cluster-secrets.sops.yaml`.

## Applied Learning

When something fails repeatedly, when I has to re-explain, or when a workaround is found for a
platform/tool limitation, add a one-line bullet here. Keep each bullet under 15 words. No
explanations. Only add things that will save time in future.

- KEDA scale-to-zero: set `replicas: 0` + driftDetection ignore `/spec/replicas` to avoid Flux fight.
- `readOnlyRootFilesystem: true`: mount ConfigMap to separate path (e.g. `/config/`), emptyDir for writable dirs.
- interceptor-service.yaml (ExternalName for KEDA HTTP proxy) is identical across all default-namespace apps — copy verbatim.
- HTTPScaledObject ingress path routes to `keda-http-interceptor-proxy` service, not the app service directly.
- Frigate 0.17: `/api/faces/{name}/register` saves new file each call — avoid on live-detection crops (duplicates).
- Frigate 0.17: UI upload auto-detects + crops face; use UI, not manual `/register` calls on raw crops.