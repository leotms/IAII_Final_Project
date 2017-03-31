# Identifying Demand and Offer of Medicines in Twitter.

## Abstract

The crisis of medicines in Venezuela has led people to use Twitter as a tool for searching and offering medicines. This study seeks to facilitate the search of medications on Twitter using an Artificial Intelligence algorithm under supervised learning. A neural network was trained with traing and testing sets of 6000 tuits manually classified and pre-processed according to characteristics that gave better experimental results in the classification. As a result, the best neuronal network obtained was capable to identify tweets with 84% accuracy and 92% recall for supply tics, 87% for demand and
74% for other tweets. The implementation and training of a neural network for automatic identification of tweets can be of important help for medicines localization in Venezuela.

Futher results can be found in the final report (in spanish) under the `docs/` folder in this repository.

## Requirements:
  - Python 3.x
  - Numpy
  - Pandas
  - Tweetpy

## Setting Up

  Before running this project it is necessary to complete the `consumer_key,
consumer_secret, access_token, access_secret` variables in the `config.py` file with yout own Twitter Application Acces Tokens.

## Running:

  ```bash
  $ python medicines.py <SearchTerm>
  ```
  Will load and use the best neural network and connect to Twitter via Tweetpy for tracking all tweets containing <SearchTerm>

  A recommended search term for testing is `ServicioPublico`. A hashtag commonly used for seaching and offering medicines in twitter.

## Disclaimer

  This study was conducted with academic purposes only. There are no intentions from neither of the authors to perform activities related to storage, sale, or distribution of medicines.

## Other:
  - All training sets used (0 to 9) with their respectively test sets are located in the `docs` folder.
  - Raw data and other files collected using Birdwatcher are stored in the `twitter` folder.
  - Results for best training set using crossvalidation are stored in the `results/` folder.
  - Futher results can be found in the final report (in spanish) under the `docs/` folder in this repository.


## Authors:
- [Leonardo Martínez](https://github.com/leotms)
- [Nicolás Mañan](https://github.com/nmanan)
- [Joel Rivas](https://github.com/JoelRg)

### Last Updated: 03/30/2017
