defmodule RojakAPI.Data.Media do
  import Ecto.Query

  alias RojakAPI.Repo
  alias RojakAPI.Data.Schemas.{
    Media,
    PairOfCandidates,
    News
  }

  def fetch(%{limit: limit, offset: offset}) do
    query = from Media, limit: ^limit, offset: ^offset
    query
    |> Repo.all
  end

  def fetch_one(%{id: id, embed: embed}) do
    Media
    |> fetch_embed(embed)
    |> Repo.get!(id)
    |> fetch_embed_after(embed)
  end

  defp fetch_embed(query, embed) when is_nil(embed), do: query
  defp fetch_embed(query, embed) do
    query
    |> fetch_latest_news(Enum.member?(embed, "latest_news"))
    # |> fetch_sentiments(Enum.member?(embed, "sentiments_on_pairings"))
  end

  defp fetch_latest_news(query, embed?) when not embed?, do: query
  defp fetch_latest_news(query, _) do
    latest_news = from n in News,
      limit: 5,
      order_by: [desc: n.id]
    from q in query,
      preload: [latest_news: ^latest_news]
  end

  defp fetch_embed_after(struct, embed) when is_nil(embed), do: struct
  defp fetch_embed_after(struct, embed) do
    struct
    |> fetch_media_sentiments(Enum.member?(embed, "sentiments_on_pairings"))
  end

  defp fetch_media_sentiments(struct, embed?) when not embed?, do: struct
  defp fetch_media_sentiments(struct, _) do
    query = from p in PairOfCandidates,
      left_join: s in fragment("""
        SELECT
          s.pair_of_candidates_id,
          n.media_id,
          COUNT(CASE WHEN s.name like 'pos%' THEN 1 END) positive,
          COUNT(CASE WHEN s.name like 'neg%' THEN 1 END) negative
        FROM news_sentiment ns
        JOIN news n ON ns.news_id = n.id
        JOIN sentiment s ON ns.sentiment_id = s.id
        GROUP BY s.pair_of_candidates_id, n.media_id
        """), on: s.pair_of_candidates_id == p.id and s.media_id == ^struct.id,
      select: %{
        pairing: p,
        positive_news_count: s.positive,
        negative_news_count: s.negative
      }
    result = query |> Repo.all
    struct
    |> Map.put(:sentiments_on_pairings, result)
  end

end
