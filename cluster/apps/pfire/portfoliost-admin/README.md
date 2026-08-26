# portfoliost-admin

## PocketID Admin API Key

The admin service uses the PocketID Admin API to fetch user identities (email, groups, etc.). This requires a static API key that is automatically mirrored from the `networking` namespace via Kubernetes Reflector.

### How it works

1. The PocketID operator creates `pocket-id-static-api-key` in the `networking` namespace
2. Reflector mirrors this secret to `pfire` using auto-mirror annotations
3. The admin HelmRelease references the mirrored secret

### Initial setup (one-time)

Annotate the source secret in `networking` to enable auto-mirroring to `pfire`:

```bash
kubectl annotate secret pocket-id-static-api-key -n networking \
  reflector.v1.k8s.emberstack.com/reflection-allowed="true" \
  reflector.v1.k8s.emberstack.com/reflection-auto-enabled="true" \
  reflector.v1.k8s.emberstack.com/reflection-auto-namespaces="pfire" \
  --overwrite
```

### Verify mirroring

```bash
# Check secret exists in pfire
kubectl get secret pocket-id-static-api-key -n pfire

# Verify the token matches
kubectl -n networking get secret pocket-id-static-api-key -o jsonpath='{.data.token}' | base64 -d
kubectl -n pfire get secret pocket-id-static-api-key -o jsonpath='{.data.token}' | base64 -d
```

### Troubleshooting

If the secret is not mirrored:

1. Check reflector logs: `kubectl logs -n system -l app.kubernetes.io/name=reflector --tail=20`
2. Verify annotations on source: `kubectl get secret pocket-id-static-api-key -n networking -o jsonpath='{.metadata.annotations}'`
3. Ensure reflector is running: `kubectl get pods -n system | grep reflector`
