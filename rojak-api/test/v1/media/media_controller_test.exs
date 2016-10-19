defmodule RojakAPI.MediaControllerTest do
  use RojakAPI.ConnCase

  @media_properties [
    "id",
    "name",
    "website_url",
    "logo_url",
    "fbpage_username",
    "twitter_username",
    "instagram_username",
  ]

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  test "lists all entries on index", %{conn: conn} do
    conn = get conn, v1_media_path(conn, :index)
    media_list = json_response(conn, 200)
    assert Enum.count(media_list) >= 0

    media_item = List.first(media_list)
    assert item_has_valid_properties?(media_item), "Item is missing valid properties."
  end

  test "shows chosen resource", %{conn: conn} do
    conn = get conn, v1_media_path(conn, :show, 1)
    media_item = json_response(conn, 200)
    assert item_has_valid_properties?(media_item), "Item is missing valid properties."
  end

  test "renders page not found when id is nonexistent", %{conn: conn} do
    assert_error_sent 404, fn ->
      get conn, v1_media_path(conn, :show, -1)
    end
  end

  defp item_has_valid_properties?(item) do
    Enum.all?(@media_properties, &(Map.has_key?(item, &1)))
  end

end
