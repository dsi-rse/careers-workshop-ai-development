IMAGE_NAME=lecture_2

.PHONY: build notebook interactive leaderboard

# Common Docker run flags
COMMON_DOCKER_FLAGS= \
	-v $(shell pwd):/app/src \
	-w /app/src

build:
	docker build . -t $(IMAGE_NAME)

interactive: build
	docker run -it \
	$(COMMON_DOCKER_FLAGS) \
	$(IMAGE_NAME) /bin/bash

notebook: build
	docker run -it -p 8888:8888 \
	$(COMMON_DOCKER_FLAGS) \
	$(IMAGE_NAME) \
	uv run jupyter notebook --allow-root --no-browser \
	--port 8888 --ip=0.0.0.0

leaderboard: build
	docker run -it -p 8000:8000 \
	$(COMMON_DOCKER_FLAGS) \
	$(IMAGE_NAME) \
	uv run uvicorn leaderboard.app:app --host 0.0.0.0 --port 8000

