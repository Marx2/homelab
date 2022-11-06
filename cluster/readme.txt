Steps to spin up cluster:
- run Ansible role
- download config
- create namespace:
kubectl create namespace flux-system --dry-run=client -o yaml | kubectl apply -f -

export FLUX_KEY_FP=...
export PERSONAL_KEY_FP=...
gpg --export-secret-keys --armor "${FLUX_KEY_FP}" |
kubectl create secret generic sops-gpg \
    --namespace=flux-system \
    --from-file=sops.asc=/dev/stdin

- do exports
- do envsubst
- do sops
- add labels for Longhorn:
kubectl label nodes wuwek wezyr silver node.longhorn.io/create-default-disk=true
- install Flux:
kubectl apply --kustomize=./cluster/base/flux-system



new steps:
brew install go-task/tap/go-task
task init
task precommit:init
task precommit:update
