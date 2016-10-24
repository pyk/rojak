defmodule RojakAPI.News do
  use RojakAPI.Web, :model

  # Self-alias
  alias RojakAPI.News

  schema "news" do
    field :title, :string
    field :url, :string
    field :author_name, :string

    # Relationship
    belongs_to :media, RojakAPI.Media
    has_many :sentiments, RojakAPI.NewsSentiment
    many_to_many :mentions, RojakAPI.Candidate, join_through: "mention"

    timestamps()
  end

  def fetch(%{limit: limit, offset: offset, embed: embed, media_id: media_id, candidate_id: candidate_id}) do
    query = from n in News,
      limit: ^limit,
      offset: ^offset,
      order_by: [desc: n.id]
    query
    |> filter_by_media(media_id)
    |> Repo.all
  end

  def fetch_one(%{id: id, embed: embed}) do
    News
    |> Repo.get!(id)
  end

  defp filter_by_media(query, media_ids) when is_nil(media_ids), do: query
  defp filter_by_media(query, media_ids) do
    from q in query,
      where: q.media_id in ^media_ids
  end

end
