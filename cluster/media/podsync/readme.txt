Basic auth
https://kubernetes.github.io/ingress-nginx/examples/auth/basic/

htpasswd -c auth marx
kubectl create secret generic podsync-basic-auth --from-file=auth -n media
kubectl get secret podsync-basic-auth -o yaml -n media > secret.yaml

kubeseal <secret.yaml >podsync-basic-auth.yaml --format yaml