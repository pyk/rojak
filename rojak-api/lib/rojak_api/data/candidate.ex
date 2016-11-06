defmodule RojakAPI.Data.Candidate do
  import Ecto.Query

  alias RojakAPI.Repo
  alias RojakAPI.Data.Schemas.{
    Candidate,
    Media,
    PairOfCandidates
  }

  def fetch(%{embed: embed}) do
    Candidate
    |> fetch_embed(embed)
    |> Repo.all
  end

  def fetch_one(%{id: id, embed: embed}) do
    Candidate
    |> fetch_embed(embed)
    |> Repo.get!(id)
  end

  def fetch_media_sentiments(%{id: id, limit: limit, offset: offset}) do
    query = from m in Media,
      left_join: s in fragment("""
        SELECT
          s.candidate_id,
          n.media_id,
          COUNT(CASE WHEN s.name like 'pro%' THEN 1 END) positive,
          COUNT(CASE WHEN s.name like 'net%' THEN 1 END) neutral,
          COUNT(CASE WHEN s.name like 'con%' THEN 1 END) negative
        FROM news_sentiment ns
        JOIN news n ON ns.news_id = n.id
        JOIN sentiment s ON ns.sentiment_id = s.id
        GROUP BY s.candidate_id, n.media_id
        """), on: s.media_id == m.id and s.candidate_id == ^id,
      limit: ^limit,
      offset: ^offset,
      select: %{m |
        sentiments: %{
          positive: s.positive,
          neutral: s.neutral,
          negative: s.negative,
        }
      }

    query
    |> Repo.all
  end

  defp fetch_embed(query, embed) when is_nil(embed), do: query
  defp fetch_embed(query, embed) do
    query
    |> fetch_pairing(Enum.member?(embed, "pairing"))
    |> fetch_sentiments(Enum.member?(embed, "sentiments"))
    |> select_embed_fields(embed)
  end

  defp select_embed_fields(query, embed) do
    case [Enum.member?(embed, "pairing"), Enum.member?(embed, "sentiments")] do
      [true, true] ->
        from [q, p, s] in query,
          select: %{q |
            pairing: p,
            sentiments: %{
              positive: s.positive,
              neutral: s.neutral,
              negative: s.negative,
            }
          }
      [true, _] ->
        from [q, p] in query,
          select: %{q | pairing: p}
      [_, true] ->
        from [q, s] in query,
          select: %{q |
            sentiments: %{
              positive: s.positive,
              neutral: s.neutral,
              negative: s.negative,
            }
          }
      _ -> query
    end
  end

  defp fetch_pairing(query, embed?) when not embed?, do: query
  defp fetch_pairing(query, _) do
    from q in query,
      join: p in PairOfCandidates, on: q.id == p.cagub_id or q.id == p.cawagub_id
  end

  defp fetch_sentiments(query, embed?) when not embed?, do: query
  defp fetch_sentiments(query, _) do
    from q in query,
      left_join: s in fragment("""
        SELECT
          s.candidate_id,
          COUNT(CASE WHEN s.name like 'pro%' THEN 1 END) positive,
          COUNT(CASE WHEN s.name like 'net%' THEN 1 END) neutral,
          COUNT(CASE WHEN s.name like 'con%' THEN 1 END) negative
        FROM news_sentiment ns
        JOIN sentiment s ON ns.sentiment_id = s.id
        GROUP BY s.candidate_id
        """), on: s.candidate_id == q.id
  end

end
