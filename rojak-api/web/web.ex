defmodule RojakAPI.Web do
  @moduledoc """
  A module that keeps using definitions for controllers,
  views and so on.

  This can be used in your application as:

      use RojakAPI.Web, :controller
      use RojakAPI.Web, :view

  The definitions below will be executed for every view,
  controller, etc, so keep them short and clean, focused
  on imports, uses and aliases.

  Do NOT define functions inside the quoted expressions
  below.
  """

  def controller do
    quote do
      use Phoenix.Controller, namespace: RojakAPI

      use Params
      import Ecto.Changeset

      import RojakAPI.Router.Helpers
      import RojakAPI.Gettext

      alias RojakAPI.ParamsValidator
    end
  end

  def view do
    quote do
      use Phoenix.View, root: "web/templates", namespace: RojakAPI

      import RojakAPI.Router.Helpers
      import RojakAPI.ErrorHelpers
      import RojakAPI.Gettext
    end
  end

  def router do
    quote do
      use Phoenix.Router
    end
  end

  def channel do
    quote do
      use Phoenix.Channel

      alias RojakAPI.Repo
      import Ecto
      import Ecto.Query
      import RojakAPI.Gettext
    end
  end

  @doc """
  When used, dispatch to the appropriate controller/view/etc.
  """
  defmacro __using__(which) when is_atom(which) do
    apply(__MODULE__, which, [])
  end
end
