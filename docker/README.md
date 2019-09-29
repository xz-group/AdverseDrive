# AdverseDrive Docker

### Prerequisites

1. Install `docker`
2. Install `nvidia-docker2`
3. Add user to docker group

### Build Docker

Change `groupname` and `version` as needed.

```
sudo docker build -t groupname/AdverseDrive:version .
```

### Use Built docker

Simple command:
```
sudo docker run \
-it --rm \
--runtime=nvidia \
--user root \
--net host \
-v $(pwd)/:/AdverseDrive \
groupname/AdverseDrive:version /bin/bash
```

Server ready command:
```
sudo docker run \
-it --rm \
--runtime=nvidia \
--user root \
--net host \
-v $(pwd)/:/AdverseDrive \
-e NB_UID=$(id -u) \
-e DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
-e NB_GID=$(id -g) \
-e GRANT_SUDO=yes \
groupname/AdverseDrive:version /bin/bash
```

Alternatively use (in root directory):

```
sh run_docker.sh
```

Note:
- This docker is Carla ready
- This docker is Jupyter Notebook ready
- Docker allows pygame visualization on servers with VNC/desktop mode enabled
