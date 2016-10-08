defmodule RojakAPI.News do
  use RojakAPI.Web, :model

  alias RojakAPI.Media
  alias RojakAPI.Sentiment
  alias RojakAPI.NewsSentiment
  alias RojakAPI.Candidate

  schema "news" do
    field :title, :string
    field :content, :string
    field :url, :string

    # Relationship
    belongs_to :media, Media
    has_many :sentiments, NewsSentiment
    many_to_many :mentions, Candidate, join_through: "mention"

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
