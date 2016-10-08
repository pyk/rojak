defmodule RojakAPI.Sentiment do
  use RojakAPI.Web, :model

  alias RojakAPI.NewsSentiment
  alias RojakAPI.Candidate

  schema "sentiment" do
    field :name, :string

    # Relationship
    belongs_to :candidate, Candidate
    has_many :news, NewsSentiment

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
