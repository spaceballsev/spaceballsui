import can
import pytest
import websockets

@pytest.mark.asyncio
async def test_soc(can_server):
    msg = can.Message(
        arbitration_id=0x355,
        data=[0x3C, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
        is_extended_id=False)

    res = await can_server.web_socket_server.can_processor.handle_message(msg)
    assert res['value'] == 60

@pytest.mark.asyncio
async def test_charge(can_server):
    msg = can.Message(
        arbitration_id=0x389,
        data=[0xB0, 0xEB, 0x3C, 0x3D, 0x45, 0xCA, 0x5F, 0x3C],
        is_extended_id=False)

    res = await can_server.web_socket_server.can_processor.handle_message(msg)
    assert res['value'] == 6

@pytest.mark.asyncio
async def test_charge(can_server):
    msg = can.Message(
        arbitration_id=0x38A,
        data=[0x60, 0x50, 0x10, 0x3D, 0x45, 0xCA, 0x5F, 0x3C],
        is_extended_id=False)

    res = await can_server.web_socket_server.can_processor.handle_message(msg)
    assert res['value'] == 96


@pytest.mark.asyncio
async def test_charge(can_server):
    msg = can.Message(
        arbitration_id=0x38B,
        data=[0x60, 0x50, 0x10, 0x3D, 0x45, 0xCA, 0x5F, 0x3C],
        is_extended_id=False)

    res = await can_server.web_socket_server.can_processor.handle_message(msg)
    assert res['value'] == 80
