package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
	"github.com/mmcdole/gofeed"
)

func isTesting() bool {
	val, exists := os.LookupEnv("TESTING")
	if !exists {
		return false
	}
	return val == "1" || val == "true"
}

func shouldCheckDate() bool {
	val, exists := os.LookupEnv("CHECK_DATE")
	if !exists {
		return true
	}
	return val == "1" || val == "true"
}

func readEnvOrBail(key string) string {
	val, exists := os.LookupEnv(key)
	if !exists || val == "" {
		log.Fatalf("%s=\"...\" is not set!", key)
		os.Exit(1)
	}
	return val
}

func postSlack(body string) error {
	data := map[string]string{
		"text":       body,
		"channel":    "#blog",
		"username":   "reckerbot",
		"icon_emoji": ":reckerbot",
	}
	payload, err := json.Marshal(data)
	if err != nil {
		return err
	}
	url := readEnvOrBail("SLACK_WEBHOOK_URL")

	if isTesting() {
		log.Printf("(skipping HTTP post for testing)")
		return nil
	}

	_, err = http.Post(url, "application/json", bytes.NewBuffer(payload))
	if err != nil {
		return err
	}

	return nil
}

func postTweet(body string) error {
	config := oauth1.NewConfig(readEnvOrBail("TWEET_CONSUMER_API_KEY"), readEnvOrBail("TWEET_CONSUMER_API_SECRET_KEY"))
	token := oauth1.NewToken(readEnvOrBail("TWEET_ACCESS_TOKEN"), readEnvOrBail("TWEET_ACCESS_TOKEN_SECRET"))
	httpClient := config.Client(oauth1.NoContext, token)
	client := twitter.NewClient(httpClient)

	if isTesting() {
		log.Printf("(skipping tweet for testing)")
		return nil
	}
	_, _, err := client.Statuses.Update(body, nil)
	return err
}

func fetchTodaysEntry(url string) (*gofeed.Item, error) {
	fp := gofeed.NewParser()

	var latest *gofeed.Item
	var err error

	for {
		feed, err := fp.ParseURL(url)
		if err != nil {
			return latest, err
		}

		latest = feed.Items[0]

		if !shouldCheckDate() {
			log.Printf("skipping date comparison, since CHECK_DATE=\"...\" disabled")
			break
		}

		// check date
		todaysDate := time.Now().Format("01-02-2006")
		thisDate := latest.PublishedParsed.Format("01-02-2006")

		if todaysDate == thisDate {
			break
		}

		log.Printf("entry date %s does not match today's date %s, waiting...", thisDate, todaysDate)
		time.Sleep(5 * time.Second)
	}

	return latest, err
}

func main() {
	feedUrl := readEnvOrBail("FEED_URL")

	latest, err := fetchTodaysEntry(feedUrl)
	if err != nil {
		log.Fatalf("error fetching %s: %s", feedUrl, err)
		os.Exit(1)
	}
	log.Printf("successfully downloaded latest entry \"%s\"", latest.Description)

	body := fmt.Sprintf("%s\n%s\n%s", latest.Title, latest.Description, latest.Link)
	err = postSlack(body)
	if err != nil {
		log.Fatalf("failed to post entry to slack: %s", err)
		os.Exit(1)
	}
	log.Printf("successfully shared \"%s\" to slack", latest.Description)

	err = postTweet(body)
	if err != nil {
		log.Fatalf("failed to post entry to twitter: %s", err)
		os.Exit(1)
	}
	log.Printf("successfully shared \"%s\" to twitter", latest.Description)
}
