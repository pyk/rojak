defmodule RojakAPI.IndexView do
  use RojakAPI.Web, :view

  def render("index.json", _assigns) do
    %{version: RojakAPI.version, message: "Selamat datang di rojak-api!"}
  end

end
