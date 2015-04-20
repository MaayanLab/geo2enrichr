1. Run the build script: `bash scripts/deploy.sh`. This runs the Python unit tests, builds the front-ends.
2. Update the extensions' versions in their `manifest.json` (Chrome) and `package.json` (Fire) files.
3. Zip compress the Chrome extension.
4. Compress the Firefox extension by running `cfx xpi` after entering the Firefox `virtualenv`.
5. Move the compiled `xpi` file into `g2e/static`.
6. Update the Chrome web store.
7. Push the updated repo with `RCX` in the commit message, where `X` is the date.
8. `ssh` into Loretta.
9. Run `cd /g2d/`
10. Run `git pull` (you may have to specify the remote)
11. Run `docker ps` to get the running containers; find GEO2Enrichr's ("g2e")
12. Run `docker restart <container ID>` to restart the docker container

docker run -it -p 8084:80 -v /home/maayanlab/g2e/g2e/static:/g2e/g2e/static g2e:latest
