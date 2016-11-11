defmodule RojakAPI.V1.PairingController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Data.PairOfCandidates

  @apidoc """
    @api {get} /pairings Get list of pairings
    @apiGroup Pairing
    @apiName PairingList
    @apiDescription Get a list of pairs of candidates running in the election, optionally with <code>candidates</code> and <code>overall_sentiments</code>.

    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>candidates</code>, <code>overall_sentiments</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
      [
        {
          "id": 1,
          "name": "Ahok Djarot",
          "cagub_id": 1,
          "cawagub_id": 2,
          "website_url": "http://ahokdjarot.id",
          "logo_url": "http://ahokdjarot.id/themes/custom/jakartabaru/logo.png",
          "fbpage_username": "AhokDjarot",
          "twitter_username": "AhokDjarot",
          "instagram_username": "ahokdjarot",
          "slogan": "TETAP AHOK-DJAROT!",
          "description": "Jangan biarkan Jakarta Baru berhenti sampai disini! Mari Bersama-sama Dukung Ahok & Djarot sebagai Cagub & Cawagub DKI Jakarta 2017.",
          "inserted_at": 1341533193,
          "updated_at": 1341533193,

          // embedded fields
          "candidates": {
            "cagub": {
              // cagub candidate data
            },
            "cawagub": {
              // cawagub candidate data
            }
          },
          "overall_sentiments": {
            "positive_news_count": 1234,
            "negative_news_count": 1234
          }
        },
        {
          "id": 2,
          "name": "Anies Sandi",
          "cagub_id": 3,
          "cawagub_id": 4,
          "website_url": "",
          "logo_url": "",
          "fbpage_username": "",
          "twitter_username": "",
          "instagram_username": "",
          "slogan": "",
          "description": "",
          "inserted_at": 1341533193,
          "updated_at": 1341533193,

          // embedded fields
          "candidates": {
            "cagub": {
              // cagub candidate data
            },
            "cawagub": {
              // cawagub candidate data
            }
          },
          "overall_sentiments": {
            "positive_news_count": 1234,
            "negative_news_count": 1234
          }
        }
      ]
  """
  defparams pairing_index_params(%{
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:embed])
      |> validate_subset(:embed, ["candidates", "overall_sentiments"])
    end
  end

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &pairing_index_params/1
    pairings = PairOfCandidates.fetch(validated_params)
    render(conn, "index.json", pairings: pairings)
  end

  @apidoc """
    @api {get} /pairings/:pairingId Get a single pairing
    @apiGroup Pairing
    @apiName PairingSingle
    @apiDescription Get a pair of candidates based on {pairingId}, optionally with <code>candidates</code>, <code>overall_sentiments</code>, and <code>sentiments_by_media</code>.

    @apiParam {String} pairingId
    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>candidates</code>, <code>overall_sentiments</code>, <code>sentiments_by_media</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
      {
        "id": 3,
        "name": "Agus Sylvi",
        "cagub_id": 5,
        "cawagub_id": 6,
        "website_url": "http://relawanagussylvi.com",
        "logo_url": "https://pbs.twimg.com/profile_images/783564904460460032/VgVxZX-l.jpg",
        "fbpage_username": "RelawanAgusSylvi",
        "twitter_username": "RelAgusSylvi",
        "instagram_username": "",
        "slogan": "Jakarta Untuk Rakyat",
        "description": "",
        "inserted_at": 1341533193,
        "updated_at": 1341533193,

        // embedded fields
        "candidates": {
          "cagub": {
            // cagub candidate data
          },
          "cawagub": {
            // cawagub candidate data
          }
        },
        "overall_sentiments": {
          "positive_news_count": 1234,
          "negative_news_count": 1234
        },
        "sentiments_by_media": [
          {
            "media": {
              // media data
            },
            "positive_news_count": 123,
            "negative_news_count": 123
          }
        ]
      }
    @apiErrorExample {json} Item Not Found
      HTTP/1.1 404 Not Found
      {
        "message" : "item not found"
      }
  """
  defparams pairing_show_params(%{
    id!: :integer,
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:id, :embed])
      |> validate_subset(:embed, ["candidates", "overall_sentiments", "sentiments_by_media"])
    end
  end

  def show(conn, params) do
    validated_params = ParamsValidator.validate params, &pairing_show_params/1
    pairing = PairOfCandidates.fetch_one(validated_params)
    render(conn, "show.json", pairing: pairing)
  end

end
