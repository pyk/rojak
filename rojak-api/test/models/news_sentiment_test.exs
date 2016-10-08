defmodule RojakAPI.NewsSentimentTest do
  use RojakAPI.ModelCase

  alias RojakAPI.NewsSentiment

  @valid_attrs %{score: "120.5"}
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = NewsSentiment.changeset(%NewsSentiment{}, @valid_attrs)
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = NewsSentiment.changeset(%NewsSentiment{}, @invalid_attrs)
    refute changeset.valid?
  end
end
