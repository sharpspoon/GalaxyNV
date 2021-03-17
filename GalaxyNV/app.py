#! env python3

""" Flask App that handles infrastructure configuration creation for Galaxy """

import os
from flask.helpers import url_for
from waitress import serve
import flask
import yaml
from GalaxyNV import config


app = flask.Flask(__name__)

# Paths used throughout the app

PATH = os.getcwd()
INFRASTRUCTURE_PATH = os.path.join(PATH, "configuration", "infrastructure")
NETWORK_PATH = os.path.join(INFRASTRUCTURE_PATH, "network.yml")
IMAGE_PATH = os.path.join(INFRASTRUCTURE_PATH, "images")


#############
#   Routes  #
#############


@app.route("/", methods=["GET", "POST"])
def _index():
    """Default route.
    GET - returns index.html,
    POST - request GET creation.html a path as the parameter.
    """

    if flask.request.method == "GET":
        return flask.render_template("index.html")
    elif flask.request.method == "POST":
        return flask.redirect(
            flask.url_for(
                "_creation",
                path=_get_field("path_to_load"),
            )
        )


@app.route("/creation", methods=["GET", "POST"])
def _creation():
    """Route for /creation
    GET - returns a blank form to be filled out by the user if there is no get
    parameter. Otherwise use the parameter as a path to the template to fill
    out the form.

    POST - the form is sent to flask so the configuration files can be
    generated from it.
    """

    if flask.request.method == "GET":

        template_path = flask.request.args.get("path", "")
        if template_path.strip() == "":
            # if no parameter, meaning the user does not want a template
            return flask.render_template("creation.html")

        if _check_path(template_path):
            # if a template is set

            base = _get_images("base")
            node = _get_images("nodes")

            network_dict = yaml.load(open(NETWORK_PATH), yaml.SafeLoader)

            network = []
            for image in network_dict["nodes"].values():
                image["links"] = "\n".join(list(image["links"].keys()))
                image["agents"] = "\n".join(image["agents"])
                network.append(image)

            return flask.render_template(
                "creation.html", base=base, node=node, network=network
            )

        return flask.redirect(url_for("_index", error="path_not_found"))

    elif flask.request.method == "POST":
        # consume the form the user fills out & create the configuration files
        base_error = _parse_base_images()
        node_error = _parse_node_images()
        network_error = _parse_network_nodes()

        if base_error or node_error or network_error:
            result = "error"
        else:
            result = "success"
        return flask.render_template("creation.html", result=result)


#######################
#   Helper Functions  #
#######################


def _check_path(path):
    """Determines if path sent in exists and if it does reset path vars."""

    global INFRASTRUCTURE_PATH
    global NETWORK_PATH
    global IMAGE_PATH

    tmp_infrastructure_path = os.path.join(PATH, path)
    tmp_network_path = os.path.join(INFRASTRUCTURE_PATH, "network.yml")
    tmp_image_path = os.path.join(INFRASTRUCTURE_PATH, "images")

    if (
        os.path.exists(INFRASTRUCTURE_PATH)
        and os.path.exists(NETWORK_PATH)
        and os.path.exists(IMAGE_PATH)
    ):
        INFRASTRUCTURE_PATH = tmp_infrastructure_path
        NETWORK_PATH = tmp_network_path
        IMAGE_PATH = tmp_image_path
        return True
    return False


def _get_images(dir):
    """Creates a list of valid image dictionaries.

    This information is used to allow the website to load in templates.
    """

    def unwrap(nested_list):
        # flatten list of lists
        return "\n".join([" ".join(elements) for elements in nested_list])

    base_path = os.path.join(IMAGE_PATH)
    path = os.path.join(base_path, dir)
    images = []
    for current, _, files in os.walk(path):
        if "config.yml" in files:

            config = yaml.load(
                open(os.path.join(current, "config.yml")), yaml.SafeLoader
            )

            config["path"] = current.split(path)[-1][1:]
            if "prebuild" in config:
                config["prebuild"] = unwrap(config["prebuild"])
            if "postbuild" in config:
                config["postbuild"] = unwrap(config["postbuild"])

            files = []
            overlay_path = os.path.join(current, "overlay")
            for dir_path, _, filenames in os.walk(overlay_path):
                for file in filenames:
                    file_path = os.path.join(dir_path, file)
                    if os.path.isfile(file_path):
                        files.append(file_path)

            config["overlay"] = "\n".join(files)
            images.append(config)

    return images


def _parse_base_images():
    """Parses POST parameters relating to base images and build appropriate
    files.
    """

    for counter in range(int(flask.request.form["baseCounter"])):
        try:
            path = _get_field("base_path", counter)
            parent_server = _get_field("base_server", counter)
            parent = _get_field("base_parent", counter)
            prebuild = _get_field("base_prebuild", counter) + "\n"
            prebuild += "\n".join(_get_field("base_pre", counter, True))
            postbuild = _get_field("base_postbuild", counter) + "\n"
            postbuild += "\n".join(_get_field("base_post", counter, True))
            overlay = _get_field("base_overlay", counter)
            config.build_image(
                os.path.join(IMAGE_PATH, "base", path),
                parent,
                parent_server,
                postbuild,
                prebuild,
                overlay,
            )
        except (KeyError, OSError) as e:
            if e is OSError:
                return True
            continue
        return False


def _parse_node_images():
    """Parses POST parameters relating to node images and build appropriate
    files.
    """

    for counter in range(int(flask.request.form["nodeCounter"])):
        try:
            path = _get_field("node_path", counter)
            parent_server = _get_field("node_server", counter)
            parent = _get_field("node_parent", counter)
            prebuild = _get_field("node_prebuild", counter)
            postbuild = _get_field("node_postbuild", counter)
            overlay = _get_field("node_overlay", counter)
            config.build_image(
                os.path.join(IMAGE_PATH, "nodes", path),
                parent,
                parent_server,
                postbuild,
                prebuild,
                overlay,
            )
        except (KeyError, OSError) as e:
            if e is OSError:
                return True
            continue
    return False


def _parse_network_nodes():
    """Parses POST parameters relating to the network config and build the
    appropriate file."""

    def flatten_list(field, counter):
        values = _get_field(field, counter).split("\n")
        return [value.strip() for value in values]

    nodes = {}
    all_links = []
    for counter in range(int(flask.request.form["networkCounter"])):
        try:
            # get info for each network item and create a dictionary
            name = flask.request.form["network_name" + str(counter)]
            nodes[name] = {}
            current_node = nodes[name]

            current_node["image"] = name
            current_node["type"] = "lxd"

            current_node["priority"] = int(
                _get_field("network_range", counter)
            )

            replicas = _get_field("network_replicas", counter)
            if replicas:
                current_node["replicas"] = int(replicas)

            hostname = _get_field("network_hostname", counter)
            if hostname:
                current_node["hostname"] = hostname

            links = flatten_list("network_links", counter)
            current_node["links"] = {}
            for link in links:
                current_node["links"][link] = {}
            all_links.extend(links)

            agents = flatten_list("network_agents", counter)
            current_node["agents"] = agents

        except KeyError:
            continue

    network = _create_network_dict(nodes, all_links)
    try:
        config.create_path(NETWORK_PATH)
        with open(NETWORK_PATH, "+w") as file:
            file.write(
                yaml.dump(network, default_flow_style=False, sort_keys=False)
            )
    except OSError:
        return True
    return False


def _create_network_dict(nodes, links):
    """Sets up nodes and links for network file."""
    all_nodes = {}
    all_nodes["nodes"] = nodes
    all_nodes["links"] = {}
    for link in links:
        all_nodes["links"][link] = {}
        all_nodes["links"][link]["type"] = "lxd"
    return all_nodes


def _get_field(name, counter="", is_list=False):
    """Gets the passed field from the flask.request object."""

    if is_list:
        return flask.request.form.getlist(name + str(counter))
    return flask.request.form[name + str(counter)]


#############
#   Public  #
#############


def run():
    serve(app, port=5000)


DEBUG = False
if __name__ == "__main__":
    if DEBUG:
        app.run(port=5000, debug=True)
    else:
        serve(app, port=5000)
