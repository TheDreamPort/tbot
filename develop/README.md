# Minnow Develop

This build target will attempt to quick install all necessary developer dependencies, as described below.  The automated process is intended for a Ubuntu 18.04 minimal desktop install, but it should work for future versions as well.  For non-ubuntu environments, pay special attention to the version numbers, as the default package managers might not match.

## Basic Requirements

Upgrade and install the basic OS dependencies.

1. sudo apt update
2. sudo apt upgrade -y
3. sudo apt install -y git make curl apt-transport-https ca-certificates gnupg-agent software-properties-common gcc libpq-dev python3-dev python python-pip net-tools vim

## Git Submodules

If you did not use --recurse-submodules when you cloned the main respository, the following command will get them now.

- git submodule update --init

## Docker Community Edition

Install the latest docker community edition engine from the docker's own repository using these instructions: https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository

1. curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
2. sudo apt-key fingerprint '9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88'
3. sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
4. sudo apt update
5. sudo apt upgrade -y
6. sudo apt install -y docker-ce docker-ce-cli containerd.io
7. sudo systemctl enable docker
8. sudo usermod -a -G docker $(whoami)
9. newgrp docker
10. docker run hello-world

## Docker Compose

Install docker-compose and the docker-compose completions scripts from github.
* https://docs.docker.com/compose/install/
* https://docs.docker.com/compose/install/

1. sudo curl -L https://github.com/docker/compose/releases/download/1.25.4/docker-compose-Linux-x86_64 -o /usr/local/bin/docker-compose
2. sudo chmod +x /usr/local/bin/docker-compose
3. sudo curl -L https://raw.githubusercontent.com/docker/compose/1.25.4/contrib/completion/bash/docker-compose -o /etc/bash_completion.d/

## Node JS

The React Jest tests require node.js version >= 10, but the Ubuntu 18.04 repository only includes up to 8.10.

1. curl -fsSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | sudo apt-key add -
2. sudo apt-key fingerprint '9FD3 B784 BC1C 6FC3 1A8A  0A1C 1655 A0AB 6857 6280'
3. sudo add-apt-repository "deb https://deb.nodesource.com/node_12.x bionic main"
4. sudo apt install -y nodejs

## React Dependencies

This project uses yarn to manage the ReactJS dependencies, please do not use npm.

1. curl -fsSL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
2. sudo apt-key fingerprint '72EC F46A 56B4 AD39 C907  BBB7 1646 B01B 86E5 0310'
3. sudo add-apt-repository "deb https://dl.yarnpkg.com/debian/ stable main"
4. sudo apt install -y yarn

## Java Dependencies

The GRASSMARLIN plugin requires Java 11 and Maven 3.6.  *These are not the default packages on Fedora 31*

1. sudo apt install -y maven openjdk-11-jdk

## iNotify User Watchers

Both yarn and VisualStudio Code rely on a large number of inotify watchers.  The typical recommendation for development boxes is to increase this by a factor of 64.

1. echo fs.inotify.max_user_watches=524288 | sudo tee /etc/sysctl.d/40-max-user-watches.conf
2. sudo sysctl --system
