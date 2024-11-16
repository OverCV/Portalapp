# frontend/ventas/components/form.py
import flet as ft


class VentaForm:
    def __init__(self, on_producto_change=None, on_monto_change=None, on_vender=None):
        self.producto_list = ft.Dropdown(
            label='Producto',
            hint_text='Seleccione un producto',
            expand=True,
            on_change=on_producto_change,
        )

        self.monto_input = ft.TextField(
            label='Monto… ($)',
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
            on_change=on_monto_change,
        )

        self.total_text = ft.Text('Total: $0')
        self.devolucion_text = ft.Text('Devolución: $0')

        self.vender_button = ft.ElevatedButton(
            'Vender', icon=ft.icons.ACCOUNT_BALANCE_WALLET, expand=True, on_click=on_vender
        )

    def update_options(self, new_options):
        """Actualiza las opciones del dropdown"""
        self.producto_list.options = new_options
        self.producto_list.value = None

    def build(self):
        return ft.Column(
            [
                ft.Container(content=self.producto_list, padding=10),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [ft.Text('Total: '), self.total_text],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Row(
                                [self.monto_input, ft.Container(width=20), self.devolucion_text]
                            ),
                            ft.Row([self.vender_button], alignment=ft.MainAxisAlignment.CENTER),
                        ]
                    ),
                    padding=10,
                ),
            ]
        )
