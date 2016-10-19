defmodule RojakAPI.V1.MediaView do
  use RojakAPI.Web, :view

  def render("index.json", %{media: media}) do
    render_many(media, RojakAPI.V1.MediaView, "media.json")
  end

  def render("show.json", %{media: media}) do
    render_one(media, RojakAPI.V1.MediaView, "media.json")
  end

  def render("media.json", %{media: media}) do
    %{
      "id": media.id,
      "name": media.name,
      "website_url": media.website_url,
      "logo_url": media.logo_url,
      "fbpage_username": media.fbpage_username,
      "twitter_username": media.twitter_username,
      "instagram_username": media.instagram_username,
    }
  end
end
