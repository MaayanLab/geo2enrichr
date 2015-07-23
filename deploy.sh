DOCKER_IMAGE='146.203.54.165:5000/g2e:latest'

# We use an insecure, private registry. Tell Docker to go ahead anyway.
# boot2docker sshcurl post t "echo $'EXTRA_ARGS=\"--insecure-registry 146.203.54.165:5000\"' | sudo tee -a /var/lib/boot2docker/profile && sudo /etc/init.d/docker restart"

docker push $DOCKER_IMAGE