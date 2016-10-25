defmodule RojakAPI.V1.NewsController do
  use RojakAPI.Web, :controller

  alias RojakAPI.News

  defparams news_index_params(%{
    limit: [field: :integer, default: 10],
    offset: [field: :integer, default: 0],
    embed: [:string],
    media_id: [:integer],
    candidate_id: [:integer]
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:limit, :offset, :embed, :media_id, :candidate_id])
      |> validate_subset(:embed, ["mentions"])
    end
  end

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &news_index_params/1
    news = News.fetch(validated_params)
    render(conn, "index.json", news: news)
  end

  defparams news_show_params(%{
    id!: :integer,
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:id, :embed])
      |> validate_subset(:embed, ["mentions"])
    end
  end

  def show(conn, params) do
    validated_params = ParamsValidator.validate params, &news_show_params/1
    news = News.fetch_one(validated_params)
    render(conn, "show.json", news: news)
  end

end
