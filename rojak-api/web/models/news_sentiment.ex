defmodule RojakAPI.NewsSentiment do
  use RojakAPI.Web, :model

  schema "news_sentiment" do
    field :score, :float

    # Relationship
    belongs_to :news, RojakAPI.News
    belongs_to :sentiment, RojakAPI.Sentiment

    timestamps()
  end

end
