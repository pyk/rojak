defmodule RojakAPI.V1.NewsController do
  use RojakAPI.Web, :controller

  alias RojakAPI.News

  @apidoc """
    @api {get} /news Get News
    @apiGroup News
    @apiName GetNews
    @apiVersion 1.0.0
    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>mentions</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>
    @apiParam {Integer} [offset=0] Skip over a number of elements by specifying an offset value for the query. </br></br> Example:
      <pre>?offset=20</pre>
    @apiParam {Integer} [limit=10] Limit the number of elements on the response. </br></br> Example:
      <pre>?limit=20</pre>
    @apiParam {Integer} [media_id[]] Filter articles based on <code>id</code> of media. </br></br> Example:
      <pre>?media_id[]=1&media_id[]=2</pre>
    @apiParam {Integer} [candidate_id[]] Filter articles based on <code>id</code> of mentioned candidates. </br></br> Example:
      <pre>?candidate_id[]=1&candidate_id[]=2</pre>
    @apiDescription Get a list of news, optionally with mentioned candidates. Filterable by media and mentioned candidates.
    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
      [
        {
          "id": 1,
          "media_id": 3,
          "title": "Kunjungan Presiden Jokowi ke Depok",
          "url": "https://rojaktv.com/jokowi-jalan-jalan-ke-depok",
          "author_name": "Anto",
          "inserted_at": 1341533193,
          "updated_at": 1341533193,
          "mentions":
          [
            {
              "id": 1,
              "full_name": "Basuki Tjahaja Purnama",
              "alias_name": "Ahok",
              "place_of_birth": "Manggar, Belitung Timur",
              "date_of_birth": "1966-06-29",
              "religion": "Kristen Protestan",
              "website_url": "http://ahok.org",
              "photo_url": "https://upload.wikimedia.org/wikipedia/id/7/7a/Gubernur_DKI_Basuki.jpg",
              "fbpage_username": "AhokBTP",
              "twitter_username": "basuki_btp",
              "instagram_username": "basukibtp",
              "inserted_at": 1341533193,
              "updated_at": 1341533193,
              "sentiment": {
                "type": "positive",
                "score": 0.123,
              }
            }
          ]
        },
        {
          "id": 2,
          "media_id": 3,
          "title": "Budi Berpasangan dengan Ani",
          "url": "https://rojaktv.com/budi-berpasangan-ani",
          "author_name": "Anto",
          "inserted_at": 1341533201,
          "updated_at": 1341533201,
          "sentiments": [
            {
              "id": 1,
              "full_name": "Basuki Tjahaja Purnama",
              "alias_name": "Ahok",
              "place_of_birth": "Manggar, Belitung Timur",
              "date_of_birth": "1966-06-29",
              "religion": "Kristen Protestan",
              "website_url": "http://ahok.org",
              "photo_url": "https://upload.wikimedia.org/wikipedia/id/7/7a/Gubernur_DKI_Basuki.jpg",
              "fbpage_username": "AhokBTP",
              "twitter_username": "basuki_btp",
              "instagram_username": "basukibtp",
              "inserted_at": 1341533193,
              "updated_at": 1341533193,
              "sentiment": {
                "type": "positive",
                "score": 0.123,
              }
            }
          ]
        }
      ]
  """
  defparams news_index_params(%{
    limit: [field: :integer, default: 10],
    offset: [field: :integer, default: 0],
    embed: [:string],
    media_id: [:integer],
    candidate_id: [:integer]
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:limit, :offset, :embed, :media_id, :candidate_id])
      |> validate_subset(:embed, ["sentiments"])
    end
  end

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &news_index_params/1
    news = News.fetch(validated_params)
    render(conn, "index.json", news: news)
  end

  @apidoc """
    @api {get} /news/:newsId Get a News
    @apiGroup News
    @apiName GetANews
    @apiVersion 1.0.0
    @apiParam {String} newsId
    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>sentiments</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>
    @apiDescription Get a news article based on {newsId}, optionally with mentioned candidates.
    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
      {
        "id": 1,
        "mediaId": 3,
        "title": "Kunjungan Presiden Jokowi ke Depok",
        "url": "https://rojaktv.com/jokowi-jalan-jalan-ke-depok",
        "author_name": "Anto",
        "inserted_at": 1341533193,
        "updated_at": 1341533193,
        "sentiments": [
          {
            "id": 1,
            "full_name": "Basuki Tjahaja Purnama",
            "alias_name": "Ahok",
            "place_of_birth": "Manggar, Belitung Timur",
            "date_of_birth": "1966-06-29",
            "religion": "Kristen Protestan",
            "website_url": "http://ahok.org",
            "photo_url": "https://upload.wikimedia.org/wikipedia/id/7/7a/Gubernur_DKI_Basuki.jpg",
            "fbpage_username": "AhokBTP",
            "twitter_username": "basuki_btp",
            "instagram_username": "basukibtp",
            "inserted_at": 1341533193,
            "updated_at": 1341533193,
            "sentiment": {
              "type": "positive",
              "score": 0.123,
            }
          }
        ]
      }
    @apiErrorExample {json} Item Not Found
      HTTP/1.1 404 Not Found
      {
        "message" : "item not found"
      }
  """
  defparams news_show_params(%{
    id!: :integer,
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:id, :embed])
      |> validate_subset(:embed, ["sentiments"])
    end
  end

  def show(conn, params) do
    validated_params = ParamsValidator.validate params, &news_show_params/1
    news = News.fetch_one(validated_params)
    render(conn, "show.json", news: news)
  end

end
