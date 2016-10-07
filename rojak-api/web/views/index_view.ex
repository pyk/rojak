defmodule RojakAPI.IndexView do
  use RojakAPI.Web, :view

  def render("index.json", _assigns) do
    %{version: Mix.Project.config[:version], message: "Selamat datang di rojak-api!"}
  end

end
