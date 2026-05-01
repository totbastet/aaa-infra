import abc
import httpx
import asyncio


class ResultsObserver(abc.ABC):
    @abc.abstractmethod
    def observe(self, data: bytes) -> None: ...


async def do_reliable_request(url: str, observer: ResultsObserver)  -> None:
    timeout = httpx.Timeout(10.0, connect=5.0)
    delay = 1.0
    async with httpx.AsyncClient(timeout=timeout) as client:
        while True:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.read()
                observer.observe(data)
                return
            except httpx.HTTPError:
                await asyncio.sleep(delay)
                delay = min(delay * 2, 30)
