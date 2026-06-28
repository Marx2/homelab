# Frigate

## Face Recognition

Frigate 0.16-beta4 has a UI bug — uploading photos via Faces UI does not trigger
the embedding model. After uploading, run the script manually to register the faces.

### Usage

Register all people:
```sh
./register-faces.sh
```

Register one person:
```sh
./register-faces.sh Marek
```

### Full workflow

1. Frigate UI → **Faces** → create person → upload photos (clear, front-facing, well-lit)
2. Run `./register-faces.sh <name>`
3. On next `person` alert, Frigate will add the matched name as a sub-label instead of `unknown`
