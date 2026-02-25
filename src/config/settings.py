import os

# ENTORNO

ENV = os.getenv("ENV", "EQU")

# SAP WEBGUI

SAP_BASE_URL = {
    "EDU": "http://amsdevecc01.claro.amx:8000",
    "EQU": "http://abapvip.claro.amx:8000",
    "EPU": "http://amsprdecc01.claro.amx:8000"
}

SAP_CLIENT = os.getenv("SAP_CLIENT", "100")
SAP_LANGUAGE = os.getenv("SAP_LANGUAGE", "ES")

SAP_WEBGUI_LOGIN_PATH = (
    "/sap/bc/gui/sap/its/webgui"
    f"?sap-client={SAP_CLIENT}"
    f"&sap-language={SAP_LANGUAGE}"
)

SAP_LOGIN_URL = SAP_BASE_URL[ENV] + SAP_WEBGUI_LOGIN_PATH

# CREDENCIALES SAP

SAP_USERNAME = os.getenv("SAP_USERNAME")
SAP_PASSWORD = os.getenv("SAP_PASSWORD")

if not SAP_USERNAME or not SAP_PASSWORD:
    raise RuntimeError(
        "Faltan credenciales SAP. "
        "Definir SAP_USERNAME y SAP_PASSWORD como variables de entorno."
    )

# TIEMPOS DE ESPERA

DEFAULT_WAIT = int(os.getenv("DEFAULT_WAIT", "10"))
LOGIN_WAIT = int(os.getenv("LOGIN_WAIT", "5"))

