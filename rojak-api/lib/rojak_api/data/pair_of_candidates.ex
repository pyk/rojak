defmodule RojakAPI.Data.PairOfCandidates do
  import Ecto.Query

  alias RojakAPI.Repo
  alias RojakAPI.Data.Schemas.{
    PairOfCandidates,
    Media
  }

  def fetch(%{embed: embed}) do
    PairOfCandidates
    |> fetch_embed(embed)
    |> Repo.all
  end

  def fetch_one(%{id: id, embed: embed}) do
    PairOfCandidates
    |> fetch_embed(embed)
    |> Repo.get!(id)
    |> fetch_embed_after(embed)
  end

  defp fetch_embed(query, embed) when is_nil(embed), do: query
  defp fetch_embed(query, embed) do
    query
    |> fetch_candidates(Enum.member?(embed, "candidates"))
    |> fetch_sentiments(Enum.member?(embed, "overall_sentiments"))
    |> select_embed_fields(embed)
  end

  defp select_embed_fields(query, embed) do
    case [Enum.member?(embed, "candidates"), Enum.member?(embed, "overall_sentiments")] do
      [true, true] ->
        from [q, cagub, cawagub, s] in query,
          select: %{q |
            candidates: %{cagub: cagub, cawagub: cawagub},
            overall_sentiments: %{
              positive_news_count: s.positive,
              negative_news_count: s.negative
            }
          }
      [true, _] ->
        from [q, cagub, cawagub] in query,
          select: %{q | candidates: %{cagub: cagub, cawagub: cawagub}}
      [_, true] ->
        from [q, s] in query,
          select: %{q |
            overall_sentiments: %{
              positive_news_count: s.positive,
              negative_news_count: s.negative
            }
          }
      _ ->
        query
    end
  end

  defp fetch_candidates(query, embed?) when not embed?, do: query
  defp fetch_candidates(query, _) do
    from q in query,
      left_join: cagub in assoc(q, :cagub),
      left_join: cawagub in assoc(q, :cawagub)
  end

  defp fetch_sentiments(query, embed?) when not embed?, do: query
  defp fetch_sentiments(query, _) do
    from q in query,
      left_join: s in fragment("""
        SELECT
          s.pair_of_candidates_id,
          COUNT(CASE WHEN s.name like 'pos%' THEN 1 END) positive,
          COUNT(CASE WHEN s.name like 'neg%' THEN 1 END) negative
        FROM news_sentiment ns
        JOIN sentiment s ON ns.sentiment_id = s.id
        GROUP BY s.pair_of_candidates_id
        """), on: s.pair_of_candidates_id == q.id
  end

  defp fetch_embed_after(struct, embed) when is_nil(embed), do: struct
  defp fetch_embed_after(struct, embed) do
    struct
    |> fetch_media_sentiments(Enum.member?(embed, "sentiments_by_media"))
  end

  defp fetch_media_sentiments(struct, embed?) when not embed?, do: struct
  defp fetch_media_sentiments(struct, _) do
    query = from m in Media,
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
        """), on: s.media_id == m.id and s.pair_of_candidates_id == ^struct.id,
      select: %{
        media: m,
        positive_news_count: s.positive,
        negative_news_count: s.negative
      }
    result = query |> Repo.all
    struct
    |> Map.put(:sentiments_by_media, result)
  end

end
