import json
import boto3

# Initialize the Amazon Comprehend client
comprehend_client = boto3.client("comprehend")


def lambda_handler(event, context):
    # 1. Extract the user review from the incoming event
    # If no review is provided in the test event, we use a default fallback string
    review_text = event.get(
        "review", "The product was okay, but delivery was delayed."
    )

    print(f"--- Incoming Review Text ---")
    print(review_text)

    try:
        # 2. Use Amazon Comprehend to detect the sentiment
        # LanguageCode 'en' stands for English
        response = comprehend_client.detect_sentiment(
            Text=review_text, LanguageCode="en"
        )

        sentiment = response["Sentiment"]
        sentiment_scores = response["SentimentScore"]

        # 3. Log the sentiment results beautifully
        print("\n--- Sentiment Analysis Results ---")
        print(f"Overall Sentiment Result: {sentiment}")
        print(f"Confidence Scores:")
        print(f"  - Positive: {sentiment_scores['Positive']:.4f}")
        print(f"  - Negative: {sentiment_scores['Negative']:.4f}")
        print(f"  - Neutral:  {sentiment_scores['Neutral']:.4f}")
        print(f"  - Mixed:    {sentiment_scores['Mixed']:.4f}")

        # Return a clean JSON response back to the caller
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Sentiment analysis completed successfully.",
                    "detected_sentiment": sentiment,
                    "scores": sentiment_scores,
                }
            ),
        }

    except Exception as e:
        print(f"Error analyzing sentiment: {str(e)}")
        raise e