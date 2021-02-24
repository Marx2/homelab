secret creation:
- encode address
echo -n "https://hooks.slack.com/services/XXXXXXXXXXXXXXXXX" | base64
- put into adress field
- seal
kubeseal <slack-secret-org.yaml >slack-secret.yaml --format yaml