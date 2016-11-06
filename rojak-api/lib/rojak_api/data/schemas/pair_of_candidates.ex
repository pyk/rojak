defmodule RojakAPI.Data.Schemas.PairOfCandidates do
  use Ecto.Schema

  schema "pair_of_candidates" do
    field :name, :string
    field :website_url, :string
    field :logo_url, :string
    field :fbpage_username, :string
    field :twitter_username, :string
    field :instagram_username, :string
    field :slogan, :string
    field :description, :string
    field :cagub_id, :integer
    field :cawagub_id, :integer

    # Virtual fields for embedding joins
    field :candidates, :map, virtual: true
    field :sentiments, :map, virtual: true

    # Relationship
    has_one :cagub, RojakAPI.Data.Schemas.Candidate, foreign_key: :id, references: :cagub_id
    has_one :cawagub, RojakAPI.Data.Schemas.Candidate, foreign_key: :id,
      references: :cawagub_id

    timestamps()
  end

end
