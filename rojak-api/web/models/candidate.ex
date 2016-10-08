defmodule RojakAPI.Candidate do
  use RojakAPI.Web, :model

  schema "candidate" do
    field :full_name, :string
    field :alias_name, :string
    field :place_of_birth, :string
    field :date_of_birth, Ecto.Date
    field :religion, :string
    field :website_url, :string
    field :photo_url, :string
    field :fbpage_username, :string
    field :instagram_username, :string
    field :twitter_username, :string

    # Relationship
    has_many :sentiments, RojakAPI.Sentiment
    many_to_many :mentioned_in, RojakAPI.News, join_through: "mention"

    timestamps()
  end

  @doc """
  Builds a changeset based on the `struct` and `params`.
  """
  def changeset(struct, params \\ %{}) do
    struct
    |> cast(params, [:full_name, :alias_name, :place_of_birth,
        :date_of_birth, :religion, :website_url, :photo_url,
        :fbpage_username, :instagram_username, :twitter_username])
    |> validate_required([:full_name, :alias_name, :place_of_birth,
        :date_of_birth, :religion])
    # TODO: add unique constraint for full_name, alias_name, etc
  end
end
