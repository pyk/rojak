defmodule RojakAPI.V1.MediaView do
  use RojakAPI.Web, :view

  def render("index.json", %{media: media}) do
    render_many(media, RojakAPI.V1.MediaView, "media.json")
  end

  def render("show.json", %{media: media}) do
    render_one(media, RojakAPI.V1.MediaView, "media.json")
  end

  def render("sentiments.json", %{sentiments: sentiments}) do
    render_many(sentiments, RojakAPI.V1.MediaView, "sentiment.json", as: :sentiment)
  end

  def render("media.json", %{media: media}) do
    Map.drop media, [:__meta__, :news, :sentiments]
  end

  def render("sentiment.json", %{sentiment: sentiment}) do
    %{sentiment |
      pairing: Map.drop(sentiment.pairing, [:__meta__, :cagub, :cawagub, :candidates]),
      candidates: %{sentiment.candidates |
        cagub: Map.drop(sentiment.candidates.cagub, [:__meta__, :mentioned_in]),
        cawagub: Map.drop(sentiment.candidates.cawagub, [:__meta__, :mentioned_in]),
      }
    }
  end
end
