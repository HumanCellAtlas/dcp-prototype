IMAGE=corpora-upload-${DEPLOYMENT_STAGE}

# make build
#	build a local image for testing
# make push
#	push the latest local image to the ECR repository

bump_version:
	expr `cat VERSION` + 1 > VERSION

build:
	docker build -t $(IMAGE) -f ../../Dockerfile.processing_image ../..

login:
	$(eval REPOSITORY_URI = $(shell aws ecr describe-repositories --repository-name $(IMAGE) | jq -r '.repositories[].repositoryUri'))
	$(eval ECR_URI = $(shell dirname $(REPOSITORY_URI)))
	aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $(ECR_URI)

push: login 
	$(eval REPOSITORY_URI = $(shell aws ecr describe-repositories --repository-name $(IMAGE) | jq -r '.repositories[].repositoryUri'))
	$(eval VERSION=$(shell cat VERSION))
	docker tag $(IMAGE):latest $(REPOSITORY_URI):$(VERSION)
	docker push $(REPOSITORY_URI):$(VERSION)

promote: login
	$(eval REPOSITORY_URI = $(shell aws ecr describe-repositories --repository-name $(IMAGE) | jq -r '.repositories[].repositoryUri'))
	$(eval VERSION=$(shell cat VERSION))
	docker tag $(REPOSITORY_URI):$(VERSION) $(REPOSITORY_URI):active
	docker push $(REPOSITORY_URI):active

.phony: build bump_version promote push login
