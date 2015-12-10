# Deploying GEO2Enrichr

### General steps
- Git commit the repo with `RCX` in the commit message, where `X` is the date.

### To deploy the Chrome extension
- Update the extension's versions in `manifest.json` (Chrome).
- Zip compress the Chrome extension.
- Update the Chrome web store.

### To deploy the Firefox extension*
- See [this documentation](https://developer.mozilla.org/en-US/Add-ons/SDK/Tools/cfx).
- Compress the Firefox extension by running `cfx xpi` after entering the Firefox `virtualenv`.
- Move the compiled `xpi` file into `g2e/static`.
- Resubmit the Firefox add-on for approval.

\* **Firefox is deprecated because the approval process is too strict and the requirements would require almost separate codebases for the two extensions. This was not the case when GEO2Enrichr was first published.**

### To deploy the web application
- Run `build.sh` with these arguments:
    - `$1` - 'prod' for production, 'dev' for development
    - `$2` - 'skip' to skip tests
    - `$3` - 'build' to build the Docker container.
    - `$4` - 'push' to push to the Docker repo.
- Restart G2E on Marathon.
- To redeploy completely, see `g2e.json` in the `marathon-deployments` repo on our GitLab.