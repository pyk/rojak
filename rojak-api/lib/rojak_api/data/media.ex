defmodule RojakAPI.Data.Media do
  import Ecto.Query

  alias RojakAPI.Repo
  alias RojakAPI.Data.Schemas.{
    Media,
    PairOfCandidates
  }

  def fetch(%{limit: limit, offset: offset}) do
    query = from Media, limit: ^limit, offset: ^offset
    query
    |> Repo.all
  end

  def fetch_one(%{id: id}) do
    Media
    |> Repo.get!(id)
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
