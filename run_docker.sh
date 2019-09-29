sudo docker run \
-it --rm \
--runtime=nvidia \
-e NVIDIA_VISIBLE_DEVICES=0 \
--user root \
--net host \
-v $(pwd)/:/AdverseDrive \
-e NB_UID=$(id -u) \
-e NB_GID=$(id -g) \
-e GRANT_SUDO=yes \
xzgroup/adversedrive:latest \
/bin/bash
