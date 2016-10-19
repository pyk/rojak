defmodule RojakAPI.Media do
  use RojakAPI.Web, :model

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

end
