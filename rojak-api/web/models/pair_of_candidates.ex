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

  @doc """
  Builds a changeset based on the `struct` and `params`.
  """
  def changeset(struct, params \\ %{}) do
    struct
    |> cast(params, [:name, :website_url, :logo_url,
          :fbpage_username, :twitter_username, :instagram_username,
          :slogan, :description])
    |> validate_required([:name])
    # TODO: add :cagub and :cawagub as required ans pass the test
    # TODO: add unique constraint for name, website_url etc
  end
end
