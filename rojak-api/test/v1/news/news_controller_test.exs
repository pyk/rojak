defmodule RojakAPI.NewsControllerTest do
  use RojakAPI.ConnCase

  @news_properties [
    "id",
    "media_id",
    "title",
    "url",
    "author_name",
  ]

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  test "lists all entries on index", %{conn: conn} do
    conn = get conn, v1_news_path(conn, :index)
    news_list = json_response(conn, 200)
    assert Enum.count(news_list) >= 0

    news_item = List.first(news_list)
    assert item_has_valid_properties?(news_item), "Item is missing valid properties."
  end

  test "shows chosen resource", %{conn: conn} do
    conn = get conn, v1_news_path(conn, :show, 1)
    news_item = json_response(conn, 200)
    assert item_has_valid_properties?(news_item), "Item is missing valid properties."
  end

  test "renders page not found when id is nonexistent", %{conn: conn} do
    assert_error_sent 404, fn ->
      get conn, v1_news_path(conn, :show, -1)
    end
  end

  defp item_has_valid_properties?(item) do
    Enum.all?(@news_properties, &(Map.has_key?(item, &1)))
  end

end
