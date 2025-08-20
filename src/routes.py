import os

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .connection_manager import ConnectionManager
from .pkg_manager import PackageManager

script_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(script_dir, "templates"))
router = APIRouter()


@router.get("/")
async def root(request: Request):
    """
    Root endpoint that redirects to the connect page.
    :param request: Asynchronous request object.
    :return: RedirectResponse to the connect page.
    """
    return templates.TemplateResponse("connect.html", {"request": request, "success": None})


@router.post("/connect-to-device")
async def connect_to_device(request: Request):
    """
    Connect to a device using ADB pairing.
    This method uses the ADB command to pair with a device using its IP address and port
    :param request: Asynchronous request object.
    :return: RedirectResponse to the packages page if successful,
     otherwise renders the connect template with an error message.
    """
    form = await request.form()
    device_ip = form.get("device_ip")
    device_port = form.get("device_port")
    device_code = form.get("pair_code")
    status = await ConnectionManager.connect_to_device(device_ip, device_port, device_code)
    if status:
        return RedirectResponse("/packages", status_code=303)
    return templates.TemplateResponse("connect.html", {"request": request, "success": False})


@router.get("/packages")
async def get_packages(request: Request):
    """
    Retrieve the list of installed packages on the device.
    :param request: Asynchronous request object.
    :return: Rendered HTML template with the list of installed packages.
    """
    packages = await PackageManager.get_installed_packages()
    if not packages:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(
        "packages.html", {"request": request, "packages": packages, "message": "", "success": True}
    )


@router.post("/apply-actions")
async def apply_action(request: Request):
    """
    Apply actions (disable or uninstall) on the selected packages.
    This method processes the form data submitted from the packages page,
    performs the specified actions on the packages, and returns the result.
    :param request: Asynchronous request object containing the form data.
    :return: Rendered HTML template with the result of the actions performed.
    """
    form = await request.form()
    action_form = dict(form)
    failed_packages = await PackageManager.perform_action_on_packages(action_form)
    return templates.TemplateResponse(
        "status.html",
        {
            "request": request,
            "message": (
                "Failed to perform actions on: " + "\n".join(failed_packages)
                if failed_packages
                else "Successfully applied actions."
            ),
            "success": not failed_packages,
        },
    )
