# Драйвер источника питания

## Сборка окружения

Для управления зависимостями используется Poetry(https://python-poetry.org/docs/)
```commandline
poetry install --no-root
```
Драйвер при запуске будет пытаться создать TCP соединение с параметрами:
```commandline
POWER_SUPPLY_HOST: 127.0.0.1
POWER_SUPPLY_PORT: 8888
```
Запуск Драйвера:
```commandline
uvicorn main:app --reload
```
Доки от FastAPI:
http://127.0.0.1:8000/docs

Сервер для отладки:
```commandline
import asyncio


async def handle_echo(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode().strip()
        print(message)
        if message == 'close':
            await writer.wait_closed()
            break
        response = '10 20 30'
        if message == ':SOURce1:CURRent 2':
            response = 'CURRent: Ok'
        elif message == ':SOURce1:VOLTage 5':
            response = 'VOLTage: Ok'
        elif message == ':OUTPUT1:STATe ON':
            response = 'OUTPUT1: Ok'
        elif message == ':OUTPut1:STATe OFF':
            response = 'OUTPUT1OFF: Ok'
        elif message == ':OUTPut2:STATe OFF':
            response = 'OUTPUT2OFF: Ok'
        elif message == ':OUTPut3:STATe OFF':
            response = 'OUTPUT3OFF: Ok'

        writer.write(response.encode())
        await writer.drain()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()


asyncio.run(main())

```