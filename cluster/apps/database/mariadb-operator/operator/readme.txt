when operator fails with: MARIADB_AUTO_UPGRADE
do
- scale deployment to 0
- edit deployment and add env with AUtO_UPGRADE
- scale deployment to 1

  env:
  - name: MARIADB_AUTO_UPGRADE
    value: "true"