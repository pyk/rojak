defmodule RojakAPI.Data.Schemas.Sentiment do
  use Ecto.Schema

  schema "sentiment" do
    field :name, :string

    # Relationship
    belongs_to :pairing, RojakAPI.Data.Schemas.PairOfCandidates,
      foreign_key: :pair_of_candidates_id
    has_many :news, RojakAPI.Data.Schemas.NewsSentiment

    timestamps()
  end

end
