import pytest

from pyle38.errors import Tile38IdNotFoundError, Tile38KeyNotFoundError

from .helper.random_data import random_latitude, random_longitude, random_string


@pytest.mark.asyncio
async def test_command_pdel(tile38):
    key = random_string()
    id = random_string()
    lat = random_latitude()
    lon = random_longitude()

    pdel_pattern = f"{id[0:3]}*"

    response = await tile38.set(key, id).point(lat, lon).exec()
    assert response.ok

    response = await tile38.get(key, id).asObject()
    assert response.ok
    assert response.object["type"] == "Point"

    response = await tile38.pdel(key, pdel_pattern)
    assert response.ok

    # key drops because only id deleted
    with pytest.raises(Tile38KeyNotFoundError):
        await tile38.get(key, id).asObject()

    # key stays because only one id is deleted
    await tile38.set(key, id).point(lat, lon).exec()
    await tile38.set(key, random_string()).point(lat, lon).exec()

    await tile38.pdel(key, pdel_pattern)

    with pytest.raises(Tile38IdNotFoundError):
        await tile38.get(key, id).asObject()
