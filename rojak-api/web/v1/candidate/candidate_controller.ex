defmodule RojakAPI.V1.CandidateController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Data.Candidate

  @apidoc """
    @api {get} /candidates Get list of candidates
    @apiGroup Candidate
    @apiName CandidateList
    @apiDescription Get a list of candidates running in the election, optionally with <code>pairing</code>.

    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>pairing</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
      [
        {
          "id": 1,
          "full_name": "Basuki Tjahaja Purnama",
          "alias_name": "Ahok",
          "place_of_birth": "Manggar, Belitung Timur",
          "date_of_birth": "1966-06-29",
          "religion": "Kristen Protestan",
          "website_url": "http://ahok.org",
          "photo_url": "https://upload.wikimedia.org/wikipedia/id/7/7a/Gubernur_DKI_Basuki.jpg",
          "fbpage_username": "AhokBTP",
          "twitter_username": "basuki_btp",
          "instagram_username": "basukibtp",
          "inserted_at": 1341533193,
          "updated_at": 1341533193

          // embeddable fields
          "pairing": {
            // pairing data
          }
        },
        {
          "id": 2,
          "full_name": "Anies Baswedan",
          "alias_name": "Anies",
          "place_of_birth": "Kuningan",
          "date_of_birth": "1969-05-07",
          "religion": "Islam",
          "website_url": "http://aniesbaswedan.com",
          "photo_url": "https://upload.wikimedia.org/wikipedia/commons/e/eb/Anies-baswedan-Dec-2010.jpg",
          "fbpage_username": "aniesbaswedan",
          "twitter_username": "aniesbaswedan",
          "instagram_username": "aniesbaswedan",
          "inserted_at": 1341533193,
          "updated_at": 1341533193

          // embeddable fields
          "pairing": {
            // pairing data
          }
        }
      ]
  """
  defparams candidate_index_params(%{
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:embed])
      |> validate_subset(:embed, ["pairing"])
    end
  end

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &candidate_index_params/1
    candidates = Candidate.fetch(validated_params)
    render(conn, "index.json", candidates: candidates)
  end

  @apidoc """
    @api {get} /candidates/:candidateId Get a single candidate
    @apiGroup Candidate
    @apiName CandidateSingle
    @apiDescription Get a candidate based on {candidateId}, optionally with <code>pairing</code>.

    @apiParam {String} candidateId
    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>pairing</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>

    @apiSuccessExample {json} Success
      HTTP/1.1 200 OK
      {
        "id": 1,
        "full_name": "Basuki Tjahaja Purnama",
        "alias_name": "Ahok",
        "place_of_birth": "Manggar, Belitung Timur",
        "date_of_birth": "1966-06-29",
        "religion": "Kristen Protestan",
        "website_url": "http://ahok.org",
        "photo_url": "https://upload.wikimedia.org/wikipedia/id/7/7a/Gubernur_DKI_Basuki.jpg",
        "fbpage_username": "AhokBTP",
        "twitter_username": "basuki_btp",
        "instagram_username": "basukibtp",
        "inserted_at": 1341533193,
        "updated_at": 1341533193,

        // embeddable fields
        "pairing": {
          // pairing data
        }
      }
    @apiErrorExample {json} Item Not Found
      HTTP/1.1 404 Not Found
      {
        "message" : "item not found"
      }
  """
  defparams candidate_show_params(%{
    id!: :integer,
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:id, :embed])
      |> validate_subset(:embed, ["pairing"])
    end
  end

  def show(conn, params) do
    validated_params = ParamsValidator.validate params, &candidate_show_params/1
    candidate = Candidate.fetch_one(validated_params)
    render(conn, "show.json", candidate: candidate)
  end

end
