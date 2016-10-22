defmodule RojakAPI.V1.CandidateController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Candidate

  # TODO: also load sentiments and pairing if `embed` parameter is set

  def index(conn, _params) do
    candidates = Repo.all(Candidate)
    render(conn, "index.json", candidates: candidates)
  end

  def show(conn, %{"id" => id}) do
    candidate = Repo.get!(Candidate, id)
    render(conn, "show.json", candidate: candidate)
  end

end
