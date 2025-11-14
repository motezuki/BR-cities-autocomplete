build:
	docker buildx build --platform linux/amd64 --provenance=false -t docker-image:test .

test:
	@printf "%b" "In a new shell execute:\n\
	curl localhost:9000/2015-03-31/functions/function/invocations -d {}\n\n"
	docker run --platform linux/amd64 -p 9000:8080 docker-image:test