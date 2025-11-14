REGION = sa-east-1
IMAGE = br_cities_autocomplete
IMAGE_TAG = latest
ACCOUNT_ID = 329599618304
ECR_REPO = $(ACCOUNT_ID).dkr.ecr.${REGION}.amazonaws.com/$(IMAGE)

build:
	docker buildx build --platform linux/amd64 --provenance=false -t $(IMAGE):test .

test:
	@printf "%b" "In a new shell execute:\n\
	curl localhost:9000/2015-03-31/functions/function/invocations -d {}\n\n"
	docker run --platform linux/amd64 -p 9000:8080 $(IMAGE):test

deploy: build
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ECR_REPO)
#	Uncomment the following line if the ECR repository does not exist
# 	aws ecr create-repository --repository-name br_cities_autocomplete --region $(REGION) --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
	docker tag $(IMAGE):test $(ECR_REPO):$(IMAGE_TAG)
	docker push $(ECR_REPO):$(IMAGE_TAG)