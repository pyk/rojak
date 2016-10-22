defmodule RojakAPI.V1.PairingController do
  use RojakAPI.Web, :controller

  alias RojakAPI.PairOfCandidates

  # TODO: also load sentiments and candidates if `embed` parameter is set

  def index(conn, _params) do
    pairings = Repo.all(PairOfCandidates)
    render(conn, "index.json", pairings: pairings)
  end

  def show(conn, %{"id" => id}) do
    pairing = Repo.get!(PairOfCandidates, id)
    render(conn, "show.json", pairing: pairing)
  end

end
