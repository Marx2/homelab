when operator fails with: MARIADB_AUTO_UPGRADE
do edit deployment and add to env:

  env:
  - name: MARIADB_AUTO_UPGRADE
    value: "true"