1. Run the build script: `bash scripts/deploy.sh`. This runs the Python unit tests, builds the front-ends.
2. Update the extensions' versions in their `manifest.json` (Chrome) and `package.json` (Fire) files.
3. Zip compress the Chrome extension.
4. Compress the Firefox extension by running `cfx xpi` after entering the Firefox `virtualenv`.
5. Move the compiled `xpi` file into `g2e/static`.
6. Update the Chrome web store.
7. Push the updated repo with `RCX` in the commit message, where `X` is the date.
8. `ssh` into Loretta.
9. Navigate to `/home/maayan/g2e/` and pull the latest changes.
10. Run `sudo /etc/g2e/apachectl restart`.
