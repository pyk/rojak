defmodule RojakAPI.V1.NewsController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Data.News

  @apidoc """
    @api {get} /news Get list of news
    @apiGroup News
    @apiName NewsList
    @apiDescription Get a list of news, optionally with <code>media</code>, <code>mentions</code>, and <code>sentiments</code>. Filterable by media and mentioned candidates.

    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>media</code>, <code>mentions</code>, <code>sentiments</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>
    @apiParam {Integer} [offset=0] Skip over a number of elements by specifying an offset value for the query. </br></br> Example:
      <pre>?offset=20</pre>
    @apiParam {Integer} [limit=10] Limit the number of elements on the response. </br></br> Example:
      <pre>?limit=20</pre>
    @apiParam {Integer} [media_id[]] Filter articles based on <code>id</code> of media. </br></br> Example:
      <pre>?media_id[]=1&media_id[]=2</pre>
    @apiParam {Integer} [candidate_id[]] Filter articles based on <code>id</code> of mentioned candidates. </br></br> Example:
      <pre>?candidate_id[]=1&candidate_id[]=2</pre>

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

          // embedded fields
          "media": {
            // media data
          },
          "mentions": [
            {
              // candidate data
            }
          ],
          "sentiments": [
            {
              pairing: {
                // pairing data
              },
              type: 'positive',
              confidentScore: 0.12345
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

          // embedded fields
          "media": {
            // media data
          },
          "mentions": [
            {
              // candidate data
            }
          ],
          "sentiments": [
            {
              pairing: {
                // pairing data
              },
              type: 'positive',
              confidentScore: 0.12345
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
      |> validate_subset(:embed, ["media", "mentions", "sentiments"])
    end
  end

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &news_index_params/1
    news = News.fetch(validated_params)
    render(conn, "index.json", news: news)
  end

  @apidoc """
    @api {get} /news/:newsId Get a single news
    @apiGroup News
    @apiName NewsSingle
    @apiDescription Get a news article based on {newsId}, optionally with <code>media</code>, <code>mentions</code>, and <code>sentiments</code>.

    @apiParam {String} newsId
    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>media</code>, <code>mentions</code>, <code>sentiments</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>

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

        // embedded fields
        "media": {
          // media data
        },
        "mentions": [
          {
            // candidate data
          }
        ],
        "sentiments": [
          {
            pairing: {
              // pairing data
            },
            type: 'positive',
            confidentScore: 0.12345
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
      |> validate_subset(:embed, ["media", "mentions", "sentiments"])
    end
  end

  def show(conn, params) do
    validated_params = ParamsValidator.validate params, &news_show_params/1
    news = News.fetch_one(validated_params)
    render(conn, "show.json", news: news)
  end

end
