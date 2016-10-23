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
            cagub: Map.drop(cagub, [:__meta__, :mentioned_in, :sentiments]),
            cawagub: Map.drop(cawagub, [:__meta__, :mentioned_in, :sentiments]),
          }
        end
    end

    pairing
  end
end
