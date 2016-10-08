defmodule RojakAPI.Sentiment do
  use RojakAPI.Web, :model

  schema "sentiment" do
    field :name, :string

    # Relationship
    belongs_to :candidate, RojakAPI.Candidate
    has_many :news, RojakAPI.NewsSentiment

    timestamps()
  end

  @doc """
  Builds a changeset based on the `struct` and `params`.
  """
  def changeset(struct, params \\ %{}) do
    struct
    |> cast(params, [:name])
    |> validate_required([:name])
  end
end
