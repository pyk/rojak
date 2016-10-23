defmodule RojakAPI.ParamsValidator do
  @moduledoc """
  Utility module for validating request params.
  """

  defmodule InvalidParamsError do
    @moduledoc """
    Exception raised when params validation failed.
    """

    defexception plug_status: :unprocessable_entity,
      message: "invalid parameters provided",
      params_errors: nil

    # We can improve the error message by providing
    # the error messages from the changeset.
    #def exception(_opts) do
    #  params_errors = Keyword.fetch!(opts, :params_errors)
    #  %InvalidParamsError{
    #    message: "invalid parameters provided"
    #  }
    #end

    # Handle InvalidParamsError as 422.
    defimpl Plug.Exception, for: InvalidParamsError do
      def status(_exception), do: 422
    end

  end

  @doc """
  Validate params based on rules function. This function will raise
  `InvalidParamsError` when changeset test fails.

  `rules` is a Params definition. See: https://github.com/vic/params
  """
  def validate(params, rules) do
    changeset = rules.(params)
    cond do
      changeset.valid? ->
        Params.data changeset
      true ->
        raise InvalidParamsError
    end
  end

end
