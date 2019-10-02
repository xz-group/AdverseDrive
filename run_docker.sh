echo "Checking docker version...";
if echo $(sudo docker --version) | grep -Eq '19.0[3-9]|19.[1-9][0-9]|20' ; then
    echo "Docker version >= 19.03 detected...";
    sudo docker run \
    -it --rm \
    --gpus 0 \
    --user root \
    --net host \
    -v $(pwd)/:/AdverseDrive \
    -e NB_UID=$(id -u) \
    -e NB_GID=$(id -g) \
    -e GRANT_SUDO=yes \
    xzgroup/adversedrive:latest \
    /bin/bash;
else
    echo "Docker version < 19.03 detected...";
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
    /bin/bash;
fi
