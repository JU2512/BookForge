def resolve_spine(manifest, spine):

    manifest_lookup = {}

    for item in manifest:

        manifest_lookup[item["id"]] = item["href"]

    reading_order = []

    for chapter in spine:

        if chapter in manifest_lookup:

            reading_order.append({

                "id": chapter,

                "file": manifest_lookup[chapter]

            })

    return reading_order