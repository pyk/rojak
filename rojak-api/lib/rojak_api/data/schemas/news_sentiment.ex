defmodule RojakAPI.Data.Schemas.NewsSentiment do
  use Ecto.Schema

  schema "news_sentiment" do
    field :score, :float

    # Relationship
    belongs_to :news, RojakAPI.Data.Schemas.News
    belongs_to :sentiment, RojakAPI.Data.Schemas.Sentiment

    timestamps()
  end

end
