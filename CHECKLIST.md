1. Update the extensions' versions in their `manifest.json` (Chrome) and `package.json` (Fire) files.
2. Run the build script: `bash scripts/deploy.sh`. This runs the Python unit tests, builds the front-ends, and zip's the Chrome extension.
3. Compress the Firefox extension by running `cfx xpi` after entering the Firefox `virtualenv`.
4. Move the compiled `xpi` file into `g2e/static`.
5. Update the Chrome web store.
6. Push the updated repo with `RCX` in the commit message, where `X` is the date.
7. `ssh` into Loretta.
8. Navigate to `/home/maayan/g2e/` and pull the latest changes.
9. Run `sudo /etc/g2e/apachectl restart`.
