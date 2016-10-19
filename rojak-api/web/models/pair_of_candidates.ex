defmodule RojakAPI.PairOfCandidates do
  use RojakAPI.Web, :model

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

    # Relationship
    has_one :cagub, RojakAPI.Candidate, foreign_key: :id, references: :cagub_id
    has_one :cawagub, RojakAPI.Candidate, foreign_key: :id,
      references: :cawagub_id

    timestamps()
  end

end
