defmodule RojakAPI.Data.Schemas.Media do
  use Ecto.Schema

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
    has_many :news, RojakAPI.Data.Schemas.News

    timestamps()
  end

end
