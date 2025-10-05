def user_in_voice(ctx) -> bool:
    return getattr(ctx.author, "voice", None) is not None and getattr(ctx.author.voice, "channel", None) is not None
