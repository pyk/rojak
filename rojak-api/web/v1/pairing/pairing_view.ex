defmodule RojakAPI.V1.PairingView do
  use RojakAPI.Web, :view

  # TODO: enable embedding sentiments and candidate

  def render("index.json", %{pairings: pairings}) do
    render_many(pairings, RojakAPI.V1.PairingView, "pairing.json")
  end

  def render("show.json", %{pairing: pairing}) do
    render_one(pairing, RojakAPI.V1.PairingView, "pairing.json")
  end

  def render("pairing.json", %{pairing: pairing}) do
    pairing =
      pairing
      |> Map.drop([:__meta__])

    # Embed candidates
    pairing = cond do
      Ecto.assoc_loaded?(pairing.cagub) and Ecto.assoc_loaded?(pairing.cawagub) ->
        pairing
        |> Map.put(:candidates, %{
            cagub: Map.drop(pairing.cagub, [:__meta__, :mentioned_in, :sentiments]),
            cawagub: Map.drop(pairing.cawagub, [:__meta__, :mentioned_in, :sentiments]),
          })
      true ->
        pairing
    end |> Map.drop([:cagub, :cawagub])

    pairing
  end
end
