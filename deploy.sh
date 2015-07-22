# DOCKER_IMAGE='146.203.54.165:5000/g2e:latest'

# We use an insecure, private registry. Tell Docker to go ahead anyway.
# boot2docker sshcurl post t "echo $'EXTRA_ARGS=\"--insecure-registry 146.203.54.165:5000\"' | sudo tee -a /var/lib/boot2docker/profile && sudo /etc/init.d/docker restart"

# docker push $DOCKER_IMAGE

# JSON for Marathon
data='{
    "instances": 1,
    "cpus": 1,
    "mem": 2048,
    "constraints": [
        [ "hostname", "CLUSTER", "charlotte.1425mad.mssm.edu" ]
    ],
    "container": {
        "type": "DOCKER",
        "docker": {
            "image": "$DOCKER_IMAGE",
            "forcePullImage": true,
            "network": "BRIDGE",
            "portMappings": [
                {
                    "containerPort": 80,
                    "hostPort": 0,
                    "protocol": "tcp",
                    "servicePort": 10009
                }
            ]
        },
        "volumes": [
            {
                "containerPath": "/g2e/g2e/static",
                "hostPath": "/data/g2e/static",
                "mode": "RW"
            }
        ]
    },
    "labels": {
       "public": "true"
    }
}'

curl -i \
    -H "Accept: application/json" \
    -H "Content-Type:application/json" \
    -X POST --data '$data' maayanlab:systemsbiology@elizabeth:8080/v2/apps/g2e