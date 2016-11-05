defmodule RojakAPI.V1.MediaController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Data.Media

  @apidoc """
    @api {get} /media Get Media
    @apiGroup Media
    @apiName GetMedia
    @apiVersion 1.0.0
    @apiParam {Integer} [offset=0] Skip over a number of elements by specifying an offset value for the query. </br></br> Example:
      <pre>?offset=20</pre>
    @apiParam {Integer} [limit=10] Limit the number of elements on the response. </br></br> Example:
      <pre>?limit=20</pre>
    @apiDescription Get a list of media.
    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
      [
        {
          "id": 1,
          "name": "detikcom",
          "website_url": "http://detik.com",
          "logo_url": "https://cdn.detik.net.id/detik2/images/logodetikcom.png?1",
          "fbpage_username": "detikcom",
          "twitter_username": "detikcom",
          "instagram_username": "detikcom",
          "inserted_at": 1341533193,
          "updated_at": 1341533193
        }
      ]
  """
  defparams media_index_params %{
    limit: [field: :integer, default: 10],
    offset: [field: :integer, default: 0],
  }

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &media_index_params/1
    media = Media.fetch(validated_params)
    render(conn, "index.json", media: media)
  end

  @apidoc """
    @api {get} /media/:mediaId Get a Media
    @apiGroup Media
    @apiName GetAMedia
    @apiVersion 1.0.0
    @apiParam {String} mediaId
    @apiDescription Get a media based on {mediaId}.
    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
      {
        "id": 1,
        "name": "detikcom",
        "website_url": "http://detik.com",
        "logo_url": "https://cdn.detik.net.id/detik2/images/logodetikcom.png?1",
        "fbpage_username": "detikcom",
        "twitter_username": "detikcom",
        "instagram_username": "detikcom",
        "inserted_at": 1341533193,
        "updated_at": 1341533193
      }
    @apiErrorExample {json} Item Not Found
      HTTP/1.1 404 Not Found
      {
        "message" : "item not found"
      }
  """
  defparams media_show_params %{
    id!: :integer,
  }

  def show(conn, params) do
    validated_params = ParamsValidator.validate params, &media_show_params/1
    media = Media.fetch_one(validated_params)
    render(conn, "show.json", media: media)
  end

  @apidoc """
    @api {get} /media/:mediaId/sentiments Get Media-Sentiments
    @apiGroup Media
    @apiName GetMediaSentiments
    @apiVersion 1.0.0
    @apiParam {String} mediaId
    @apiDescription Get a breakdown of sentiments for each pairing and candidate by this media.
    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
      [
        {
          "pairing": {
            "id": 3,
            "name": "Agus Sylvi",
            "cagub_id": 5,
            "cawagub_id": 6,
            "website_url": "http://relawanagussylvi.com",
            "logo_url": "https://pbs.twimg.com/profile_images/783564904460460032/VgVxZX-l.jpg",
            "fbpage_username": "RelawanAgusSylvi",
            "twitter_username": "RelAgusSylvi",
            "instagram_username": "",
            "slogan": "Jakarta Untuk Rakyat",
            "description": "",
            "inserted_at": 1341533193,
            "updated_at": 1341533193,
            "sentiments": {
              "positive": 0.41256,
              "negative": 0.12345,
              "neutral": 0.46399
            }
          },
          "candidates": {
            "cagub": {
              "id": 3,
              "full_name": "Agus Harimurti Yudhoyono",
              "alias_name": "Agus Yudhoyono",
              "place_of_birth": "Bandung, Jawa Barat",
              "date_of_birth": "1978-08-10",
              "religion": "Islam",
              "website_url": ""
              "photo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Mayor_Infanteri_Agus_Harimurti_Yudhoyono%2C_M.Sc.%2C_MPA.png",
              "fbpage_username": "",
              "twitter_username": "agusyudhoyono",
              "instagram_username": "agusyudhoyono",
              "inserted_at": 1341533193,
              "updated_at": 1341533193,
              "sentiments": {
                "positive": 0.41256,
                "negative": 0.12345,
                "neutral": 0.46399
              }
            },
            "cawagub": {
              "id": 4,
              "full_name": "Sylviana Murni",
              "alias_name": "Sylvi",
              "place_of_birth": "Jakarta",
              "date_of_birth": "1958-10-11",
              "religion": "Islam",
              "website_url": "http://sylvianamurni.com",
              "photo_url": "https://pbs.twimg.com/profile_images/781481260489125888/06iQrhGr.jpg",
              "fbpage_username": "sylviana_murni",
              "twitter_username": "sylviana_murni",
              "instagram_username": "sylvianamurni_",
              "inserted_at": 1341533193,
              "updated_at": 1341533193,
              "sentiments": {
                "positive": 0.41256,
                "negative": 0.12345,
                "neutral": 0.46399
              }
            }
          }
        }
      ]
  """
  defparams media_sentiments_params %{
    id!: :integer,
  }

  def sentiments(conn, params) do
    validated_params = ParamsValidator.validate params, &media_sentiments_params/1
    sentiments = Media.fetch_sentiments(validated_params)
    render(conn, "sentiments.json", sentiments: sentiments)
  end

end
