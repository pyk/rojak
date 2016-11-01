defmodule RojakAPI.Media do
  use RojakAPI.Web, :model

  # Self-alias
  alias RojakAPI.Media

  schema "media" do
    field :name, :string
    field :website_url, :string
    field :logo_url, :string
    field :fbpage_username, :string
    field :twitter_username, :string
    field :instagram_username, :string

    # Virtual fields for embedding joins
    field :sentiments, :map, virtual: true

    # Relationship
    has_many :news, RojakAPI.News

    timestamps()
  end

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
    query = from p in RojakAPI.PairOfCandidates,
      join: cagub in assoc(p, :cagub),
      join: cawagub in assoc(p, :cawagub),
      join: cagub_sentiments in fragment("""
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
      join: cawagub_sentiments in fragment("""
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
