defmodule RojakAPI.NewsTest do
  use RojakAPI.ModelCase

  alias RojakAPI.News

  @valid_attrs %{content: "some content", title: "some content", url: "some content"}
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = News.changeset(%News{}, @valid_attrs)
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = News.changeset(%News{}, @invalid_attrs)
    refute changeset.valid?
  end
end
