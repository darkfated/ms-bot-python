import asyncio
import logging
import discord
from discord import FFmpegPCMAudio

logger = logging.getLogger(__name__)

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}


class MusicPlayer:
    def __init__(self, bot, guild_id: int):
        self.bot = bot
        self.guild_id = guild_id

        self.queue: asyncio.Queue = asyncio.Queue()
        self.current = None

        self.repeat = False

        self.situations: dict[str, list] = {}
        self.situation_active: str | None = None

        self._connected_event = asyncio.Event()
        self._next_event = asyncio.Event()
        self._lock = asyncio.Lock()

        self._audio = None
        self._skip_flag = False

        self._task = self.bot.loop.create_task(self._loop())

    async def _loop(self):
        await self.bot.wait_until_ready()

        while True:
            source = await self.queue.get()

            async with self._lock:
                self.current = source
                self._next_event.clear()
                self._skip_flag = False

            await self._connected_event.wait()

            vc = self._get_vc()
            if not vc or not vc.is_connected():
                await asyncio.sleep(1)
                continue

            await self._play(vc)

            try:
                await asyncio.wait_for(self._next_event.wait(), timeout=3600)
            except asyncio.TimeoutError:
                self._trigger_next()

            self._next_event.clear()

            if self.repeat and self.current and not self._skip_flag:
                await self._requeue_repeat()

            if self.queue.empty() and self.situation_active:
                for it in self.situations.get(self.situation_active, []):
                    await self.queue.put(it)

            self.current = None

    async def _play(self, vc):
        try:
            await self._kill_audio()

            self._audio = FFmpegPCMAudio(
                self.current.url,
                **FFMPEG_OPTIONS
            )

            def _after(_):
                self.bot.loop.call_soon_threadsafe(self._next_event.set)

            vc.play(self._audio, after=_after)

        except Exception:
            self._trigger_next()

    async def _kill_audio(self):
        try:
            if self._audio:
                self._audio.cleanup()
        except Exception:
            pass
        self._audio = None

    def skip(self):
        vc = self._get_vc()

        self._skip_flag = True

        try:
            if vc and vc.is_playing():
                vc.stop()
        except Exception:
            pass

        self._trigger_next()

    def pause(self):
        vc = self._get_vc()
        if vc and vc.is_playing():
            vc.pause()

    def resume(self):
        vc = self._get_vc()
        if vc and vc.is_paused():
            vc.resume()

    def stop_all(self):
        vc = self._get_vc()

        try:
            self.queue = asyncio.Queue()
        except Exception:
            pass

        try:
            if vc:
                vc.stop()
        except Exception:
            pass

        self.current = None
        self._trigger_next()

    async def join_voice(self, channel: discord.VoiceChannel):
        vc = channel.guild.voice_client

        if vc is None:
            await channel.connect()
        elif not vc.is_connected():
            await channel.connect()
        else:
            await vc.move_to(channel)

        self._connected_event.set()

    def _get_vc(self):
        guild = self.bot.get_guild(self.guild_id)
        return guild.voice_client if guild else None

    def _trigger_next(self):
        self.bot.loop.call_soon_threadsafe(self._next_event.set)

    async def _requeue_repeat(self):
        try:
            tmp = []

            while not self.queue.empty():
                tmp.append(self.queue.get_nowait())

            await self.queue.put(self.current)

            for it in tmp:
                await self.queue.put(it)

        except Exception:
            await self.queue.put(self.current)

    async def start_situation(self, name: str):
        name = name.strip().lower()

        if name not in self.situations:
            return False

        async with self._lock:
            while not self.queue.empty():
                self.queue.get_nowait()

            for it in self.situations[name]:
                await self.queue.put(it)

            self.situation_active = name

        return True

    async def stop_situation(self):
        async with self._lock:
            while not self.queue.empty():
                self.queue.get_nowait()

            self.situation_active = None

        return True

    async def create_situation(self, name: str) -> bool:
        name = name.strip().lower()
        if not name or name in self.situations:
            return False
        self.situations[name] = []
        return True

    async def add_to_situation(self, name: str, source) -> bool:
        name = name.strip().lower()
        if name not in self.situations:
            return False
        self.situations[name].append(source)
        return True
