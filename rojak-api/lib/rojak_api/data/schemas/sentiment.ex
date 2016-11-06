defmodule RojakAPI.Data.Schemas.Sentiment do
  use Ecto.Schema

  schema "sentiment" do
    field :name, :string

    # Relationship
    belongs_to :candidate, RojakAPI.Data.Schemas.Candidate
    has_many :news, RojakAPI.Data.Schemas.NewsSentiment

    timestamps()
  end

end
