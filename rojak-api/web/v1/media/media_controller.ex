defmodule RojakAPI.V1.MediaController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Media

  defparams media_index_params %{
    limit: [field: :integer, default: 10],
    offset: [field: :integer, default: 0],
  }

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &media_index_params/1
    media = Media.fetch(validated_params)
    render(conn, "index.json", media: media)
  end

  defparams media_show_params %{
    id!: :integer,
  }

  def show(conn, params) do
    validated_params = ParamsValidator.validate params, &media_show_params/1
    media = Media.fetch_one(validated_params)
    render(conn, "show.json", media: media)
  end

end
