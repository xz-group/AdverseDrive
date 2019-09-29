# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
#
# THIS IS A GENERATED DOCKERFILE.
#
# This file was assembled from multiple pieces, whose use is documented
# throughout. Please refer to the TensorFlow dockerfiles documentation
# for more information.

ARG UBUNTU_VERSION=16.04

ARG ARCH=
ARG CUDA=9.0
FROM nvidia/cuda${ARCH:+-$ARCH}:${CUDA}-base-ubuntu${UBUNTU_VERSION} as base
# ARCH and CUDA are specified again because the FROM directive resets ARGs
# (but their default value is retained if set previously)
ARG ARCH
ARG CUDA
ARG CUDNN=7.4.1.5-1
ARG CUDNN_MAJOR_VERSION=7
ARG LIB_DIR_PREFIX=x86_64

# Needed for string substitution
SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cuda-command-line-tools-${CUDA/./-} \
        cuda-cublas-dev-${CUDA/./-} \
        cuda-cudart-dev-${CUDA/./-} \
        cuda-cufft-dev-${CUDA/./-} \
        cuda-curand-dev-${CUDA/./-} \
        cuda-cusolver-dev-${CUDA/./-} \
        cuda-cusparse-dev-${CUDA/./-} \
        libcudnn7=${CUDNN}+cuda${CUDA} \
        libcudnn7-dev=${CUDNN}+cuda${CUDA} \
        libcurl3-dev \
        libfreetype6-dev \
        libhdf5-serial-dev \
        libzmq3-dev \
        pkg-config \
        rsync \
        software-properties-common \
        unzip \
        zip \
        zlib1g-dev \
        wget \
        git \
        nano \
        && \
    find /usr/local/cuda-${CUDA}/lib64/ -type f -name 'lib*_static.a' -not -name 'libcudart_static.a' -delete && \
    rm /usr/lib/${LIB_DIR_PREFIX}-linux-gnu/libcudnn_static_v7.a

RUN [[ "${ARCH}" = "ppc64le" ]] || { apt-get update && \
        apt-get install nvinfer-runtime-trt-repo-ubuntu1604-5.0.2-ga-cuda${CUDA} \
        && apt-get update \
        && apt-get install -y --no-install-recommends \
            libnvinfer5=5.0.2-1+cuda${CUDA} \
            libnvinfer-dev=5.0.2-1+cuda${CUDA} \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*; }

# Configure the build for our CUDA configuration.
ENV CI_BUILD_PYTHON python
ENV LD_LIBRARY_PATH /usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH
ENV TF_NEED_CUDA 1
ENV TF_NEED_TENSORRT 1
ENV TF_CUDA_COMPUTE_CAPABILITIES=3.5,5.2,6.0,6.1,7.0
ENV TF_CUDA_VERSION=${CUDA}
ENV TF_CUDNN_VERSION=${CUDNN_MAJOR_VERSION}
# CACHE_STOP is used to rerun future commands, otherwise cloning tensorflow will be cached and will not pull the most recent version
ARG CACHE_STOP=1
# Check out TensorFlow source code if --build-arg CHECKOUT_TF_SRC=1
ARG CHECKOUT_TF_SRC=0
RUN test "${CHECKOUT_TF_SRC}" -eq 1 && git clone https://github.com/tensorflow/tensorflow.git /tensorflow_src || true

ARG USE_PYTHON_3_NOT_2=True
ARG _PY_SUFFIX=${USE_PYTHON_3_NOT_2:+3}
ARG PYTHON=python${_PY_SUFFIX}
ARG PIP=pip${_PY_SUFFIX}

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y \
    ${PYTHON} \
    ${PYTHON}-pip

RUN ${PIP} --no-cache-dir install --upgrade \
    pip \
    setuptools

# Some TF tools expect a "python" binary
RUN ln -s $(which ${PYTHON}) /usr/local/bin/python

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    openjdk-8-jdk \
    ${PYTHON}-dev \
    swig \
    libsm6 \
    libxext6 \
    libxrender-dev

RUN ${PIP} --no-cache-dir install \
    cmake \
    psutil \
    Pillow \
    h5py \
    keras_applications \
    keras_preprocessing \
    matplotlib \
    mock \
    numpy \
    scipy \
    sklearn \
    pandas \
    opencv-python \
    bayesian-optimization==1.0.1 \
    imutils \
    gym \
    seaborn \
    && test "${USE_PYTHON_3_NOT_2}" -eq 1 && true || ${PIP} --no-cache-dir install \
    enum34

# Carla requirements
RUN ${PIP} --no-cache-dir install \
  absl-py==0.1.13 \
  astor==0.6.2 \
  backcall==0.1.0 \
  bleach==1.5.0 \
  configparser==3.5.0 \
  cycler==0.10.0 \
  cython==0.28.2 \
  decorator==4.3.0 \
  dlib==19.16.0 \
  entrypoints==0.2.3 \
  enum34==1.1.6 \
  gast==0.2.0 \
  grpcio==1.10.0 \
  imgaug==0.2.5 \
  ipykernel==4.8.2 \
  ipython==6.3.0 \
  ipython-genutils==0.2.0 \
  ipywidgets==7.2.0 \
  jedi==0.11.1 \
  jinja2==2.10 \
  jsonschema==2.6.0 \
  keras==2.2.4 \
  kiwisolver==1.0.1 \
  markdown==2.6.11 \
  markupsafe==1.0 \
  matplotlib==2.2.2 \
  mistune==0.8.3 \
  mock==2.0.0 \
  nbconvert==5.3.1 \
  nbformat==4.4.0 \
  networkx==2.1 \
  notebook==5.4.1 \
  numpy==1.15.3 \
  opencv-python==3.4.0.12 \
  pandas==0.22.0 \
  pandocfilters==1.4.2 \
  parso==0.1.1 \
  pbr==4.0.2 \
  pexpect==4.4.0 \
  pickleshare==0.7.4 \
  pid==2.2.0 \
  pid-controller==0.2.0 \
  pillow==5.3.0 \
  prompt-toolkit==1.0.15 \
  protobuf==3.6.1 \
  psutil==5.6.1 \
  ptyprocess==0.5.2 \
  pygame==1.9.4 \
  pygments==2.2.0 \
  pyparsing==2.2.0 \
  python-dateutil==2.7.2 \
  py_trees==0.8.3 \
  pytz==2018.4 \
  pywavelets==0.5.2 \
  pyyaml==3.12 \
  pyzmq==17.0.0 \
  qtconsole==4.3.1 \
  scikit-image==0.13.1 \
  scipy==1.0.1 \
  seaborn==0.8.1 \
  send2trash==1.5.0 \
  simplegeneric==0.8.1 \
  tensorflow-gpu==1.12.0 \
  tensorboard==1.12.0 \
  termcolor==1.1.0 \
  terminado==0.8.1 \
  testpath==0.3.1 \
  torch==1.1.0 \
  torchvision==0.2.2 \
  tornado==5.0.1 \
  traitlets==4.3.2 \
  wcwidth==0.1.7 \
  webencodings==0.5.1 \
  werkzeug==0.14.1 \
  widgetsnbextension==3.2.0

# Install bazel
ARG BAZEL_VERSION=0.19.2
RUN mkdir /bazel && \
    wget -O /bazel/installer.sh "https://github.com/bazelbuild/bazel/releases/download/${BAZEL_VERSION}/bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh" && \
    wget -O /bazel/LICENSE.txt "https://raw.githubusercontent.com/bazelbuild/bazel/master/LICENSE" && \
    chmod +x /bazel/installer.sh && \
    /bazel/installer.sh && \
    rm -f /bazel/installer.sh


COPY bashrc /etc/bash.bashrc
RUN chmod a+rwx /etc/bash.bashrc

RUN ${PIP} install jupyter matplotlib
RUN ${PIP} install jupyter_http_over_ws
RUN jupyter serverextension enable --py jupyter_http_over_ws

RUN mkdir /.local && chmod a+rwx /.local
RUN apt-get install -y --no-install-recommends wget

RUN apt-get autoremove -y
RUN apt-get update -y

RUN apt-get update -y
RUN apt-get install -y libpng16-16

#RUN apt-get autoremove -y && apt-get remove -y wget
RUN apt-get install x11-xserver-utils -y

RUN apt-get install python3-tk -y
RUN apt-get install graphviz -y

WORKDIR /AdverseDrive
EXPOSE 8888

RUN ${PYTHON} -m ipykernel.kernelspec

# CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/AdverseDrive --ip 0.0.0.0 --no-browser --allow-root"]
CMD ["bash", "-c", "source /etc/bash.bashrc && xhost +"]
