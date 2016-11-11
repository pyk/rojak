defmodule RojakAPI.V1.NewsView do
  use RojakAPI.Web, :view

  def render("index.json", %{news: news}) do
    render_many(news, RojakAPI.V1.NewsView, "news.json")
  end

  def render("show.json", %{news: news}) do
    render_one(news, RojakAPI.V1.NewsView, "news.json")
  end

  def render("news.json", %{news: news}) do
    news =
      news
      |> Map.drop([:__meta__, :is_analyzed])

    # Embed media
    news = case Map.get(news, :media) do
      %Ecto.Association.NotLoaded{} ->
        news
        |> Map.drop([:media])
      _ ->
        news
        |> Map.update!(:media, fn media ->
          Map.drop media, [:__meta__, :latest_news]
        end)
    end

    # Embed mentions
    news = case Map.get(news, :mentions) do
      %Ecto.Association.NotLoaded{} ->
        news
        |> Map.drop([:mentions])
      _ ->
        news
        |> Map.update!(:mentions, fn mentions ->
          Enum.map mentions, fn candidate ->
            Map.drop candidate, [:__meta__, :pairing]
          end
        end)
    end

    sentiments = Map.get(news, :sentiments)

    news =
      news
      |> Map.drop([:sentiments])

    # Embed mentions
    news = case sentiments do
      %Ecto.Association.NotLoaded{} ->
        news
      _ ->
        sentiments =
          Enum.map sentiments, fn news_sentiment ->
            pairing =
              news_sentiment
              |> Map.get(:sentiment)
              |> Map.get(:pairing)
            pairing = case pairing do
              nil ->
                pairing
              _ ->
                pairing
                |> Map.drop([:__meta__, :cagub, :cawagub, :candidates, :overall_sentiments])
            end
            sentiment_name =
              news_sentiment
              |> Map.get(:sentiment)
              |> Map.get(:name)
            sentiment_type = case sentiment_name do
              "pos" <> _ -> "positive"
              "neg" <> _ -> "negative"
              "oot" <> _ -> "oot"
            end
            confident_score =
              news_sentiment
              |> Map.get(:confident_score_scaled)
            %{
              pairing: pairing,
              type: sentiment_type,
              confident_score: confident_score
            }
          end

        Map.put news, :sentiments, sentiments
    end

    news
  end
end
