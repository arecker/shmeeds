SLACK_SECRETS := SLACK_WEBHOOK_URL="$$(pass slack/reckers/webhook)"
TWEET_SECRETS := TWEET_ACCESS_TOKEN="$$(pass twitter/reckerbot/access-token)" \
		 TWEET_ACCESS_TOKEN_SECRET="$$(pass twitter/reckerbot/access-token-secret)" \
		 TWEET_CONSUMER_API_KEY="$$(pass twitter/reckerbot/consumer-api-key)" \
		 TWEET_CONSUMER_API_SECRET_KEY="$$(pass twitter/reckerbot/consumer-api-secret-key)"

.PHONY: run
run: shmeeds
	TESTING="1" \
	$(SLACK_SECRETS) $(TWEET_SECRETS) \
	FEED_URL="https://www.alexrecker.com/feed.xml" \
	./shmeeds

shmeeds: $(wildcard *.go)
	go mod download
	go build ./...


.PHONY: docker
docker:
	docker build --progress=plain -t "arecker/shmeeds:latest" .
