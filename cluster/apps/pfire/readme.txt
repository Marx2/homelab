https://dev.to/asizikov/using-github-container-registry-with-kubernetes-38fb
https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/

private image registry support:

1. Generate secret text
kubectl create secret docker-registry regcred \
  --docker-server=ghcr.io \
  --docker-username=Marx2 \
  --docker-password=xxxx \
  --docker-email=no@spam.xx \
  --dry-run=client \
  -o yaml | base64

2. Replace .dockerconfigjson value with variable


to test decode like this:
echo "xxxx==" | base64 --decode
