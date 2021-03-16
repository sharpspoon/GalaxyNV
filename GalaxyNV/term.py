import os
import yaml
import config


def build_master_base():
    """Builds default master config file."""

    parent_server = "https://images.linuxcontainers.org"
    parent = "debian/stretch/amd64"
    prebuild = [
        "apt-get -yq update",
        "apt-get -yq install curl dnsutils git iptables iptables-persistent \
        iputils-ping netcat nmap openssh-client openssh-server python3 \
        python3-pip resolvconf rsyslog traceroute tshark ulogd2",
        "systemctl disable systemd-resolved",
        "iptables -I INPUT -s 10.0.0.0/8 -m state --state NEW,INVALID, \
        ESTABLISHED,RELATED -j NFLOG --nflog-prefix iptable_connections",
        "sh -c iptables-save > /etc/iptables/rules.v4",
    ]
    postbuild = [
        "pip3 install /opt/trollius",
        "pip3 install /opt/ceads-api",
        "pip3 install /opt/galaxy-api",
        "pip3 install py-spy",
        "sed -i s/nullok_secure/nullok/ /etc/pam.d/common-auth",
        "sed -i -E s/(#)?( )?PermitRootLogin prohibit-password/PermitRootLogin \
        yes/ /etc/ssh/sshd_config",
        "sed -i -E s/(#)?( )?PermitEmptyPasswords no/PermitEmptyPasswords yes/ \
        /etc/ssh/sshd_config",
        "passwd -d root",
        "update-rc.d drone defaults",
    ]
    config.build_image(
        os.path.join(config.IMAGE_PATH, "base", "master"),
        parent,
        parent_server,
        postbuild,
        prebuild,
    )


def build_base_images():
    """Requests information from standard input for building
    base images. Loops until user specifies they are done.
    """

    done = False

    while not done:
        parent = input("Parent: ")
        parent_server = input("Parent Server: ")

        prebuilds = []
        prebuild = input("Prebuild: ")
        while prebuild:
            prebuilds.append(prebuild)
            prebuild = input("Prebuild: ")

        postbuilds = []
        postbuild = input("Postbuild: ")
        while postbuild:
            postbuilds.append(postbuild)
            postbuild = input("Postbuild: ")

        filepath = input("File path: ")

        filepath = os.path.join(config.IMAGE_PATH, "base", filepath)

        config.build_image(
            filepath, parent, parent_server, postbuilds, prebuilds
        )

        isdone = input("Done? ")

        if "y" in isdone.lower():
            done = True


def build_node_images():
    """Requests information from standard input for building
    node images. Loops until user specifies they are done.
    """

    done = False
    nodes = {}
    while not done:
        provided_parent = False
        while not provided_parent:
            parent = input("Parent: ")
            if parent:
                provided_parent = True

        filepath = input("File path: ")
        node_name = filepath
        filepath = os.path.join(config.INFRASTRUCTURE_PATH, "nodes", filepath)
        config.build_image(filepath, parent)

        nodes[node_name] = get_net_info_for_node(node_name)
        isdone = input("Done? ")

        if "y" in isdone.lower():
            done = True
    return nodes


def get_net_info_for_node(node_name):
    """Requests information from standard input for building
    network information. Appends to node dictionary which is used later.
    """

    cur_node = {}

    # image
    cur_node["image"] = node_name

    # type
    node_type = input("Type [LXD]: ")
    if not node_type:
        node_type = "lxd"
    else:
        node_type = node_type.lower()
    cur_node["type"] = node_type

    # priority
    no_num = True
    while no_num:
        node_priority = input("Priority [0]: ")
        if not node_priority:
            node_priority = 0
            no_num = False
        elif node_priority.isalpha():
            node_priority = str(node_priority)
            no_num = False
    cur_node["priority"] = node_priority

    # links
    done = False
    cur_node["links"] = []
    while not done:
        link = input("Link: ")
        cur_node["links"].append(link)

        is_done = input("Done? ")
        if "y" in is_done.lower():
            done = True

    # agents
    done = False
    cur_node["agent"] = []
    while not done:
        node_agent = input("Agent: ")
        cur_node["agent"].append(node_agent)
        is_done = input("Done? ")

    if "y" in is_done.lower():
        done = True
    return cur_node


def build_network_config(nodes):
    """Using the node dictionary created earlier
    generate network config.
    """

    done = False
    links = {}
    while not done:
        link = input("Link: ")
        links[link] = {}
        cur_link = links[link]

        link_type = input("Type [LXD]: ")
        link_type = "lxd" if not link_type else link_type.lower()
        cur_link["type"] = link_type

        is_done = input("Done? ")
        if "y" in is_done.lower():
            done = True
    network_config = {}
    network_config["nodes"] = nodes
    network_config["links"] = links

    with open(
        os.path.join(config.INFRASTRUCTURE_PATH, "network.yml"), "+w"
    ) as file:
        file.write(yaml.dump(network_config))


def create():
    """Populates infrastructure with configuration
    files via terminal input.
    """

    build_master_base()
    build_base_images()
    network_for_nodes = build_node_images()
    build_network_config(network_for_nodes)


if __name__ == "__main__":
    create()
