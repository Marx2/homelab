https://dev.to/asizikov/using-github-container-registry-with-kubernetes-38fb
https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/

## GITHUB_API_TOKEN_IMAGE_REGISTRY_READ_ENCODED

This is the base64-encoded dockerconfigjson for pulling private images from ghcr.io.

Generate value (replace TOKEN with your GitHub PAT with read:packages scope):

    kubectl create secret docker-registry regcred \
      --docker-server=ghcr.io \
      --docker-username=Marx2 \
      --docker-password=TOKEN \
      --docker-email=no@spam.xx \
      --dry-run=client \
      -o yaml \
      | grep '\.dockerconfigjson:' \
      | awk '{print $2}'

Store the printed value in KeePass as: GITHUB_API_TOKEN_IMAGE_REGISTRY_READ_ENCODED
Then run: ./encode.py

