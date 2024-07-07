# Sentiment Analysis API

This Python application integrates a pre-trained sentiment analysis model and exposes an API endpoint for sentiment analysis. It also dockerizes the application for seamless deployment and integrates with a PostgreSQL database to store the analyzed data.

## Usage

1. Install Docker on your system if you haven't already.
2. Clone this repository to your local machine.
3. Navigate to the project directory.

4. Build the Docker image using the command:
    ```
    docker build -t sentiment-analysis-app .
    ```

5. Once the image is built, run the Docker container:
    ```
    docker run -p 5000:5000 sentiment-analysis-app
    ```

The API endpoint for sentiment analysis is available at `http://localhost:5000/analyze_sentiment`.

Send a POST request with JSON payload containing the text data to analyze. For example:
```json
{
  "text": "I love this product!"
}
