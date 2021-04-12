FLUX 2
https://toolkit.fluxcd.io/guides/installation/

- install flux command on local Mac
brew install fluxcd/tap/flux

- Verify prerequisites, and that current cluster is correctly set:
flux check --pre


- UNINSTALL
flux uninstall --crds

- INSTALL
export GITHUB_TOKEN=<github token>
export GITHUB_REPO=homelab
export GITHUB_USER=Marx2


flux bootstrap github \
  --owner=${GITHUB_USER} \
  --repository=${GITHUB_REPO} \
  --branch=master \
  --path=/cluster \
  --personal

Flux ressurection (install Flux on new cluster, when repo already contains Flux):
kubectl create namespace flux-system
kubectl create secret generic flux-system --from-literal=username=Marx2 --from-literal=password=<GITHUB_TOKEN> -n flux-system



useful commands:
helm get values -n kube-system sealed-secrets-controller -a
flux reconcile source helm prometheus-community-charts -n flux-system
flux reconcile hr prometheus -n monitoring


Toolbox image:
https://github.com/nicolaka/netshoot