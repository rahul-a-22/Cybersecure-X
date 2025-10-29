# app/routers/network_tools.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from app.utils import subnet_tools

router = APIRouter(prefix="/network-tools", tags=["network-tools"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/ui")
def network_ui(request: Request):
    return templates.TemplateResponse("network.html", {"request": request})


@router.post("/api/subnet")
async def api_subnet(payload: dict):
    try:
        network_ip = payload.get("network_ip")
        current_prefix = int(payload.get("current_prefix"))
        new_prefix = int(payload.get("new_prefix"))
        return subnet_tools.subnetting(network_ip, current_prefix, new_prefix)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/supernet")
async def api_supernet(payload: dict):
    try:
        raw = payload.get("networks", None)
        # Accept either a single string (comma separated) or a list
        items = []
        if raw is None:
            raise ValueError("No networks provided")
        if isinstance(raw, str):
            # split by comma or newline
            items = [s.strip() for s in raw.replace("\n", ",").split(",") if s.strip()]
        elif isinstance(raw, list):
            items = [str(s).strip() for s in raw if str(s).strip()]
        else:
            raise ValueError("Invalid networks format. Provide comma-separated string or array.")

        if not items:
            raise ValueError("No valid network entries found")

        result = subnet_tools.supernetting(items)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/supernet/minimal")
async def api_supernet_minimal(payload: dict):
    try:
        raw = payload.get("networks", [])
        # accept string or list (same parsing used earlier)
        if isinstance(raw, str):
            items = [s.strip() for s in raw.replace("\n", ",").split(",") if s.strip()]
        elif isinstance(raw, list):
            items = [str(s).strip() for s in raw if str(s).strip()]
        else:
            raise ValueError("Invalid networks input")

        if not items:
            raise ValueError("No networks provided")

        res = subnet_tools.minimal_cover_supernet(items)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/nextsubnet")
async def api_next_subnet(payload: dict):
    try:
        network_str = payload.get("network")
        return subnet_tools.next_subnet(network_str)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/reverse")
async def api_reverse_lookup(payload: dict):
    try:
        ip = payload.get("ip")
        return subnet_tools.reverse_lookup(ip)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
