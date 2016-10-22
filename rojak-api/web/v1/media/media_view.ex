defmodule RojakAPI.V1.MediaView do
  use RojakAPI.Web, :view

  def render("index.json", %{media: media}) do
    render_many(media, RojakAPI.V1.MediaView, "media.json")
  end

  def render("show.json", %{media: media}) do
    render_one(media, RojakAPI.V1.MediaView, "media.json")
  end

  def render("media.json", %{media: media}) do
    Map.drop media, [:__meta__, :news]
  end
end
