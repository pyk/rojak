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

  def fetch_sentiments(%{id: id}) do
    query = from p in PairOfCandidates,
      left_join: cagub in assoc(p, :cagub),
      left_join: cawagub in assoc(p, :cawagub),
      left_join: cagub_sentiments in fragment("""
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
        """), on: cagub_sentiments.candidate_id == p.cawagub_id and cagub_sentiments.media_id == ^id,
      left_join: cawagub_sentiments in fragment("""
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
        """), on: cawagub_sentiments.candidate_id == p.cawagub_id and cawagub_sentiments.media_id == ^id,
      select: %{
        pairing: %{p |
          sentiments: %{
            cagub: %{
              positive: cagub_sentiments.positive,
              neutral: cagub_sentiments.neutral,
              negative: cagub_sentiments.negative,
            },
            cawagub: %{
              positive: cawagub_sentiments.positive,
              neutral: cawagub_sentiments.neutral,
              negative: cawagub_sentiments.negative,
            },
          },
        },
        candidates: %{
          cagub: %{cagub |
            sentiments: %{
              positive: cagub_sentiments.positive,
              neutral: cagub_sentiments.neutral,
              negative: cagub_sentiments.negative,
            },
          },
          cawagub: %{cawagub |
            sentiments: %{
              positive: cawagub_sentiments.positive,
              neutral: cawagub_sentiments.neutral,
              negative: cawagub_sentiments.negative,
            },
          },
        },
      }

    query
    |> Repo.all
  end

end
