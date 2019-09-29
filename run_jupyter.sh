sudo nvidia-docker run -it -e NVIDIA_VISIBLE_DEVICES=0 --rm --user root --net host -v $(pwd)/:/tf -e NB_UID=$(id -u) -e NB_GID=$(id -g) -e GRANT_SUDO=yes deep-jupyter/xz:v1
