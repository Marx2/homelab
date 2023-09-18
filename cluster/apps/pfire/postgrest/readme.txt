Based on: https://kubernetes.github.io/ingress-nginx/examples/auth/basic/

htpasswd -c auth postgrest

kubectl create secret generic postgrest-basic-auth --from-file=auth -o yaml -n pfire > secret.yaml