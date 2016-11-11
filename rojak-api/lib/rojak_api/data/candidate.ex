defmodule RojakAPI.Data.Candidate do
  import Ecto.Query

  alias RojakAPI.Repo
  alias RojakAPI.Data.Schemas.{
    Candidate,
    PairOfCandidates
  }

  def fetch(%{embed: embed}) do
    Candidate
    |> fetch_embed(embed)
    |> Repo.all
  end

  def fetch_one(%{id: id, embed: embed}) do
    Candidate
    |> fetch_embed(embed)
    |> Repo.get!(id)
  end

  defp fetch_embed(query, embed) when is_nil(embed), do: query
  defp fetch_embed(query, embed) do
    query
    |> fetch_pairing(Enum.member?(embed, "pairing"))
    |> select_embed_fields(embed)
  end

  defp select_embed_fields(query, embed) do
    case [Enum.member?(embed, "pairing")] do
      [true] ->
        from [q, p] in query,
          select: %{q | pairing: p }
      _ -> query
    end
  end

  defp fetch_pairing(query, embed?) when not embed?, do: query
  defp fetch_pairing(query, _) do
    from q in query,
      join: p in PairOfCandidates, on: q.id == p.cagub_id or q.id == p.cawagub_id
  end

end
