defmodule RojakAPI.NewsControllerTest do
  use RojakAPI.ConnCase

  @news_properties ~w(
    id
    media_id
    title
    url
    author_name
    inserted_at
    updated_at
  )

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

  test "allows limit on index", %{conn: conn} do
    conn = get conn, v1_news_path(conn, :index), %{limit: 1}
    news_list = json_response(conn, 200)
    assert Enum.count(news_list) == 1
  end

  test "limit defaults to 10", %{conn: conn} do
    conn = get conn, v1_news_path(conn, :index)
    news_list = json_response(conn, 200)
    assert Enum.count(news_list) == 10
  end

  test "renders invalid parameters when limit is not an integer", %{conn: conn} do
    assert_error_sent 422, fn ->
      get conn, v1_news_path(conn, :index), %{limit: "foo"}
    end
  end

  test "allows offset on index", %{conn: conn} do
    conn = get conn, v1_news_path(conn, :index), %{offset: 0}
    news_list = json_response(conn, 200)

    conn = get conn, v1_news_path(conn, :index), %{offset: 1}
    news_list_offset = json_response(conn, 200)

    assert Enum.at(news_list, 1) == Enum.at(news_list_offset, 0)
  end

  test "renders invalid parameters when offset is not an integer", %{conn: conn} do
    assert_error_sent 422, fn ->
      get conn, v1_news_path(conn, :index), %{offset: "foo"}
    end
  end

  test "allows embedding mentions on index", %{conn: conn} do
    conn = get conn, v1_news_path(conn, :index), %{embed: ["mentions"]}
    news_list = json_response(conn, 200)
    assert Enum.count(news_list) >= 0

    news_item = List.first(news_list)
    assert Map.has_key?(news_item, "mentions")
  end

  test "allows filtering by media id", %{conn: conn} do
    conn = get conn, v1_news_path(conn, :index), %{media_id: ["1"]}
    news_list = json_response(conn, 200)
    assert Enum.all? news_list, fn news_item ->
      Map.get(news_item, "media_id") == 1
    end
  end

  test "renders invalid parameters when media_id is not an array of integers", %{conn: conn} do
    assert_error_sent 422, fn ->
      get conn, v1_news_path(conn, :index), %{media_id: "1"}
    end

    assert_error_sent 422, fn ->
      get conn, v1_news_path(conn, :index), %{media_id: ["foo"]}
    end
  end

  test "allows filtering by mentioned candidate id", %{conn: conn} do
    conn = get conn, v1_news_path(conn, :index), %{candidate_id: ["1"], embed: ["mentions"]}
    news_list = json_response(conn, 200)
    assert Enum.all? news_list, fn news_item ->
      mentions = Map.get(news_item, "mentions")
      Enum.any? mentions, fn mentioned_candidate ->
        Map.get(mentioned_candidate, "id") == 1
      end
    end
  end

  test "renders invalid parameters when candidate_id is not an array of integers", %{conn: conn} do
    assert_error_sent 422, fn ->
      get conn, v1_news_path(conn, :index), %{candidate_id: "1"}
    end

    assert_error_sent 422, fn ->
      get conn, v1_news_path(conn, :index), %{candidate_id: ["foo"]}
    end
  end

  test "shows chosen resource", %{conn: conn} do
    conn = get conn, v1_news_path(conn, :show, 1)
    news_item = json_response(conn, 200)
    assert item_has_valid_properties?(news_item), "Item is missing valid properties."
  end

  test "allows embedding mentions on show", %{conn: conn} do
    conn = get conn, v1_news_path(conn, :show, 1), %{embed: ["mentions"]}
    news_item = json_response(conn, 200)

    assert Map.has_key?(news_item, "mentions")
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
