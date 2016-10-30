defmodule RojakAPI.V1.PairingController do
  use RojakAPI.Web, :controller

  alias RojakAPI.PairOfCandidates

  @apidoc """
    @api {get} /pairings Get Pairs
    @apiGroup Pairings
    @apiName GetPairs
    @apiVersion 1.0.0
    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>sentiments</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>
    @apiDescription Get a list of pairs of candidates running in the election, optionally with <code>sentiments</code>.
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
          "sentiments": {
            "positive": 0.41256,
            "negative": 0.12345,
            "neutral": 0.46399
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
          "sentiments": {
            "positive": 0.41256,
            "negative": 0.12345,
            "neutral": 0.46399
          }
        }
      ]
  """
  defparams pairing_index_params(%{
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:embed])
      |> validate_subset(:embed, ["sentiments"])
    end
  end

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &pairing_index_params/1
    pairings = PairOfCandidates.fetch(validated_params)
    render(conn, "index.json", pairings: pairings)
  end

  @apidoc """
    @api {get} /pairings/:pairingId Get a Pair
    @apiGroup Pairings
    @apiName GetPair
    @apiVersion 1.0.0
    @apiParam {String} pairingId
    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>sentiments</code>, <code>candidates</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>
    @apiDescription Get a pair of candidates based on {pairingId}, optionally with <code>sentiments</code> and <code>candidates</code>.
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
        "sentiments": {
          "positive": 0.41256,
          "negative": 0.12345,
          "neutral": 0.46399
        },
        "candidates": {
          "cagub" : {
            "id": 3,
            "full_name": "Agus Harimurti Yudhoyono",
            "alias_name": "Agus Yudhoyono",
            "place_of_birth": "Bandung, Jawa Barat",
            "date_of_birth": "1978-08-10",
            "religion": "Islam",
            "website_url": "",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Mayor_Infanteri_Agus_Harimurti_Yudhoyono%2C_M.Sc.%2C_MPA.png",
            "fbpage_username": "",
            "twitter_username": "agusyudhoyono",
            "instagram_username": "agusyudhoyono",
            "inserted_at": 1341533193,
            "updated_at": 1341533193
          },
          "cawagub" : {
            "id": 4,
            "full_name": "Sylviana Murni",
            "alias_name": "Sylvi",
            "place_of_birth": "Jakarta",
            "date_of_birth": "1958-10-11",
            "religion": "Islam",
            "website_url": "http://sylvianamurni.com",
            "photo_url": "https://pbs.twimg.com/profile_images/781481260489125888/06iQrhGr.jpg",
            "fbpage_username": "sylviana_murni",
            "twitter_username": "sylviana_murni",
            "instagram_username": "sylvianamurni_",
            "inserted_at": 1341533193,
            "updated_at": 1341533193
          }
        }
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
      |> validate_subset(:embed, ["sentiments", "candidates"])
    end
  end

  def show(conn, params) do
    validated_params = ParamsValidator.validate params, &pairing_show_params/1
    pairing = PairOfCandidates.fetch_one(validated_params)
    render(conn, "show.json", pairing: pairing)
  end

  @apidoc """
    @api {get} /pairings/:pairingId/media-sentiments Get Media-Sentiments
    @apiGroup Pairings
    @apiName GetPairMediaSentiments
    @apiVersion 1.0.0
    @apiParam {String} pairingId
    @apiParam {Integer} [offset=0] Skip over a number of elements by specifying an offset value for the query. </br></br> Example:
      <pre>?offset=20</pre>
    @apiParam {Integer} [limit=10] Limit the number of elements on the response. </br></br> Example:
      <pre>?limit=20</pre>
    @apiDescription Get a breakdown of media sentiments for this pairing.
    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
      [
        {
          "id": 1,
          "name": "detikcom",
          "website_url": "http://detik.com",
          "logo_url": "https://cdn.detik.net.id/detik2/images/logodetikcom.png?1",
          "fbpage_username": "detikcom",
          "twitter_username": "detikcom",
          "instagram_username": "detikcom",
          "inserted_at": 1341533193,
          "updated_at": 1341533193,
          "sentiments": {
            "positive": 0.41256,
            "negative": 0.12345,
            "neutral": 0.46399
          }
        }
      ]
  """
  defparams pairing_media_sentiments_params %{
    id!: :integer,
    limit: [field: :integer, default: 10],
    offset: [field: :integer, default: 0],
  }

  def media_sentiments(conn, params) do
    validated_params = ParamsValidator.validate params, &pairing_media_sentiments_params/1
    media_sentiments = PairOfCandidates.fetch_media_sentiments(validated_params)
    render(conn, "media_sentiments.json", media_sentiments: media_sentiments)
  end

end
