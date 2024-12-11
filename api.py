from fastapi import FastAPI
import multiprocessing
import flet as fl

from frontend.app.portalapp import Portalapp

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Servidor FastAPI está corriendo correctamente.'}


def start_flet():
    """
    Función principal de inicialización de la aplicación.

    Responsabilidades:
    - Crea una instancia de la aplicación Portal
    - Lanza la aplicación utilizando el framework Flet
    - Configura la vista de la aplicación como una aplicación Flet nativa
    """
    portal_app = Portalapp()
    fl.app(
        target=portal_app.main,
        view=fl.AppView.WEB_BROWSER,  # O ajusta si prefieres otra vista
    )


# Arrancar Flet en un proceso independiente
@app.on_event('startup')
async def startup_event():
    flet_process = multiprocessing.Process(target=start_flet)
    flet_process.start()
