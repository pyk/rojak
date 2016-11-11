defmodule RojakAPI.Data.Schemas.Candidate do
  use Ecto.Schema

  schema "candidate" do
    field :full_name, :string
    field :alias_name, :string
    field :place_of_birth, :string
    field :date_of_birth, Ecto.Date
    field :religion, :string
    field :website_url, :string
    field :photo_url, :string
    field :fbpage_username, :string
    field :instagram_username, :string
    field :twitter_username, :string

    # Virtual fields for embedding joins
    field :pairing, :map, virtual: true

    timestamps()
  end

end
