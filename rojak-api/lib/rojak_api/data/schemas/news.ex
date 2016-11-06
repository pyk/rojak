defmodule RojakAPI.Data.Schemas.News do
  use Ecto.Schema

  schema "news" do
    field :title, :string
    field :url, :string
    field :author_name, :string

    # Relationship
    belongs_to :media, RojakAPI.Data.Schemas.Media
    has_many :sentiments, RojakAPI.Data.Schemas.NewsSentiment
    many_to_many :mentions, RojakAPI.Data.Schemas.Candidate, join_through: "mention"

    timestamps()
  end

end
