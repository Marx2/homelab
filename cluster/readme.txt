Steps to spin up cluster:
- run Ansible role
- download config
- create namespace:
kubectl create namespace flux-system --dry-run=client -o yaml | kubectl apply -f -
gpg --export-secret-keys --armor "${FLUX_KEY_FP}" |
- do exports
- do envsubst
- do sops
- create key:
kubectl create secret generic sops-gpg \
    --namespace=flux-system \
    --from-file=sops.asc=/dev/stdin
- add labels for Longhorn:
kubectl label nodes wuwek wezyr silver node.longhorn.io/create-default-disk=true
- install Flux:
kubectl apply --kustomize=./cluster/base/flux-system