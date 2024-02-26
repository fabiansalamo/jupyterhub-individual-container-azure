# Configuration file for JupyterHub
import os
import re
import unicodedata
from oauthenticator.azuread import AzureAdOAuthenticator

c = get_config()  # noqa: F821

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# custom authentication 
class NormalizedUsernameLocalAzureAdOAuthenticator(AzureAdOAuthenticator):

    def normalize_username(self, username):
        username = username.lower()[0:32]
        username = unicodedata.normalize('NFD', username).encode('ascii','ignore').decode("utf-8")
        username = re.sub(r'\W+', '', username)
        return username

c.JupyterHub.authenticator_class = NormalizedUsernameLocalAzureAdOAuthenticator
c.Authenticator.admin_users = "[]"
c.Authenticator.allowed_users = "[]"

# custom config
c.DockerSpawner.port = 5001

# ssl
c.JupyterHub.ssl_key = '/etc/letsencrypt/live/[]/privkey.pem'
c.JupyterHub.ssl_cert = '/etc/letsencrypt/live/[]/fullchain.pem'

# Azure AD
c.AzureAdOAuthenticator.tenant_id = "[]"
c.AzureAdOAuthenticator.client_id = "[]"
c.AzureAdOAuthenticator.client_secret = "[]"
c.AzureAdOAuthenticator.oauth_callback_url = "https://[]/hub/oauth_callback"
c.AzureAdOAuthenticator.allow_existing_users = False
