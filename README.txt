Authors:     Leonardo Martinez #11-10576
             Nicolas Manan     #06-39883
             Joel Rivas        #11-10866
Updated:     03/30/2017

## Requirements:
  - Python 3.x
  - Numpy
  - Pandas
  - Tweetpy

## Setting Up

Before running this project it is necessary to complete the `consumer_key,
consumer_secret, access_token, access_secret` variables in the `config.py` file with yout own Twitter Application Acces Tokens.

There are already configured API keys provided in config.py for testing.

## Running:

  $ python medicines.py <SearchTerm>

  Will load and use the best neural network and connect to Twitter via Tweetpy for tracking all tweets containing <SearchTerm>
  A recommended search term for testing is `ServicioPublico`. A hashtag commonly used for seaching and offering medicines in twitter.

## Other:
  - All training sets used (0 to 9) with their respectively test sets are located in the `docs` folder.
  - Raw data and other files collected using Birdwatcher are stored in the `twitter` folder.
  - Results for best training set using crossvalidation are stored in the `results/` folder.
  - Futher results can be found in the final report under the `docs/` folder in this repository.
