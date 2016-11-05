defmodule RojakAPI.ErrorView do
  use RojakAPI.Web, :view

  def render("404.json", _assigns) do
    %{message: "item not found"}
  end

  def render("422.json", _assigns) do
    %{message: "invalid parameters provided"}
  end

  def render("500.json", _assigns) do
    %{message: "internal server error"}
  end

  # In case no render clause matches or no
  # template is found, let's render it as 500
  def template_not_found(_template, assigns) do
    render "500.json", assigns
  end
end
