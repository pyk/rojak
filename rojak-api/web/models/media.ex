defmodule RojakAPI.Media do
  use RojakAPI.Web, :model

  schema "media" do
    field :name, :string
    field :website_url, :string
    field :logo_url, :string
    field :fbpage_username, :string
    field :description, :string

    # Relationship
    has_many :news, RojakAPI.News

    timestamps()
  end

  @doc """
  Builds a changeset based on the `struct` and `params`.
  """
  def changeset(struct, params \\ %{}) do
    struct
    |> cast(params, [:name, :website_url, :logo_url, :fbpage_username,
        :description])
    |> validate_required([:name, :website_url, :logo_url])
  end
end
