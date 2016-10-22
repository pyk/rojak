defmodule RojakAPI.V1.MediaController do
  use RojakAPI.Web, :controller
  use Params

  alias RojakAPI.Media
  alias RojakAPI.V1.ParamsValidator

  defparams index_params %{
    limit: [field: :integer, default: 10],
    offset: [field: :integer, default: 0],
  }

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &index_params/1
    %{limit: limit, offset: offset} = validated_params
    media = Repo.all(
      from Media,
        limit: ^limit,
        offset: ^offset
    )
    render(conn, "index.json", media: media)
  end

  def show(conn, %{"id" => id}) do
    media = Repo.get!(Media, id)
    render(conn, "show.json", media: media)
  end

end
