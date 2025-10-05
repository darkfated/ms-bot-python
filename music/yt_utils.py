import yt_dlp, asyncio, logging
logger = logging.getLogger(__name__)

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': False,
    'quiet': True,
    'ignoreerrors': True,
    'default_search': 'auto',
    'nocheckcertificate': True,
    'retries': 3,
}

class YTDLSource:
    def __init__(self, title: str, url: str, webpage_url: str, duration: float | None):
        self.title = title
        self.url = url
        self.webpage_url = webpage_url
        self.duration = duration

    @classmethod
    async def create_source(cls, search: str, *, loop: asyncio.AbstractEventLoop | None = None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: cls._extract_info(search))
        if data is None:
            return None
        return cls(title=data['title'], url=data['url'], webpage_url=data.get('webpage_url'), duration=data.get('duration'))

    @staticmethod
    def _extract_info(search: str):
        try:
            with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
                info = ydl.extract_info(search, download=False)
        except Exception as e:
            logger.exception("yt_dlp failed for %s: %s", search, e)
            return None

        if info is None:
            return None

        if 'entries' in info:
            entries = [e for e in info['entries'] if e]
            if not entries:
                return None
            info = entries[0]

        formats = info.get('formats') or []
        audio_url = None
        for f in formats:
            if f.get('acodec') != 'none' and f.get('url'):
                audio_url = f.get('url')
                break

        if audio_url is None:
            audio_url = info.get('url')

        if audio_url is None:
            logger.warning("No audio URL for %s", search)
            return None

        return {'title': info.get('title'), 'url': audio_url, 'webpage_url': info.get('webpage_url'), 'duration': info.get('duration')}
