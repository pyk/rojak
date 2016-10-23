defmodule RojakAPI.V1.CandidateController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Candidate

  defparams candidate_index_params(%{
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:embed])
      |> validate_subset(:embed, ["sentiments"])
    end
  end

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &candidate_index_params/1
    candidates = Candidate.fetch(validated_params)
    render(conn, "index.json", candidates: candidates)
  end

  defparams candidate_show_params(%{
    id!: :integer,
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:id, :embed])
      |> validate_subset(:embed, ["sentiments", "pairing"])
    end
  end

  def show(conn, params) do
    validated_params = ParamsValidator.validate params, &candidate_show_params/1
    candidate = Candidate.fetch_one(validated_params)
    render(conn, "show.json", candidate: candidate)
  end

end
