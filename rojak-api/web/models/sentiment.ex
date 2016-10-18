defmodule RojakAPI.Sentiment do
  use RojakAPI.Web, :model

  schema "sentiment" do
    field :name, :string

    # Relationship
    belongs_to :candidate, RojakAPI.Candidate
    has_many :news, RojakAPI.NewsSentiment

    timestamps()
  end

end
