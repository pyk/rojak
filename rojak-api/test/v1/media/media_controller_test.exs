defmodule RojakAPI.MediaControllerTest do
  use RojakAPI.ConnCase

  @media_properties ~w(
    id
    name
    website_url
    logo_url
    fbpage_username
    twitter_username
    instagram_username
    inserted_at
    updated_at
  )

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

  test "allows limit on index", %{conn: conn} do
    conn = get conn, v1_media_path(conn, :index), %{limit: 1}
    media_list = json_response(conn, 200)
    assert Enum.count(media_list) == 1
  end

  test "limit defaults to 10", %{conn: conn} do
    conn = get conn, v1_media_path(conn, :index)
    media_list = json_response(conn, 200)
    assert Enum.count(media_list) == 10
  end

  test "renders invalid parameters when limit is not an integer", %{conn: conn} do
    assert_error_sent 422, fn ->
      get conn, v1_media_path(conn, :index), %{limit: "foo"}
    end
  end

  test "allows offset on index", %{conn: conn} do
    conn = get conn, v1_media_path(conn, :index), %{offset: 0}
    media_list = json_response(conn, 200)

    conn = get conn, v1_media_path(conn, :index), %{offset: 1}
    media_list_offset = json_response(conn, 200)

    assert Enum.at(media_list, 1) == Enum.at(media_list_offset, 0)
  end

  test "renders invalid parameters when offset is not an integer", %{conn: conn} do
    assert_error_sent 422, fn ->
      get conn, v1_media_path(conn, :index), %{offset: "foo"}
    end
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

  test "list sentiments of the candidates on :sentiments", %{conn: conn} do
    conn = get conn, v1_media_path(conn, :sentiments, 1)
    sentiment_list = json_response(conn, 200)
    assert Enum.count(sentiment_list) >= 0

    sentiment_item = List.first(sentiment_list)
    assert Map.has_key?(sentiment_item, "pairing")
    assert Map.has_key?(sentiment_item, "candidates")

    pairing = Map.get(sentiment_item, "pairing")
    assert Map.has_key?(pairing, "sentiments")

    candidates = Map.get(sentiment_item, "candidates")
    assert Map.has_key?(candidates, "cagub")
    assert Map.has_key?(candidates, "cawagub")

    cagub = Map.get(candidates, "cagub")
    cawagub = Map.get(candidates, "cawagub")
    assert Map.has_key?(cagub, "sentiments")
    assert Map.has_key?(cawagub, "sentiments")
  end

  defp item_has_valid_properties?(item) do
    Enum.all?(@media_properties, &(Map.has_key?(item, &1)))
  end

end
