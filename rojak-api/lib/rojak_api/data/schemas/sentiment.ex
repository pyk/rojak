defmodule RojakAPI.Data.Schemas.Sentiment do
  use Ecto.Schema

  schema "sentiment" do
    field :name, :string

    # Relationship
    belongs_to :pairing, RojakAPI.Data.Schemas.PairOfCandidates
    has_many :news, RojakAPI.Data.Schemas.NewsSentiment

    timestamps()
  end

end
