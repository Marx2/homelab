https://dev.to/asizikov/using-github-container-registry-with-kubernetes-38fb
https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/

private image registry support:

1. Generate secret text (replace xxx with token)
kubectl create secret docker-registry regcred \
  --docker-server=ghcr.io \
  --docker-username=Marx2 \
  --docker-password=xxx \
  --docker-email=no@spam.xx \
  --dry-run=client \
  -o yaml

2. take .dockerconfigjson value and save in keepass
3. run ./encode.py
