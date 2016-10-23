defmodule RojakAPI.Candidate do
  use RojakAPI.Web, :model

  # Self alias
  alias RojakAPI.Candidate

  schema "candidate" do
    field :full_name, :string
    field :alias_name, :string
    field :place_of_birth, :string
    field :date_of_birth, Ecto.Date
    field :religion, :string
    field :website_url, :string
    field :photo_url, :string
    field :fbpage_username, :string
    field :instagram_username, :string
    field :twitter_username, :string

    # Virtual fields for embedding joins
    field :pairing, :map, virtual: true

    # Relationship
    has_many :sentiments, RojakAPI.Sentiment
    many_to_many :mentioned_in, RojakAPI.News, join_through: "mention"

    timestamps()
  end

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

  defp fetch_embed(query, embed) when is_nil(embed), do: query
  defp fetch_embed(query, embed) do
    query
    |> fetch_pairing(Enum.member?(embed, "pairing"))
  end

  defp fetch_pairing(query, embed?) when not embed?, do: query
  defp fetch_pairing(query, _) do
    from q in query,
      join: p in RojakAPI.PairOfCandidates, on: q.id == p.cagub_id or q.id == p.cawagub_id,
      select: %{q | pairing: p}
  end

end
