import regex
import aiohttp
import utils # type: ignore
from aiohttp_session import get_session
from common.objects.account import Account # type: ignore

async def register(r: aiohttp.web.RequestHandler):
    return await utils.render_template(r, "register.html")

async def register_post(r: aiohttp.web.RequestHandler):
    session = await get_session(r)
    session["logged_in"] = False
    if session.get("logged_in"):
        return aiohttp.web.HTTPFound("/")
    
    data = await r.post()
    username = data["username"]
    password = data["password"]
    email = data["email"]
    
    if not regex.match(".{1,}@[^.]{1,}", email):
        return aiohttp.web.HTTPBadRequest(reason="invalid email")
    
    try:
        ip = r.headers["CF-Connecting-IP"]
    except KeyError:
        ip = "0.0.0.0"
    await Account.register(username, password, email, ip)
    
    return aiohttp.web.HTTPFound("/")