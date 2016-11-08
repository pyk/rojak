defmodule RojakAPI.StatsControllerTest do
  use RojakAPI.ConnCase

  @stats_properties ~w(
    media_count
    news_count
    total_sentiments_count
    positive_sentiments_count
    negative_sentiments_count
    oot_sentiments_count
  )

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  test "shows statistics", %{conn: conn} do
    conn = get conn, v1_stats_path(conn, :index)
    stats = json_response(conn, 200)
    assert item_has_valid_properties?(stats), "Stats is missing valid properties."
  end

  defp item_has_valid_properties?(item) do
    Enum.all?(@stats_properties, &(Map.has_key?(item, &1)))
  end

end
