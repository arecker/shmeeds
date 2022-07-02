.PHONY: run
run: shmeeds
	SLACK_WEBHOOK_URL="$$(pass slack/reckers/webhook)" \
	FEED_URL="https://www.alexrecker.com/feed.xml" \
	./shmeeds

shmeeds: $(wildcard *.go)
	go mod download
	go build ./...


.PHONY: docker
docker:
	docker build --progress=plain -t "arecker/shmeeds:latest" .
