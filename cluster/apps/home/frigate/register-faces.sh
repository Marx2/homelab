#!/usr/bin/env bash
# Register all face images uploaded via Frigate UI with the embedding model.
# Run after uploading new face photos in Frigate UI → Faces.
#
# Usage: ./register-faces.sh [person_name]
#   No args: registers all people
#   With arg: registers only that person, e.g. ./register-faces.sh Marek

set -euo pipefail

FRIGATE_POD=$(kubectl get pod -n home -l app.kubernetes.io/name=frigate -o jsonpath='{.items[0].metadata.name}')
FACES_DIR="/media/frigate/clips/faces"

register_person() {
  local name="$1"
  echo "==> Registering: $name"
  local count=0
  local errors=0

  while IFS= read -r file; do
    result=$(kubectl exec -n home "$FRIGATE_POD" -- \
      curl -s -X POST "http://localhost:5000/api/faces/${name}/register" \
      -F "file=@${file}")
    success=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin).get('success','?'))" 2>/dev/null || echo "?")
    if [ "$success" = "True" ]; then
      count=$((count + 1))
    else
      msg=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin).get('message','unknown'))" 2>/dev/null || echo "parse error")
      echo "    SKIP $(basename "$file"): $msg"
      errors=$((errors + 1))
    fi
  done < <(kubectl exec -n home "$FRIGATE_POD" -- find "${FACES_DIR}/${name}" -maxdepth 1 -name '*.webp' -o -name '*.jpg' -o -name '*.png' 2>/dev/null)

  echo "    OK: $count  Failed: $errors"
}

if [ $# -eq 1 ]; then
  register_person "$1"
else
  while IFS= read -r name; do
    [ "$name" = "train" ] && continue
    register_person "$name"
  done < <(kubectl exec -n home "$FRIGATE_POD" -- \
    find "$FACES_DIR" -mindepth 1 -maxdepth 1 -type d -exec basename {} \;)
fi

echo "Done."
