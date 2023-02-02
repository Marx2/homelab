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



Longhorn correct backup path:
nfs://192.168.1.49/volume1/backup/longhorn


Error:
"orphaned pod found, but volume paths are still present on disk
but error not a directory occurred when trying to remove the volumes dir"

k3s kubectl get pods --all-namespaces # lists all namespaces in use
cd /var/lib/kubelet/pods
cat <pod UUID logs say is orphaned>/etc-hosts
# note the last line, the app name is in the entry after the IP address
k3s kubectl get pod -n <appname>
# if nothing comes back, it is orphaned
rm -rf <pod UUID logs say is orphaned>
systemctl restart k3s
