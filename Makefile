# https://stackoverflow.com/questions/30088319/using-shell-in-makefile-to-find-ubuntu-version
OS_VERS := $(shell lsb_release -a 2>/dev/null | grep Description | awk '{ print $$2 "-" $$3 }')
SUPPORTED_DEV_ENV = Ubuntu-18.04
RM = rm -rf
DOCKER_EXEC=docker exec -it
DOCKER_COMPOSE=docker-compose -f compose/docker-compose.yml

.PHONY: all
all: 
	$(DOCKER_COMPOSE) build

checkrelease:
	@echo "checking your development environment"
ifneq (,$(findstring $(SUPPORTED_DEV_ENV),$(OS_VERS)))
	@echo "supported environment $(OS_VERS) found"
else
	@echo "your operating system is not supported for development!"
	@false
endif

.PHONY: develop
develop: checkrelease
	$(MAKE) -C develop all
	( cd test && make develop )

.PHONY: test
test: all
	@echo "running tests"
	$(DOCKER_COMPOSE) up -d
	$(DOCKER_EXEC) compose_daphne_1 python manage.py test --parallel 4
	@( cd test && make unittest )
	$(DOCKER_COMPOSE) stop && $(DOCKER_COMPOSE) rm -fv

.PHONY: clean
clean:
	@echo "cleaning system"
	@$(DOCKER_COMPOSE) stop && $(DOCKER_COMPOSE) rm -fv
	@sudo $(RM) /opt/tbot

# Run targets
.PHONY: run
run:
	cd compose && docker-compose up -d --build
