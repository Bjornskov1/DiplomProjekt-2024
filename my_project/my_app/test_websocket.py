import asyncio
import websockets

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/meetings/moderum_1/"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")
            # Læs beskeder fra WebSocket (tilføj, hvis serveren sender noget)
            async for message in websocket:
                print(f"Message received: {message}")
    except Exception as e:
        print(f"Failed to connect: {e}")

asyncio.run(test_websocket())