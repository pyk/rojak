defmodule RojakAPI.MediaTest do
  use RojakAPI.ModelCase

  alias RojakAPI.Media

  @valid_attrs %{description: "some content", fbpage_username: "some content", logo_url: "some content", name: "some content", website_url: "some content"}
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = Media.changeset(%Media{}, @valid_attrs)
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = Media.changeset(%Media{}, @invalid_attrs)
    refute changeset.valid?
  end
end
