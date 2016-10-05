defmodule RojakAPI.IndexView do
  use RojakAPI.Web, :view

  def render("index.json", _assigns) do
    %{version: "0.0.0", message: "Selamat datang di rojak-api!"}
  end

end
