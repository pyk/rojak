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
    Map.drop pairing, [:__meta__, :cagub, :cawagub]
  end
end
