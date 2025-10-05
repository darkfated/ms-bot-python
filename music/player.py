import asyncio, logging
import discord
from discord import FFmpegPCMAudio

logger = logging.getLogger(__name__)
FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}

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
        self._task = self.bot.loop.create_task(self._loop())

    async def _loop(self):
        await self.bot.wait_until_ready()
        while True:
            try:
                source = await self.queue.get()
            except asyncio.CancelledError:
                break
            self.current = source
            await self._connected_event.wait()
            guild = self.bot.get_guild(self.guild_id)
            if guild is None:
                self.current = None
                continue
            vc = guild.voice_client
            if vc is None or not vc.is_connected():
                self.current = None
                continue
            try:
                audio = FFmpegPCMAudio(self.current.url, **FFMPEG_OPTIONS)
                vc.play(audio, after=lambda e: self.bot.loop.call_soon_threadsafe(self._next_event.set))
            except Exception:
                self._next_event.set()
            await self._next_event.wait()
            self._next_event.clear()

            if self.repeat and self.current:
                try:
                    tmp = []
                    while not self.queue.empty():
                        tmp.append(self.queue.get_nowait())
                    await self.queue.put(self.current)
                    for it in tmp:
                        await self.queue.put(it)
                except Exception:
                    await self.queue.put(self.current)

            if self.queue.empty() and self.situation_active:
                items = self.situations.get(self.situation_active, [])
                if items:
                    for it in items:
                        await self.queue.put(it)

            self.current = None

    async def join_voice(self, channel: discord.VoiceChannel):
        try:
            if channel.guild.voice_client is None:
                await channel.connect()
            else:
                vc = channel.guild.voice_client
                if not vc.is_connected():
                    await vc.connect()
                else:
                    await vc.move_to(channel)
            self._connected_event.set()
        except Exception:
            raise

    async def stop(self):
        try:
            while not self.queue.empty():
                self.queue.get_nowait()
        except Exception:
            pass
        guild = self.bot.get_guild(self.guild_id)
        if guild and guild.voice_client:
            try:
                if guild.voice_client.is_playing():
                    guild.voice_client.stop()
            except Exception:
                pass
            try:
                await guild.voice_client.disconnect()
            except Exception:
                pass
        self._connected_event.clear()
        self.situation_active = None

    def pause(self):
        guild = self.bot.get_guild(self.guild_id)
        if guild and guild.voice_client and guild.voice_client.is_playing():
            try:
                guild.voice_client.pause()
            except Exception:
                pass

    def resume(self):
        guild = self.bot.get_guild(self.guild_id)
        if guild and guild.voice_client and guild.voice_client.is_paused():
            try:
                guild.voice_client.resume()
            except Exception:
                pass

    def skip(self):
        guild = self.bot.get_guild(self.guild_id)
        if guild and guild.voice_client and guild.voice_client.is_playing():
            try:
                guild.voice_client.stop()
            except Exception:
                pass

    async def create_situation(self, name: str) -> bool:
        name = name.strip().lower()
        if not name:
            return False
        if name in self.situations:
            return False
        self.situations[name] = []
        return True

    def list_situations(self) -> list:
        return list(self.situations.keys())

    async def add_to_situation(self, name: str, source) -> bool:
        name = name.strip().lower()
        if name not in self.situations:
            return False
        self.situations[name].append(source)
        return True

    def get_situation_tracks(self, name: str) -> list:
        name = name.strip().lower()
        return self.situations.get(name, [])

    async def start_situation(self, name: str):
        name = name.strip().lower()
        if name not in self.situations:
            return False
        try:
            try:
                while not self.queue.empty():
                    self.queue.get_nowait()
            except Exception:
                pass
            for it in self.situations[name]:
                await self.queue.put(it)
            self.situation_active = name
            return True
        except Exception:
            return False

    async def stop_situation(self):
        self.situation_active = None
        try:
            while not self.queue.empty():
                self.queue.get_nowait()
        except Exception:
            pass
        return True

    async def delete_situation(self, name: str) -> bool:
        name = name.strip().lower()
        if not name:
            return False
        if name not in self.situations:
            return False
        try:
            if self.situation_active == name:
                self.situation_active = None
                try:
                    while not self.queue.empty():
                        self.queue.get_nowait()
                except Exception:
                    pass
            del self.situations[name]
            return True
        except Exception:
            return False
