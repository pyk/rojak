defmodule RojakAPI.PairOfCandidates do
  use RojakAPI.Web, :model

  schema "pair_of_candidates" do
    field :name, :string
    field :website_url, :string
    field :logo_url, :string
    field :fbpage_username, :string
    field :twitter_username, :string
    field :instagram_username, :string
    field :slogan, :string
    field :description, :string
    field :cagub_id, :integer
    field :cawagub_id, :integer

    # Relationship
    has_one :cagub, RojakAPI.Candidate, foreign_key: :id, references: :cagub_id
    has_one :cawagub, RojakAPI.Candidate, foreign_key: :id,
      references: :cawagub_id

    timestamps()
  end

  def fetch_embed(query, embed) do
    case embed do
      nil ->
        query
      _ ->
        query
        |> fetch_candidates(embed_by?(embed, "candidates"))
    end
  end

  defp fetch_candidates(query, should_embed?) do
    case should_embed? do
      false ->
        query
      true ->
        from q in query,
          join: cagub in assoc(q, :cagub),
          join: cawagub in assoc(q, :cawagub),
          preload: [cagub: cagub, cawagub: cawagub]
    end
  end

  defp embed_by?(embed, key) do
    Enum.member?(embed, key)
  end

end
