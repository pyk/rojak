defmodule RojakAPI.ErrorViewTest do
  use RojakAPI.ConnCase, async: true

  # Bring render/3 and render_to_string/3 for testing custom views
  import Phoenix.View

  test "renders 404.json" do
    assert render(RojakAPI.ErrorView, "404.json", []) ==
           %{message: "item not found"}
  end

  test "renders 422.json" do
    assert render(RojakAPI.ErrorView, "422.json", []) ==
           %{message: "invalid parameters provided"}
  end

  test "render 500.json" do
    assert render(RojakAPI.ErrorView, "500.json", []) ==
           %{message: "internal server error"}
  end

  test "render any other" do
    assert render(RojakAPI.ErrorView, "505.json", []) ==
           %{message: "internal server error"}
  end

end
