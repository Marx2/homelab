Based on: https://kubernetes.github.io/ingress-nginx/examples/auth/basic/

htpasswd -c auth postgrest

kubectl create secret generic postgrest-basic-auth --from-file=auth -o yaml -n pfire > secret.yaml


Base on: https://postgrest.org/en/stable/tutorials/tut0.html
create role web_anon nologin;

grant usage on schema attributes to web_anon;
grant select on attributes to web_anon;
grant select on latest_attributes to web_anon;
