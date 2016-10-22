defmodule RojakAPI.V1.CandidateView do
  use RojakAPI.Web, :view

  # TODO: enable embedding sentiments and pairing

  def render("index.json", %{candidates: candidates}) do
    render_many(candidates, RojakAPI.V1.CandidateView, "candidate.json")
  end

  def render("show.json", %{candidate: candidate}) do
    render_one(candidate, RojakAPI.V1.CandidateView, "candidate.json")
  end

  def render("candidate.json", %{candidate: candidate}) do
    Map.drop candidate, [:__meta__, :mentioned_in, :sentiments]
  end
end
