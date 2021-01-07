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






useful commands:
helm get values -n kube-system sealed-secrets-controller -a
flux reconcile hr prometheus -n monitoring