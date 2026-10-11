"""Resolve published STAC objects through the PySTAC SDK."""

from pathlib import Path

import click
import pystac


def read_item(href: str) -> pystac.Item:
    path = Path(href)
    document = pystac.read_file(str(path / "catalog.json") if path.is_dir() else href)
    if isinstance(document, pystac.Item):
        return document
    if isinstance(document, pystac.Catalog):
        item = next(document.get_all_items(), None)
        if item is not None:
            return item
    raise click.ClickException("Input must be a STAC Item or catalog containing an Item")


def asset_href(asset: pystac.Asset) -> str:
    href = asset.get_absolute_href()
    if href is None:
        raise click.ClickException("STAC asset has no resolvable href")
    return href
