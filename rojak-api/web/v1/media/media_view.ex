defmodule RojakAPI.V1.MediaView do
  use RojakAPI.Web, :view

  def render("index.json", %{media: media}) do
    render_many(media, RojakAPI.V1.MediaView, "media.json")
  end

  def render("show.json", %{media: media}) do
    render_one(media, RojakAPI.V1.MediaView, "media.json")
  end

  def render("media.json", %{media: media}) do
    media =
      media
      |> Map.drop([:__meta__])

    # embed latest_news
    media = case Map.get(media, :latest_news) do
      %Ecto.Association.NotLoaded{} ->
        media
        |> Map.drop([:latest_news])
      latest_news ->
        media
        |> Map.update!(:latest_news, fn _ ->
          Enum.map(latest_news, fn news ->
            Map.drop news, [:__meta__, :media, :mentions, :sentiments]
          end)
        end)
    end

    # embed sentiments_on_pairings
    media = case Map.get(media, :sentiments_on_pairings) do
      nil ->
        media
        |> Map.drop([:sentiments_on_pairings])
        sentiments ->
          Map.update! media, :sentiments_on_pairings, fn _ ->
            Enum.map sentiments, fn sentiment ->
              pairing = Map.get sentiment, :pairing
              %{sentiment | pairing: Map.drop(pairing, [:__struct__, :__meta__, :cagub, :cawagub, :candidates, :overall_sentiments]) }
            end
          end
    end

    media
  end

end
