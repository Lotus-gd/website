import aiohttp
from web import templates # type: ignore
from aiohttp_session import get_session
from common import userhelper # type: ignore

async def render_template(r, template, *args, **kwargs) -> aiohttp.web.Response:
    
    # This is not needed as we can just add .html to all
    #if not template.endswith(".html"):
    #    template += ".html"  # make sure we have .html always at the end or else the server will break.
    
    session = await get_session(r)
    user = None
    if session.get("user_id") and session.get("logged_in"):
        user = await userhelper.get_user(session.get("user_id"))
    text = templates.get_template(template).render(*args, **kwargs, session=session, user=user)
    return aiohttp.web.Response(text=text, content_type="text/html")

def text(_text, **kwargs) -> aiohttp.web.Response:
    return aiohttp.web.Response(text=_text, **kwargs)