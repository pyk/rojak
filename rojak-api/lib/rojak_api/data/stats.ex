defmodule RojakAPI.Data.Stats do
  import Ecto.Query

  alias RojakAPI.Repo
  alias RojakAPI.Data.Schemas.{
    Media,
    News,
    NewsSentiment
  }

  def get do
    media_count = Repo.aggregate(Media, :count, :id)
    news_count = Repo.aggregate(News, :count, :id)
    sentiments_query =
      from ns in NewsSentiment,
        left_join: s in assoc(ns, :sentiment),
        select: %{
          total: fragment("COUNT(1) AS total"),
          positive: fragment("COUNT(CASE WHEN ? like 'pos%' THEN 1 END) AS positive", field(s, :name)),
          negative: fragment("COUNT(CASE WHEN ? like 'neg%' THEN 1 END) AS negative", field(s, :name)),
          oot: fragment("COUNT(CASE WHEN ? like 'oot%' THEN 1 END) AS oot", field(s, :name))
        }
    sentiments_count = sentiments_query |> Repo.one
    %{
      total_sentiments_count: sentiments_count.total,
      positive_sentiments_count: sentiments_count.positive,
      negative_sentiments_count: sentiments_count.negative,
      oot_sentiments_count: sentiments_count.oot,
      media_count: media_count,
      news_count: news_count
    }
  end

end
