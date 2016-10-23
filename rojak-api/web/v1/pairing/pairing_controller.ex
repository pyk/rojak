defmodule RojakAPI.V1.PairingController do
  use RojakAPI.Web, :controller

  alias RojakAPI.PairOfCandidates

  # TODO: also load sentiments and candidates if `embed` parameter is set

  defparams pairing_index_params(%{
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:embed])
      |> validate_subset(:embed, ["sentiments"])
    end
  end

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &pairing_index_params/1
    %{embed: embed} = validated_params
    pairings = Repo.all(PairOfCandidates)
    render(conn, "index.json", pairings: pairings)
  end

  defparams pairing_show_params(%{
    id!: :integer,
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:id, :embed])
      |> validate_subset(:embed, ["sentiments", "candidates"])
    end
  end

  def show(conn, %{"id" => id} = params) do
    validated_params = ParamsValidator.validate params, &pairing_show_params/1
    %{embed: embed} = validated_params
    pairing =
      PairOfCandidates
      |> PairOfCandidates.fetch_embed(embed)
      |> Repo.get!(id)
    render(conn, "show.json", pairing: pairing)
  end

end
