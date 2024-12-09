# frontend/ventas/components/form.py
import flet as ft


class VentaForm:
    """Formulario para realizar una venta.

    Esta clase representa un formulario de venta que permite seleccionar un producto, ingresar el monto,
    y calcular el total y la devolución de una transacción. Además, cuenta con un botón para realizar la venta.

    Atributos:
        producto_list (ft.Dropdown): Lista desplegable de productos disponibles para la venta.
        monto_input (ft.TextField): Campo de texto para ingresar el monto de la venta.
        total_text (ft.Text): Texto que muestra el total de la venta.
        devolucion_text (ft.Text): Texto que muestra la cantidad a devolver.
        vender_button (ft.ElevatedButton): Botón para realizar la venta.

    Métodos:
        update_options(new_options): Actualiza las opciones disponibles en el dropdown de productos.
        build(): Construye y retorna la estructura de la interfaz de usuario del formulario de venta.
    """

    def __init__(self, on_producto_change=None, on_monto_change=None, on_vender=None):
        """Inicializa el formulario de venta con los controles necesarios.

        Args:
            on_producto_change (Callable, opcional): Función que se ejecuta cuando se cambia el producto.
            on_monto_change (Callable, opcional): Función que se ejecuta cuando se cambia el monto.
            on_vender (Callable, opcional): Función que se ejecuta al hacer clic en el botón de vender.
        """
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
        """Actualiza las opciones del dropdown de productos.

        Este método permite modificar las opciones disponibles en la lista de productos.

        Args:
            new_options (List[ft.DropdownOption]): Lista de nuevas opciones para el dropdown de productos.
        """
        self.producto_list.options = new_options
        self.producto_list.value = None

    def build(self):
        """Construye la interfaz de usuario del formulario de venta.

        Este método organiza y devuelve la disposición de los elementos del formulario,
        incluyendo el campo de selección de producto, el campo de monto, los textos de total y devolución,
        y el botón de venta.

        Returns:
            ft.Column: El contenedor principal con todos los elementos de la interfaz.
        """
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
