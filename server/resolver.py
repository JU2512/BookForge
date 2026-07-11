def resolve_spine(manifest, spine):
    """
    Resolve the EPUB spine into the reading order.

    Matches spine item IDs with manifest entries and returns
    the ordered list of chapter files.
    """

    if not manifest or not spine:
        return []

    manifest_lookup = {}

    for item in manifest:

        if not isinstance(item, dict):
            continue

        item_id = item.get("id")
        href = item.get("href")

        if item_id and href:
            manifest_lookup[item_id] = href

    reading_order = []

    for chapter in spine:

        if chapter in manifest_lookup:

            reading_order.append({
                "id": chapter,
                "file": manifest_lookup[chapter]
            })

    return reading_order