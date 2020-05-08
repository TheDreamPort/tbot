DOCKER_COMPOSE_VERSION=1.25.4
DOCKER_COMPOSE_URL=https://github.com/docker/compose/releases/download/$(DOCKER_COMPOSE_VERSION)/docker-compose-
DOCKER_COMPOSE_BASH_COMPLETION_URL=https://raw.githubusercontent.com/docker/compose/$(DOCKER_COMPOSE_VERSION)/contrib/completion/bash/docker-compose

.PHONY: all
all: basic_deps docker_deps docker_compose_deps yarn_deps java_deps ansible_deps inotify_deps node_deps

basic_deps:
	sudo apt update
	sudo apt upgrade -y
	sudo apt install -y make curl apt-transport-https ca-certificates gnupg-agent software-properties-common gcc libpq-dev python3-dev python python-pip net-tools vim
	touch basic_deps

docker.gpg: basic_deps
	curl -f -o docker.gpg https://download.docker.com/linux/ubuntu/gpg

docker_deps: basic_deps docker.gpg
	gpg -nq --import --import-options import-show docker.gpg | grep 9DC858229FC7DD38854AE2D88D81803C0EBFCD88 || (echo "fingerprint does not match" && false)
	sudo apt-key add docker.gpg
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
	sudo apt update
	sudo apt upgrade -y
	sudo apt install -y docker-ce docker-ce-cli containerd.io
	sudo systemctl enable docker
	sudo usermod -a -G docker `whoami`
	touch docker_deps

docker_compose_deps: basic_deps docker_deps
	sudo curl -L $(DOCKER_COMPOSE_URL)$(shell uname -s)-$(shell uname -m) -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
	sudo curl -L $(DOCKER_COMPOSE_BASH_COMPLETION_URL) -o /etc/bash_completion.d/docker-compose
	touch docker_compose_deps

node.gpg:
	curl -f -o node.gpg https://deb.nodesource.com/gpgkey/nodesource.gpg.key

node_deps: basic_deps node.gpg
	gpg -nq --import --import-options import-show node.gpg | grep 9FD3B784BC1C6FC31A8A0A1C1655A0AB68576280 || (echo "fingerprint does not match" && false)
	sudo apt-key add node.gpg
	sudo add-apt-repository "deb https://deb.nodesource.com/node_12.x bionic main"
	sudo apt install -y nodejs
	touch node_deps

yarn.gpg: basic_deps
	curl -f -o yarn.gpg https://dl.yarnpkg.com/debian/pubkey.gpg

yarn_deps: basic_deps node_deps yarn.gpg
	gpg -nq --import --import-options import-show yarn.gpg | grep 72ECF46A56B4AD39C907BBB71646B01B86E50310 || (echo "fingerprint does not match" && false)
	sudo apt-key add yarn.gpg
	sudo add-apt-repository "deb https://dl.yarnpkg.com/debian/ stable main"
	sudo apt install -y yarn
	touch yarn_deps

ansible_deps: basic_deps
	sudo apt update
	sudo apt install software-properties-common
	sudo apt-add-repository --yes --update ppa:ansible/ansible
	sudo apt install -y ansible
	touch ansible_deps

java_deps: basic_deps
	sudo apt install -y maven openjdk-11-jdk
	touch java_deps

inotify_deps:
	echo fs.inotify.max_user_watches=524288 | sudo tee /etc/sysctl.d/40-max-user-watches.conf
	sudo sysctl --system
	touch inotify_deps

.PHONY: clean
clean:
	rm -f basic_deps docker.gpg docker_deps docker_compose_deps yarn.gpg yarn_deps java_deps ansible_deps inotify_deps node.gpg node_deps
