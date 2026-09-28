PORT ?= 80
IMAGE_NAME = leaderboard
CONTAINER_NAME = leaderboard

.PHONY: serve build docker-up docker-down

serve:
	cd .. && uv run uvicorn leaderboard.app:app --host 0.0.0.0 --port $(PORT)

build:
	cd .. && docker build -f leaderboard/Dockerfile -t $(IMAGE_NAME) .

docker-up: build
	docker run -d \
		--name $(CONTAINER_NAME) \
		--restart unless-stopped \
		-p $(PORT):$(PORT) \
		-v $(shell cd .. && pwd):/app/src \
		-w /app/src \
		$(IMAGE_NAME) \
		uv run uvicorn leaderboard.app:app --host 0.0.0.0 --port $(PORT)

docker-down:
	docker stop $(CONTAINER_NAME) 2>/dev/null || true
	docker rm $(CONTAINER_NAME) 2>/dev/null || true
