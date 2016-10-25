defmodule RojakAPI.PairOfCandidates do
  use RojakAPI.Web, :model

  # Self alias
  alias RojakAPI.PairOfCandidates

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

    # Virtual fields for embedding joins
    field :candidates, :map, virtual: true

    # Relationship
    has_one :cagub, RojakAPI.Candidate, foreign_key: :id, references: :cagub_id
    has_one :cawagub, RojakAPI.Candidate, foreign_key: :id,
      references: :cawagub_id

    timestamps()
  end

  def fetch(%{embed: embed}) do
    PairOfCandidates
    |> fetch_embed(embed)
    |> Repo.all
  end

  def fetch_one(%{id: id, embed: embed}) do
    PairOfCandidates
    |> fetch_embed(embed)
    |> Repo.get!(id)
  end

  defp fetch_embed(query, embed) when is_nil(embed), do: query
  defp fetch_embed(query, embed) do
    query
    |> fetch_candidates(Enum.member?(embed, "candidates"))
  end

  defp fetch_candidates(query, embed?) when not embed?, do: query
  defp fetch_candidates(query, _) do
    from q in query,
      join: cagub in assoc(q, :cagub),
      join: cawagub in assoc(q, :cawagub),
      select: %{q | candidates: %{cagub: cagub, cawagub: cawagub}}
  end

end
