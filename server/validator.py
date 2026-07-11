"""
BookForge - CSS & Image Validator

This module validates the presence of CSS stylesheets and image files
declared in the EPUB manifest.

The functions are defensive and never assume the manifest is perfectly
formed, allowing malformed EPUBs to be analyzed without crashing.
"""


def validate_css(manifest):
    """
    Validate CSS files declared in the EPUB manifest.
    """

    css_files = []

    # Handle missing or invalid manifest
    if not manifest:
        return {
            "module": "CSS",
            "status": "ERROR",
            "checks": [
                {
                    "status": "ERROR",
                    "message": "Manifest is empty or could not be parsed."
                }
            ]
        }

    for item in manifest:

        # Ignore malformed manifest entries
        if not isinstance(item, dict):
            continue

        media_type = item.get("media_type", "")

        if media_type == "text/css":
            css_files.append(item)

    if not css_files:
        return {
            "module": "CSS",
            "status": "ERROR",
            "checks": [
                {
                    "status": "ERROR",
                    "message": "No CSS stylesheet found."
                }
            ]
        }

    return {
        "module": "CSS",
        "status": "PASS",
        "checks": [
            {
                "status": "PASS",
                "message": f"{len(css_files)} CSS file(s) found.",
                "files": css_files
            }
        ]
    }


def validate_images(manifest):
    """
    Validate image files declared in the EPUB manifest.
    """

    image_files = []

    # Handle missing or invalid manifest
    if not manifest:
        return {
            "module": "Images",
            "status": "ERROR",
            "checks": [
                {
                    "status": "ERROR",
                    "message": "Manifest is empty or could not be parsed."
                }
            ]
        }

    for item in manifest:

        # Ignore malformed manifest entries
        if not isinstance(item, dict):
            continue

        media_type = item.get("media_type", "")

        if media_type.startswith("image/"):
            image_files.append(item)

    if not image_files:
        return {
            "module": "Images",
            "status": "ERROR",
            "checks": [
                {
                    "status": "ERROR",
                    "message": "No images found."
                }
            ]
        }

    return {
        "module": "Images",
        "status": "PASS",
        "checks": [
            {
                "status": "PASS",
                "message": f"{len(image_files)} image(s) found.",
                "files": image_files
            }
        ]
    }