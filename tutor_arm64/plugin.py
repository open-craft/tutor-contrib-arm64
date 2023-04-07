from glob import glob
import os
import pkg_resources

from tutor import hooks

from .__about__ import __version__

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
        "DOCKER_IMAGE_OPENEDX": "ghcr.io/open-craft/openedx-arm64:{{ TUTOR_VERSION }}",
        "DOCKER_IMAGE_OPENEDX_DEV": "ghcr.io/open-craft/openedx-arm64-dev:{{ TUTOR_VERSION }}",
        "DOCKER_IMAGE_PERMISSIONS": "ghcr.io/open-craft/openedx-permissions-arm64:{{ TUTOR_VERSION }}",
    },
}


@hooks.Filters.DOCKER_BUILD_COMMAND.add()
def modify_build_command(cmd_args: list[str]):
    """ Replace 'build' with 'buildx build'"""
    # cmd_args is e.g. ["build", "-t", "(tag)", ...]
    return ["buildx"] + cmd_args


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
