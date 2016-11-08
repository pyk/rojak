defmodule RojakAPI.V1.MediaController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Data.Media

  @apidoc """
    @api {get} /media Get list of media
    @apiGroup Media
    @apiName MediaList
    @apiDescription Get a list of media.

    @apiParam {Integer} [offset=0] Skip over a number of elements by specifying an offset value for the query. </br></br> Example:
      <pre>?offset=20</pre>
    @apiParam {Integer} [limit=10] Limit the number of elements on the response. </br></br> Example:
      <pre>?limit=20</pre>

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
    @api {get} /media/:mediaId Get a single media
    @apiGroup Media
    @apiName MediaSingle
    @apiDescription Get a media based on {mediaId}, optionally with <code>latest_news</code> and <code>sentiments_on_pairings</code>.

    @apiParam {String} mediaId
    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>latest_news</code>, <code>sentiments_on_pairings</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>

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
        "updated_at": 1341533193,

        // embedded fields
        "latest_news": [
          {
            // news data
          }
        ],
        "sentiments_on_pairings": [
          {
            "pairing": {
              // pairing data
            },
            "positive_news_count": 123,
            "negative_news_count": 123
          }
        ]
      }
    @apiErrorExample {json} Item Not Found
      HTTP/1.1 404 Not Found
      {
        "message" : "item not found"
      }
  """
  defparams media_show_params(%{
    id!: :integer,
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:id, :embed])
      |> validate_subset(:embed, ["latest_news", "sentiments_on_pairings"])
    end
  end

  def show(conn, params) do
    validated_params = ParamsValidator.validate params, &media_show_params/1
    media = Media.fetch_one(validated_params)
    render(conn, "show.json", media: media)
  end

end
