defmodule RojakAPI.V1.CandidateView do
  use RojakAPI.Web, :view

  def render("index.json", %{candidates: candidates}) do
    render_many(candidates, RojakAPI.V1.CandidateView, "candidate.json")
  end

  def render("show.json", %{candidate: candidate}) do
    render_one(candidate, RojakAPI.V1.CandidateView, "candidate.json")
  end

  def render("media_sentiments.json", %{media_sentiments: media_sentiments}) do
    render_many(media_sentiments, RojakAPI.V1.CandidateView, "media_sentiment.json", as: :media_sentiment)
  end

  def render("candidate.json", %{candidate: candidate}) do
    candidate =
      candidate
      |> Map.drop([:__meta__, :mentioned_in])

    # Embed pairing
    candidate = case Map.get(candidate, :pairing) do
      nil ->
        candidate |> Map.drop([:pairing])
      pairing ->
        Map.update! candidate, :pairing, fn _ ->
          Map.drop(pairing, [:__meta__, :cagub, :cawagub])
        end
    end

    # Embed sentiments
    candidate = case Map.get(candidate, :sentiments) do
      nil ->
        candidate |> Map.drop([:sentiments])
      sentiments ->
        Map.update! candidate, :sentiments, fn _ ->
            %{
              positive: sentiments.positive,
              neutral: sentiments.neutral,
              negative: sentiments.negative,
            }
        end
    end

    candidate
  end

  def render("media_sentiment.json", %{media_sentiment: media_sentiment}) do
    media_sentiment
    |> Map.drop([:__meta__, :news])
  end

end
