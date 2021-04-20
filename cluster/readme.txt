Steps to spin up cluster:
- run Ansible role
- download config
- create namespace:
kubectl create namespace flux-system --dry-run=client -o yaml | kubectl apply -f -
- create key:
gpg --export-secret-keys --armor "${FLUX_KEY_FP}" |
kubectl create secret generic sops-gpg \
    --namespace=flux-system \
    --from-file=sops.asc=/dev/stdin
- do exports
- do envsubst
- do sops
- install Flux:
kubectl apply --kustomize=./cluster/base/flux-system