# Rojak API API documentation version v1
https://api.rojak.com/

---

## /pairings
Collection of available pairings.

### /pairings

* **get**: Get a list of pairings.

### /pairings/{pairingId}
Entity representing a pairing.

* **get**: Get the pairing
with pairingId =
{pairingId}.

### /pairings/{pairingId}/news

* **get**: Get list of news mentioning both or either of the candidates with their sentiments.

### /pairings/{pairingId}/sentiments

* **get**: Get the overall sentiments for these pairing.

### /pairings/{pairingId}/sentiments/media

* **get**: Get a breakdown of media with their sentiment for these candidates.

### /pairings/{pairingId}/sentiments/media/{mediaId}

* **get**: Get the sentiment by this media for these candidates.

### /pairings/{pairingId}/sentiments/media/{mediaId}/news

* **get**: Get a breakdown of sentiments from the news of this media.

## /candidates
Collection of available candidates.

### /candidates

* **get**: Get a list of candidates.

### /candidates/{candidateId}
Entity representing a candidate.

* **get**: Get the candidate
with candidateId =
{candidateId}.

### /candidates/{candidateId}/news

* **get**: Get list of news mentioning this candidate.

### /candidates/{candidateId}/sentiments

* **get**: Get the overall sentiments for this candidate.

### /candidates/{candidateId}/sentiments/media

* **get**: Get a breakdown of media with their sentiment for this candidate.

### /candidates/{candidateId}/sentiments/media/{mediaId}

* **get**: Get the sentiment by this media for this candidate.

### /candidates/{candidateId}/sentiments/media/{mediaId}/news

* **get**: Get a breakdown of sentiments from the news of this media.

## /news
Collection of available news.

### /news

* **get**: Get a list of news.

### /news/{newsId}
Entity representing a news.

* **get**: Get the news
with newsId =
{newsId}.

### /news/{newsId}/candidates

* **get**: Get list of candidates mentioned in this article.

### /news/{newsId}/sentiments

* **get**: Get the sentiments score of this article for each candidate.

## /media
Collection of available media.

### /media

* **get**: Get a list of media.

### /media/{mediaId}
Entity representing a media.

* **get**: Get the media
with mediaId =
{mediaId}.

### /media/{mediaId}/news

* **get**: Get list of news articles of this media.

### /media/{mediaId}/sentiments

* **get**: Get the sentiments score of this media for each candidate.

