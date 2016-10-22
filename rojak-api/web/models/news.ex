defmodule RojakAPI.News do
  use RojakAPI.Web, :model

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

end
