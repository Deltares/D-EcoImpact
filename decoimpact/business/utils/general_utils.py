from importlib.metadata import version


def read_version_number():
    """Reads the version of the tool

    Returns:
        str: version number of tool
    """
    version_string = version("decoimpact")
    return version_string
