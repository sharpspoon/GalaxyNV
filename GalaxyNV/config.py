import os
import logging
import shutil
import errno
import pathlib
import zipfile
import jinja2 as jinja
import werkzeug.utils

PATH = os.path.dirname(__file__)
INFRASTRUCTURE_PATH = os.path.join(PATH, "..", "infrastructure")
IMAGE_PATH = os.path.join(INFRASTRUCTURE_PATH, "images")


def create_path(filepath):
    """ Recursively creates path. """

    path = os.path.split(filepath)[0]
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def copy_recursive(src, dst):
    """Utility function that copies directories and files recursively. """
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


def convert_string(input_string):
    """Parses space delimited string into a comma
    delimited string surrounded by brackets.
    """

    return '["' + '", "'.join(input_string.split()) + '"]'


def build_config(filepath, parent, parent_server, postbuilds, prebuilds):
    filepath = os.path.join(filepath, "config.yml")
    with open(os.path.join(PATH, "templates", "config_template.j2")) as file_:
        template = jinja.Template(file_.read())

    if prebuilds:
        prebuilds = (
            prebuilds.split("\n") if isinstance(prebuilds, str) else prebuilds
        )

    if postbuilds:
        postbuilds = (
            postbuilds.split("\n")
            if isinstance(postbuilds, str)
            else postbuilds
        )

    postbuilds = [convert_string(x) for x in postbuilds if x]
    prebuilds = [convert_string(x) for x in prebuilds if x]
    t = template.render(
        parent=parent,
        parentServer=parent_server,
        postBuilds=postbuilds,
        preBuilds=prebuilds,
    )

    create_path(filepath)
    with open(filepath, "w") as file:
        file.write(t)
    logging.debug(t)


def build_image(
    path,
    parent,
    parent_server=None,
    postbuilds=None,
    prebuilds=None,
    overlay=None,
):
    """Takes in parameters to build an image that galaxy can read."""

    build_config(path, parent, parent_server, postbuilds, prebuilds)
    # build_overlay(path, overlay)


def build_overlay(image_path, file=None):
    """Takes in a path and a zipfile to build an overlay
    for base and node images. If the passed file is not a zipfile or
    the filename is empty nothing will happen.

    Otherwise it will save the zipfile, then extract it, and the remove the
    original zip archive.
    """

    filename = werkzeug.utils.secure_filename(file.filename)
    if filename != "":
        overlay_path = os.path.join(image_path, filename)
        file.save(overlay_path)
        if zipfile.is_zipfile(overlay_path):
            with zipfile.ZipFile(overlay_path, "r") as zip_ref:
                zip_ref.extractall(image_path)

        os.remove(overlay_path)
