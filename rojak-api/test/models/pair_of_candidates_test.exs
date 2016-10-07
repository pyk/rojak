defmodule RojakAPI.PairOfCandidatesTest do
  use RojakAPI.ModelCase

  alias RojakAPI.PairOfCandidates
  alias RojakAPI.Candidate
  alias Ecto.Date

  @valid_attrs %{
    description: "some content",
    fbpage_username: "some content",
    instagram_username: "some content",
    logo_url: "some content",
    name: "some content",
    slogan: "some content",
    twitter_username: "some content",
    website_url: "some content",
    cagub: %Candidate{
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
    },
    cawagub: %Candidate{
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
  }
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = PairOfCandidates.changeset(%PairOfCandidates{}, @valid_attrs)
    IO.puts changeset.errors
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = PairOfCandidates.changeset(%PairOfCandidates{}, @invalid_attrs)
    refute changeset.valid?
  end
end
