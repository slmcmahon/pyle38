import pytest

from pyle38.commands.within import Within

key = "fleet"
id = "truck"
feature = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [13.37, 52.25]},
    "properties": {"id": id},
}
polygon = {
    "type": "Polygon",
    "coordinates": [
        [
            [13.361263275146484, 52.24630137198303],
            [13.379974365234373, 52.24630137198303],
            [13.379974365234373, 52.256705331409506],
            [13.361263275146484, 52.256705331409506],
            [13.361263275146484, 52.24630137198303],
        ]
    ],
}

expected = {"id": id, "object": feature}


@pytest.mark.parametrize(
    "format, precision, expected",
    [
        (
            "OBJECTS",
            None,
            [
                "WITHIN",
                [
                    key,
                    "MATCH",
                    "*",
                    "NOFIELDS",
                    "CURSOR",
                    0,
                    "LIMIT",
                    10,
                    "FENCE",
                    "DETECT",
                    "enter,exit",
                    "COMMANDS",
                    "del,set",
                    "CIRCLE",
                    1.0,
                    1.0,
                    100,
                ],
            ],
        )
    ],
    ids=["OBJECTS"],
)
@pytest.mark.asyncio
async def test_command_within_compile(tile38, format, precision, expected):
    query = (
        Within(tile38.client, key)
        .match("*")
        .nofields()
        .cursor(0)
        .limit(10)
        .fence()
        .detect(["enter", "exit"])
        .commands(["del", "set"])
        .circle(1, 1, 100)
    )

    received = query.output(format, precision).compile()

    assert expected == received


@pytest.mark.asyncio
async def test_command_within_circle(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.within(key).circle(52.25, 13.37, 100).asObjects()
    assert response.ok
    assert response.objects[0].dict() == expected


@pytest.mark.asyncio
async def test_command_within_object(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = (
        await tile38.within(key)
        .object(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [13.361263275146484, 52.24630137198303],
                        [13.379974365234373, 52.24630137198303],
                        [13.379974365234373, 52.256705331409506],
                        [13.361263275146484, 52.256705331409506],
                        [13.361263275146484, 52.24630137198303],
                    ]
                ],
            }
        )
        .asObjects()
    )

    assert response.ok
    assert response.objects[0].dict() == expected


@pytest.mark.asyncio
async def test_command_within_hash(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.within(key).hash("u3390").asObjects()
    assert response.ok
    assert response.objects[0].dict() == expected


@pytest.mark.asyncio
async def test_command_within_quadkey(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.within(key).quadkey("120").asObjects()
    assert response.ok
    assert response.objects[0].dict() == expected


@pytest.mark.asyncio
async def test_command_within_tile(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.within(key).tile(2200, 1348, 12).asObjects()
    assert response.ok
    assert response.objects[0].dict() == expected


@pytest.mark.asyncio
async def test_command_within_bounds(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.within(key).bounds(52.24, 13.36, 52.256, 13.379).asObjects()
    assert response.ok
    assert response.objects[0].dict() == expected


@pytest.mark.asyncio
async def test_command_within_get(tile38):
    response = await tile38.set(key, id).object(feature).exec()
    assert response.ok

    response = await tile38.set("zones", "zone").object(polygon).exec()
    assert response.ok

    response = await tile38.within(key).get("zones", "zone").asObjects()
    assert response.ok
    assert response.objects[0].dict() == expected