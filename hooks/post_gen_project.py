import os
import shutil
import yaml
import logging

MANIFEST = "manifest.yml"


def delete_resources_for_disabled_features():
    with open(MANIFEST) as manifest_file:
        manifest = yaml.load(manifest_file, Loader=yaml.SafeLoader)
        for feature in manifest["features"]:
            if not feature["enabled"]:
                logging.info("Removing resources for disabled feature %s .", feature["name"])
                for resource in feature["resources"]:
                    delete_resource(resource)
    logging.info("Cleanup complete, removing manifest.")
    delete_resource(MANIFEST)


def delete_resource(resource):
    if os.path.isfile(resource):
        logging.info("Removing file: %s", resource)
        os.remove(resource)
    elif os.path.isdir(resource):
        logging.info("Removing directory: %s", resource)
        shutil.rmtree(resource)


if __name__ == "__main__":
    delete_resources_for_disabled_features()
