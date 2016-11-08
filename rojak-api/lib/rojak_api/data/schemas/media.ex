defmodule RojakAPI.Data.Schemas.Media do
  use Ecto.Schema

  schema "media" do
    field :name, :string
    field :website_url, :string
    field :logo_url, :string
    field :fbpage_username, :string
    field :twitter_username, :string
    field :instagram_username, :string

    # Relationship
    has_many :latest_news, RojakAPI.Data.Schemas.News,
      foreign_key: :media_id

    timestamps()
  end

end
