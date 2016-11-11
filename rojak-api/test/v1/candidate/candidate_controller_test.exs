defmodule RojakAPI.CandidateControllerTest do
  use RojakAPI.ConnCase

  @candidate_properties ~w(
    id
    full_name
    alias_name
    place_of_birth
    date_of_birth
    religion
    website_url
    photo_url
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
    conn = get conn, v1_candidate_path(conn, :index)
    candidate_list = json_response(conn, 200)
    assert Enum.count(candidate_list) >= 0

    candidate_item = List.first(candidate_list)
    assert item_has_valid_properties?(candidate_item), "Item is missing valid properties."
  end

  test "allows embedding pairing on index", %{conn: conn} do
    conn = get conn, v1_candidate_path(conn, :index), %{embed: ["pairing"]}
    candidate_list = json_response(conn, 200)
    assert Enum.count(candidate_list) >= 0

    candidate_item = List.first(candidate_list)
    assert item_has_valid_properties?(candidate_item), "Item is missing valid properties."

    assert Map.has_key?(candidate_item, "pairing")
  end

  test "renders invalid parameters when trying to embed invalid field on index", %{conn: conn} do
    assert_error_sent 422, fn ->
      get conn, v1_candidate_path(conn, :index), %{embed: ["foo"]}
    end
  end

  test "shows chosen resource", %{conn: conn} do
    conn = get conn, v1_candidate_path(conn, :show, 1)
    candidate_item = json_response(conn, 200)
    assert item_has_valid_properties?(candidate_item), "Item is missing valid properties."
  end

  test "allows embedding pairing on show", %{conn: conn} do
    conn = get conn, v1_candidate_path(conn, :show, 1), %{embed: ["pairing"]}
    candidate_item = json_response(conn, 200)
    assert item_has_valid_properties?(candidate_item), "Item is missing valid properties."

    assert Map.has_key?(candidate_item, "pairing")
  end

  test "renders invalid parameters when trying to embed invalid field on show", %{conn: conn} do
    assert_error_sent 422, fn ->
      get conn, v1_candidate_path(conn, :show, 1), %{embed: ["foo"]}
    end
  end

  test "renders page not found when id is nonexistent", %{conn: conn} do
    assert_error_sent 404, fn ->
      get conn, v1_candidate_path(conn, :show, -1)
    end
  end

  defp item_has_valid_properties?(item) do
    Enum.all?(@candidate_properties, &(Map.has_key?(item, &1)))
  end

end
