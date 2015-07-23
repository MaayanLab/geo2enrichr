General deployment steps:
=
1. Git commit the repo with `RCX` in the commit message, where `X` is the date.

To deploy the extensions
=
2. Update the extensions' versions in their `manifest.json` (Chrome) and `package.json` (Fire) files.
3. Zip compress the Chrome extension.
4. Compress the Firefox extension by running `cfx xpi` after entering the Firefox `virtualenv`.
5. Move the compiled `xpi` file into `g2e/static`.
6. Update the Chrome web store.
7. Resubmit the Firefox add-on for approval.

To deploy the web application
=
2. Run `build.sh` with the first argument 'prod' for production, 'dev' for development
   and an optional second argument 'skip' to skip tests. This will automatically configure
   the connection to the correct database as well.
3. Run `deploy.sh`