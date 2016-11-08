defmodule RojakAPI.V1.PairingView do
  use RojakAPI.Web, :view

  def render("index.json", %{pairings: pairings}) do
    render_many(pairings, RojakAPI.V1.PairingView, "pairing.json")
  end

  def render("show.json", %{pairing: pairing}) do
    render_one(pairing, RojakAPI.V1.PairingView, "pairing.json")
  end

  def render("pairing.json", %{pairing: pairing}) do
    pairing =
      pairing
      |> Map.drop([:__meta__, :cagub, :cawagub])

    # Embed candidates
    pairing = case Map.get(pairing, :candidates) do
      nil ->
        pairing |> Map.drop([:candidates])
      %{cagub: cagub, cawagub: cawagub} ->
        Map.update! pairing, :candidates, fn _ ->
          %{
            cagub: Map.drop(cagub, [:__meta__]),
            cawagub: Map.drop(cawagub, [:__meta__]),
          }
        end
    end

    # Embed overall_sentiments
    pairing = case Map.get(pairing, :overall_sentiments) do
      nil ->
        pairing |> Map.drop([:overall_sentiments])
      _ ->
        pairing
    end

    # Embed sentiments_by_media
    pairing = case Map.get(pairing, :sentiments_by_media) do
      nil ->
        pairing |> Map.drop([:sentiments_by_media])
      sentiments ->
        Map.update! pairing, :sentiments_by_media, fn _ ->
          Enum.map sentiments, fn sentiment ->
            media =
              sentiment
              |> Map.get(:media)
              |> Map.drop([:__struct__, :__meta__, :latest_news])
            %{sentiment | media: media}
          end
        end
    end

    pairing
  end

end
