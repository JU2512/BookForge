def validate_css(manifest):

    css_files = []

    for item in manifest:

        if item["media_type"] == "text/css":

            css_files.append(item)

    if len(css_files) == 0:

        return {

            "module":"CSS",

            "status":"ERROR",

            "checks":[

                {

                    "status":"ERROR",

                    "message":"No CSS stylesheet found."

                }

            ]

        }

    return {

        "module":"CSS",

        "status":"PASS",

        "checks":[

            {

                "status":"PASS",

                "message":f"{len(css_files)} CSS file(s) found.",

                "files":css_files

            }

        ]

    }

def validate_images(manifest):

    image_files = []

    for item in manifest:

        if item["media_type"].startswith("image/"):

            image_files.append(item)

    if len(image_files) == 0:

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