import sys
import json
import requests
from collections import OrderedDict


def main():
    try:
        with open("cfbs.json", "r") as f:
            new_index = json.loads(f.read(), object_pairs_hook=OrderedDict)
        with open("cfbs.old.json", "r") as f:
            old_index = json.loads(f.read(), object_pairs_hook=OrderedDict)
        compare_index_changes(new_index, old_index)
    except Exception as e:
        print(e)
        sys.exit(1)
    sys.exit(0)


def compare_index_changes(new_index, old_index):
    assert "index" in new_index
    new_modules = new_index["index"]

    assert "index" in old_index
    old_modules = old_index["index"]

    for module_name in new_modules:
        new_module = new_modules[module_name]
        old_module = old_modules.get(module_name)

        # Resolve any aliases
        if "alias" in new_module:
            new_module = new_modules[new_module["alias"]]
        if old_module and "alias" in old_module:
            old_module = old_modules[old_module["alias"]]

        # Any remote resources must be reachable
        validate_reachable_resources(new_module, old_module, module_name)

        if old_module:
            # If either version or commit is changed, then both must be changed
            validate_version_and_commit(new_module, old_module, module_name)


def validate_version_and_commit(new_module, old_module, module_name):
    if new_module.get("version") != old_module.get("version"):
        if new_module.get("commit") == old_module.get("commit"):
            print(
                "Error: Attribute 'version' was changed, but not 'commit'; in module '%s'"
                % module_name
            )
            sys.exit(1)

    if new_module.get("commit") != old_module.get("commit"):
        if new_module.get("version") == old_module.get("version"):
            print(
                "Error: Attribute 'commit' was changed but not 'version'; in module '%s'"
                % module_name
            )
            sys.exit(1)


def validate_reachable_resources(new_module, old_module, module_name):
    # To save bandwidth we only HEAD request on changes to an URL
    def _head(url):
        response = requests.head(url)
        if not response.ok:
            print(
                f"Error: remote resource '{url}' in module '{module_name}' is not reachable"
            )
            sys.exit(1)

    if (
        not old_module
        or new_module.get("repo") != old_module.get("repo")
        or new_module.get("commit") != old_module.get("commit")
        or new_module.get("subdirectory") != old_module.get("subdirectory")
    ):
        assert "repo" in new_module, "Missing required attribute 'repo' in module {}".format(module_name)
        assert "commit" in new_module, "Missing required attribute 'commit' in module {}".format(module_name)
        url = new_module["repo"]
        commit = new_module["commit"]
        subdir = new_module.get("subdirectory")

        if url.startswith("https://github.com"):
            url += f"/tree/{commit}"
            if subdir:
                url += f"/{subdir}"
        elif url.startswith("https://gitlab.com"):
            url += f"/-/tree/{commit}"
            if subdir:
                url += f"/{subdir}"

        _head(url)

    if "documentation" in new_module and (
        not old_module
        or new_module.get("documentation") != old_module.get("documentation")
    ):
        _head(new_module["documentation"])

    if "website" in new_module and (
        not old_module or new_module.get("website") != old_module.get("website")
    ):
        _head(new_module["website"])


if __name__ == "__main__":
    main()
