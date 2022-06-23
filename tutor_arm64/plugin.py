from glob import glob
import os
import pkg_resources

from tutor import hooks
from tutor.__about__ import __version_suffix__ as tutor_version_suffix

from .__about__ import __version__

# We currently do not have a CI pipeline set up to build an ARM image for every
# new Tutor release automatically, so for now we have to settle for grabbing the
# latest image of the right type (either nightly or regular)
DOCKER_IMAGE_TAG = tutor_version_suffix or "latest"

################# Configuration
config = {
    "defaults": {
        "VERSION": __version__,
    },
    "unique": {
    },
    # Danger zone! Values here will override settings from Tutor core or other plugins.
    "overrides": {
        # The default MySQL 5.7 doesn't have an ARM image, so we need to use MySQL 8.
        # Note: For Maple and earlier, MySQL 8 won't work so "mariadb:10.4" can be used; it also has ARM support.
        # If you are upgrading from a previous version of this plugin which used mariadb, you may need to override this
        # setting to use "mariadb:10.4" so that you'll still have the same MySQL data.
        "DOCKER_IMAGE_MYSQL": "mysql:8.0-oracle",
        # The official overhang.io docker repo doesn't have arm64 images so we
        # need to use a separate repo that's related to this plugin, which does:
        "DOCKER_IMAGE_OPENEDX": "docker.io/opencraft/openedx-arm64:" + DOCKER_IMAGE_TAG,
        "DOCKER_IMAGE_OPENEDX_DEV": "docker.io/opencraft/openedx-arm64:" + DOCKER_IMAGE_TAG,
        "DOCKER_IMAGE_PERMISSIONS": "docker.io/opencraft/openedx-permissions-arm64:" + DOCKER_IMAGE_TAG,
    },
}


################# You don't really have to bother about what's below this line,
################# except maybe for educational purposes :)

# Plugin templates
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutor_arm64", "templates")
)
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("arm64/build", "plugins"),
        ("arm64/apps", "plugins"),
    ],
)
# Load all patches from the "patches" folder
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutor_arm64", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

# Load all configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"ARM64_{key}", value)
        for key, value in config["defaults"].items()
    ]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"ARM64_{key}", value)
        for key, value in config["unique"].items()
    ]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))
