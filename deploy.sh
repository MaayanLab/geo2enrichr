DOCKER_IMAGE='146.203.54.165:5000/g2e:latest'

docker push $DOCKER_IMAGE

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