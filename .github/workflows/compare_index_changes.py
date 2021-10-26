import sys
import json
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
        if module_name not in old_modules:
            continue

        new_module = new_modules[module_name]
        old_module = old_modules[module_name]

        # Handled by another GH Action
        if "version" not in new_module:
            continue
        if "commit" not in new_module:
            continue
        if "version" not in old_module:
            continue
        if "commit" not in old_module:
            continue

        if new_module["version"] != old_module["version"]:
            if new_module["commit"] == old_module["commit"]:
                print("Error: Attribute 'version' was changed, but not 'commit'; in module '%s'" % module_name)
                sys.exit(1)

        if new_module["commit"] != old_module["commit"]:
            if new_module["version"] == old_module["commit"]:
                print("Error: Attribute 'commit' was changed but not 'version'; in module '%s'" % module_name)
                sys.exit(1)


if __name__ == "__main__":
    main()
