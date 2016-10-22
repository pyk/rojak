defmodule RojakAPI.V1.NewsController do
  use RojakAPI.Web, :controller

  alias RojakAPI.News

  # TODO: also load mentions if `embed` parameter is set

  defparams news_index_params %{
    limit: [field: :integer, default: 10],
    offset: [field: :integer, default: 0],
  }

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &news_index_params/1
    %{limit: limit, offset: offset} = validated_params
    news = Repo.all(
      from n in News,
        limit: ^limit,
        offset: ^offset,
        order_by: [desc: n.id]
    )
    render(conn, "index.json", news: news)
  end

  def show(conn, %{"id" => id}) do
    news = Repo.get!(News, id)
    render(conn, "show.json", news: news)
  end

end
