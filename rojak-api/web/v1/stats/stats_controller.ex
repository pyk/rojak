defmodule RojakAPI.V1.StatsController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Data.Stats

  @apidoc """
    @api {get} /stats Get Rojak statistics
    @apiGroup Stats
    @apiName Stats
    @apiDescription Get statistics of data in Rojak.

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
      {
        "media_count": 20,
        "total_news_count": 1000,
        "analyzed_news_count": 800,
        "total_sentiments_count": 2000,
        "positive_sentiments_count": 1000,
        "negative_sentiments_count": 700,
        "oot_sentiments_count": 300
      }
  """
  def index(conn, _params) do
    stats = Stats.get()
    json conn, stats
  end

end
