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
  --personal \
  --private=false

backup existing Fllux secret:
kubectl  -n flux-system get secret flux-system -o yaml > flux_identity.yaml

Flux ressurection (install Flux on new cluster, when repo already contains Flux):
kubectl create namespace flux-system
kubectl apply -f flux_identity.yaml


useful commands:
helm get values -n kube-system sealed-secrets-controller -a
flux reconcile source helm prometheus-community-charts -n flux-system
flux reconcile hr prometheus -n monitoring


Toolbox image:
https://github.com/nicolaka/netshoot
example:
kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- /bin/bash

reconnect:
kubectl attach tmp-shell -c tmp-shell -i -t