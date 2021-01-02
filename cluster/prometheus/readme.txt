Helm Chart from https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack#kube-prometheus-stack

helm install prometheus prometheus-community/kube-prometheus-stack -n prometheus
helm uninstall prometheus -n prometheus

Lens config:
Prometheuse operator
prometheus/prometheus-kube-prometheus-prometheus:9090/

Default Grafana credentials: admin/prom-operator