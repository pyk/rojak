defmodule RojakAPI.NewsSentiment do
  use RojakAPI.Web, :model

  alias RojakAPI.News
  alias RojakAPI.Sentiment

  alias RojakAPI.Sentiment
  schema "news_sentiment" do
    field :score, :float

    # Relationship
    belongs_to :news, News
    belongs_to :sentiment, Sentiment

    timestamps()
  end

  @doc """
  Builds a changeset based on the `struct` and `params`.
  """
  def changeset(struct, params \\ %{}) do
    struct
    |> cast(params, [:news_id, :sentiment_id, :score])
    |> validate_required([:news_id, :sentiment_id])
  end
end
