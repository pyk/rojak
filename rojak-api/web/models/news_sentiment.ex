defmodule RojakAPI.NewsSentiment do
  use RojakAPI.Web, :model

  schema "news_sentiment" do
    field :score, :float

    # Relationship
    belongs_to :news, RojakAPI.News
    belongs_to :sentiment, RojakAPI.Sentiment

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
