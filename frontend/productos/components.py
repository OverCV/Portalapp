# productos/components.py #
import flet as fl
from backend.models.producto import Producto
from typing import Callable

from frontend.app.enums.app import AppParams


class ProductoCard(fl.Card):
    """Representa una tarjeta visual para mostrar la información de un producto.

    La tarjeta incluye detalles como el nombre, el precio, el stock y una imagen (si está disponible).
    También incluye botones para editar y eliminar el producto.

    Args:
        producto (Producto): Objeto que contiene la información del producto (nombre, precio, stock, ruta de la imagen).
        on_edit (Callable[[Producto], None]): Función de callback que se ejecuta al hacer clic en el botón de editar.
        on_delete (Callable[[Producto], None]): Función de callback que se ejecuta al hacer clic en el botón de eliminar.
    """
    def __init__(
        self,
        producto: Producto,
        on_edit: Callable[[Producto], None],
        on_delete: Callable[[Producto], None],
    ):
        """Inicializa una instancia de ProductoCard con los datos del producto y callbacks.

        La tarjeta ajusta dinámicamente su diseño dependiendo de si el producto incluye una ruta de imagen.

        Args:
            producto (Producto): Objeto que contiene la información del producto.
            on_edit (Callable[[Producto], None]): Callback para manejar la acción de edición.
            on_delete (Callable[[Producto], None]): Callback para manejar la acción de eliminación.
        """
        super().__init__()
        self.content = fl.Container(
            content=(
                fl.Row(
                    [
                        fl.Column(  # Columna izquierda
                            [
                                fl.Container(
                                    content=fl.Image(
                                        src=f'{AppParams.APP_ASSETS_PATH}/productos/{producto.imagen_ruta}',
                                        fit=fl.ImageFit.COVER,
                                    ),
                                    width=150,
                                    height=100,
                                    border_radius=fl.border_radius.all(8),
                                    clip_behavior=fl.ClipBehavior.ANTI_ALIAS,
                                ),
                                fl.Column(
                                    [
                                        fl.Text(
                                            producto.nombre,
                                            size=16,
                                            weight=fl.FontWeight.W_500,
                                            width=150,  # Limitar ancho
                                            overflow=fl.TextOverflow.ELLIPSIS,  # ... si es muy largo
                                        ),
                                        fl.Text(
                                            f'Stock: {producto.stock}',
                                            size=14,
                                            color=fl.colors.BLACK54
                                            if producto.stock >= 5
                                            else fl.colors.ERROR,
                                        ),
                                    ],
                                    spacing=2,
                                ),
                            ],
                            spacing=8,
                            expand=True,  # Toma el espacio restante
                        ),
                        fl.Column(  # Columna derecha
                            [
                                fl.Container(  # Contenedor para el precio
                                    content=fl.Text(
                                        f'${producto.precio:,}',
                                        size=16,
                                        weight=fl.FontWeight.W_500,
                                        text_align=fl.TextAlign.RIGHT,
                                    ),
                                    width=100,  # Ancho fijo para el precio
                                ),
                                fl.Row(
                                    [
                                        fl.IconButton(
                                            icon=fl.icons.EDIT_OUTLINED,
                                            tooltip='Editar',
                                            icon_size=20,
                                            on_click=lambda e: on_edit(producto),
                                        ),
                                        fl.IconButton(
                                            icon=fl.icons.DELETE_OUTLINE,
                                            icon_color=fl.colors.ERROR,
                                            tooltip='Eliminar',
                                            icon_size=20,
                                            on_click=lambda e: on_delete(producto),
                                        ),
                                    ],
                                    alignment=fl.MainAxisAlignment.END,
                                ),
                            ],
                            spacing=8,
                            alignment=fl.MainAxisAlignment.SPACE_BETWEEN,  # Distribuye verticalmente
                            height=160,  # Altura fija para que SPACE_BETWEEN funcione
                        ),
                    ],
                    alignment=fl.MainAxisAlignment.SPACE_BETWEEN,
                )
                if producto.imagen_ruta
                # Layout sin imagen (mantenemos el diseño original)
                else fl.Column(
                    [
                        fl.Row(
                            [
                                fl.Icon(
                                    fl.icons.IMAGE_NOT_SUPPORTED_OUTLINED,
                                    size=40,
                                    color=fl.colors.ON_SURFACE_VARIANT,
                                ),
                                fl.Column(
                                    [
                                        fl.Text(
                                            producto.nombre, size=16, weight=fl.FontWeight.W_500
                                        ),
                                        fl.Text(
                                            f'Stock: {producto.stock}',
                                            size=14,
                                            color=fl.colors.BLACK54
                                            if producto.stock >= 5
                                            else fl.colors.ERROR,
                                        ),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                fl.Text(
                                    f'${producto.precio:,}',
                                    size=16,
                                    weight=fl.FontWeight.W_500,
                                ),
                            ],
                            expand=True,
                            alignment=fl.MainAxisAlignment.START,
                        ),
                        fl.Row(
                            [
                                fl.IconButton(
                                    icon=fl.icons.EDIT_OUTLINED,
                                    tooltip='Editar',
                                    icon_size=20,
                                    on_click=lambda e: on_edit(producto),
                                ),
                                fl.IconButton(
                                    icon=fl.icons.DELETE_OUTLINE,
                                    icon_color=fl.colors.ERROR,
                                    tooltip='Eliminar',
                                    icon_size=20,
                                    on_click=lambda e: on_delete(producto),
                                ),
                            ],
                            alignment=fl.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=8,
                )
            ),
            padding=fl.padding.all(10),
            width=250,
            height=180 if producto.imagen_ruta else 100,
            bgcolor=fl.colors.SURFACE_VARIANT,
            border_radius=fl.border_radius.all(12),
        )
