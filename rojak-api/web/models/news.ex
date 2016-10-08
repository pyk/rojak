defmodule RojakAPI.News do
  use RojakAPI.Web, :model

  schema "news" do
    field :title, :string
    field :content, :string
    field :url, :string

    # Relationship
    belongs_to :media, RojakAPI.Media
    has_many :sentiments, RojakAPI.NewsSentiment
    many_to_many :mentions, RojakAPI.Candidate, join_through: "mention"

    timestamps()
  end

  @doc """
  Builds a changeset based on the `struct` and `params`.
  """
  def changeset(struct, params \\ %{}) do
    struct
    |> cast(params, [:title, :content, :url, :media_id])
    |> validate_required([:title, :content, :url, :media_id])
  end
end
