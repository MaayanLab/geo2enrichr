General deployment steps:
=
1. Run the build script: `bash deploy.sh`. This runs the Python unit tests, builds the front-ends.
2. Push the updated repo with `RCX` in the commit message, where `X` is the date.

To deploy the extensions
=
3. Update the extensions' versions in their `manifest.json` (Chrome) and `package.json` (Fire) files.
4. Zip compress the Chrome extension.
5. Compress the Firefox extension by running `cfx xpi` after entering the Firefox `virtualenv`.
6. Move the compiled `xpi` file into `g2e/static`.
7. Update the Chrome web store.
8. Resubmit the Firefox add-on for approval.

To deploy the web application
=
3. Configure application to use production database
   ** Never revision control this change or the config files! **
   In g2e/orm/commondb.py, change prod file from 'db-dev.conf' to 'db-prod.conf'
4. Run `build.sh`
5. Run `deploy.sh`