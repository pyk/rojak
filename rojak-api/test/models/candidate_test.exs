defmodule RojakAPI.CandidateTest do
  use RojakAPI.ModelCase

  alias RojakAPI.Candidate
  alias Ecto.Date

  @valid_attrs %{
    full_name: "some content",
    alias_name: "some content",
    place_of_birth: "some content",
    date_of_birth: Date.from_erl({2016, 10, 1}),
    religion: "some content",
    website_url: "some content",
    photo_url: "some content",
    fbpage_username: "some content",
    instagram_username: "some content",
    twitter_username: "some content"
  }
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = Candidate.changeset(%Candidate{}, @valid_attrs)
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = Candidate.changeset(%Candidate{}, @invalid_attrs)
    refute changeset.valid?
  end
end
