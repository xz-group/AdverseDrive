sudo docker run \
  -it \
  --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0 \
  --net="host" \
  xzgroup/carla:latest \
  /bin/bash CarlaUE4.sh /Game/Maps/Town01_nemesisA \
  -benchmark \
  -carla-server \
  -fps=10 \
  -world-port=2000 \
  -windowed -ResX=100 -ResY=100 \
  -carla-no-hud
