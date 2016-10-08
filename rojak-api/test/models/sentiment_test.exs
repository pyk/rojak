defmodule RojakAPI.SentimentTest do
  use RojakAPI.ModelCase

  alias RojakAPI.Sentiment

  @valid_attrs %{name: "some content"}
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = Sentiment.changeset(%Sentiment{}, @valid_attrs)
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = Sentiment.changeset(%Sentiment{}, @invalid_attrs)
    refute changeset.valid?
  end
end
