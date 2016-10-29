defmodule RojakAPI.V1.CandidateController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Candidate

  @apidoc """
    @api {get} /candidates Get Candidates 
    @apiGroup Candidates
    @apiName GetCandidates
    @apiVersion 1.0.0
    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>sentiments</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>
    @apiDescription Get a list of candidates running in the election, optionally with <code>sentiments</code>.
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
          "sentiments": {
            "positive": 0.41256,
            "negative": 0.12345,
            "neutral": 0.46399
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
          "sentiments": {
            "positive": 0.41256,
            "negative": 0.12345,
            "neutral": 0.46399
          }
        }
      ]
  """
  defparams candidate_index_params(%{
    embed: [:string],
  }) do
    def changeset(ch, params) do
      cast(ch, params, [:embed])
      |> validate_subset(:embed, ["sentiments"])
    end
  end

  def index(conn, params) do
    validated_params = ParamsValidator.validate params, &candidate_index_params/1
    candidates = Candidate.fetch(validated_params)
    render(conn, "index.json", candidates: candidates)
  end

  @apidoc """
    @api {get} /candidates/:candidateId Get a Candidate
    @apiGroup Candidates
    @apiName GetCandidate
    @apiVersion 1.0.0
    @apiParam {String} candidateId
    @apiParam {String} [embed[]] Fields to embed on the response. Available fields: <code>sentiments</code>, <code>candidates</code> </br></br> Example:
      <pre>?embed[]=field1&embed[]=field2</pre>
    @apiDescription Get a candidates based on {candidateId}, optionally with <code>sentiments</code> and <code>pairing</code>.
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
        "sentiments": {
          "positive": 0.41256,
          "negative": 0.12345,
          "neutral": 0.46399
        },
        "pairing": {
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
          "updated_at": 1341533193
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
      |> validate_subset(:embed, ["sentiments", "pairing"])
    end
  end

  def show(conn, params) do
    validated_params = ParamsValidator.validate params, &candidate_show_params/1
    candidate = Candidate.fetch_one(validated_params)
    render(conn, "show.json", candidate: candidate)
  end

  @apidoc """
    @api {get} /candidates/:candidateId/media-sentiments Get Media-Sentiments
    @apiGroup Candidates
    @apiName GetCandidateMediaSentiments
    @apiVersion 1.0.0
    @apiParam {String} candidateId
    @apiParam {Integer} [offset=0] Skip over a number of elements by specifying an offset value for the query. </br></br> Example:
      <pre>?offset=20</pre>
    @apiParam {Integer} [limit=10] Limit the number of elements on the response. </br></br> Example:
      <pre>?limit=20</pre>
    @apiDescription Get a breakdown of media sentiments for this candidate.
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

end
