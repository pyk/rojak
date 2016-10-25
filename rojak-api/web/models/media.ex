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

end
