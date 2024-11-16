# frontend/ventas/components/list.py
import flet as ft


class VentaList:
    def __init__(self, on_cantidad_change=None):
        self.on_cantidad_change = on_cantidad_change
        self.list_view = ft.ListView(
            spacing=10,
            padding=10,
            expand=True,
            height=200,
            controls=[self._get_header()],
        )

    def _get_header(self):
        """Retorna el row de la cabecera"""
        return ft.Row(
            [
                ft.Text(
                    'Producto',
                    weight=ft.FontWeight.BOLD,
                    expand=True,  # Para que tome el espacio disponible
                ),
                ft.Text(
                    'Cantidad',
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,  # Centrar el texto
                    expand=True,  # Para que tome el espacio disponible
                ),
                ft.Text(
                    'Total',
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.RIGHT,  # Alinear a la derecha
                    expand=True,  # Para que tome el espacio disponible
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def update_items(self, items):
        controls = [self._get_header()]

        for item in items:
            row = ft.Row(
                [
                    # Columna Producto (izquierda)
                    ft.Text(item['nombre'], expand=True),
                    # Columna Cantidad (centro)
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    ft.icons.REMOVE_CIRCLE_OUTLINE,
                                    data=item['producto_id'],
                                    on_click=self._handle_decrease,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        str(item['cantidad']),
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    width=30,  # Ancho fijo para el número
                                    alignment=ft.alignment.center,
                                ),
                                ft.IconButton(
                                    ft.icons.ADD_CIRCLE_OUTLINE,
                                    data=item['producto_id'],
                                    on_click=self._handle_increase,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,  # Centrar horizontalmente
                        ),
                        expand=True,  # Para que tome el espacio disponible
                        alignment=ft.alignment.center,  # Centrar el contenedor
                    ),
                    # Columna Total (derecha)
                    ft.Text(f"${item['total']:.2f}", text_align=ft.TextAlign.RIGHT, expand=True),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            controls.append(row)

        self.list_view.controls = controls

    def _handle_decrease(self, e):
        if self.on_cantidad_change:
            self.on_cantidad_change(e.control.data, -1)

    def _handle_increase(self, e):
        if self.on_cantidad_change:
            self.on_cantidad_change(e.control.data, 1)

    def clear(self):
        """Limpia la lista pero mantiene la cabecera"""
        self.list_view.controls = [self._get_header()]
