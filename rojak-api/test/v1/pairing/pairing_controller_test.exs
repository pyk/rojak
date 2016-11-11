defmodule RojakAPI.PairingControllerTest do
  use RojakAPI.ConnCase

  @pairing_properties ~w(
    id
    name
    website_url
    logo_url
    fbpage_username
    twitter_username
    instagram_username
    slogan
    description
    cagub_id
    cawagub_id
    inserted_at
    updated_at
  )

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  test "lists all entries on index", %{conn: conn} do
    conn = get conn, v1_pairing_path(conn, :index)
    pairing_list = json_response(conn, 200)
    assert Enum.count(pairing_list) >= 0

    pairing_item = List.first(pairing_list)
    assert item_has_valid_properties?(pairing_item), "Item is missing valid properties."
  end

  test "allows embedding candidates on index", %{conn: conn} do
    conn = get conn, v1_pairing_path(conn, :index), %{embed: ["candidates"]}
    pairing_list = json_response(conn, 200)
    assert Enum.count(pairing_list) >= 0

    pairing_item = List.first(pairing_list)
    assert item_has_valid_properties?(pairing_item), "Item is missing valid properties."

    assert Map.has_key?(pairing_item, "candidates")
  end

  test "allows embedding overall_sentiments on index", %{conn: conn} do
    conn = get conn, v1_pairing_path(conn, :index), %{embed: ["overall_sentiments"]}
    pairing_list = json_response(conn, 200)
    assert Enum.count(pairing_list) >= 0

    pairing_item = List.first(pairing_list)
    assert item_has_valid_properties?(pairing_item), "Item is missing valid properties."

    assert Map.has_key?(pairing_item, "overall_sentiments")
  end

  test "renders invalid parameters when trying to embed invalid field on index", %{conn: conn} do
    assert_error_sent 422, fn ->
      get conn, v1_pairing_path(conn, :index), %{embed: ["foo"]}
    end
  end

  test "shows chosen resource", %{conn: conn} do
    conn = get conn, v1_pairing_path(conn, :show, 1)
    pairing_item = json_response(conn, 200)
    assert item_has_valid_properties?(pairing_item), "Item is missing valid properties."
  end

  test "allows embedding candidates on show", %{conn: conn} do
    conn = get conn, v1_pairing_path(conn, :show, 1), %{embed: ["candidates"]}
    pairing_item = json_response(conn, 200)
    assert item_has_valid_properties?(pairing_item), "Item is missing valid properties."

    assert Map.has_key?(pairing_item, "candidates")
  end

  test "allows embedding overall_sentiments on show", %{conn: conn} do
    conn = get conn, v1_pairing_path(conn, :show, 1), %{embed: ["overall_sentiments"]}
    pairing_item = json_response(conn, 200)
    assert item_has_valid_properties?(pairing_item), "Item is missing valid properties."

    assert Map.has_key?(pairing_item, "overall_sentiments")
  end

  test "allows embedding sentiments_by_media on show", %{conn: conn} do
    conn = get conn, v1_pairing_path(conn, :show, 1), %{embed: ["sentiments_by_media"]}
    pairing_item = json_response(conn, 200)
    assert item_has_valid_properties?(pairing_item), "Item is missing valid properties."

    assert Map.has_key?(pairing_item, "sentiments_by_media")
  end

  test "renders invalid parameters when trying to embed invalid field on show", %{conn: conn} do
    assert_error_sent 422, fn ->
      get conn, v1_pairing_path(conn, :show, 1), %{embed: ["foo"]}
    end
  end

  test "renders page not found when id is nonexistent", %{conn: conn} do
    assert_error_sent 404, fn ->
      get conn, v1_pairing_path(conn, :show, -1)
    end
  end

  defp item_has_valid_properties?(item) do
    Enum.all?(@pairing_properties, &(Map.has_key?(item, &1)))
  end

end
