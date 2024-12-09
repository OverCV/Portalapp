# frontend/ventas/components/list.py
import flet as ft


class VentaList:
    """Lista de productos en una venta, mostrando nombre, cantidad y total.

    Esta clase gestiona la visualización de una lista de productos vendidos en una venta,
    permitiendo actualizar la cantidad de productos, calcular el total y gestionar interacciones
    con botones de incremento y decremento para las cantidades.

    Atributos:
        on_cantidad_change (Callable, opcional): Función que se ejecuta cuando se cambia la cantidad de un producto.
        list_view (ft.ListView): Contenedor que presenta la lista de productos y sus detalles.

    Métodos:
        _get_header(): Crea y devuelve la fila de cabecera de la lista.
        update_items(items): Actualiza la lista con los productos y sus detalles.
        _handle_decrease(e): Maneja la disminución de la cantidad de un producto.
        _handle_increase(e): Maneja el incremento de la cantidad de un producto.
        clear(): Limpia la lista, pero mantiene la cabecera visible.
    """

    def __init__(self, on_cantidad_change=None):
        """Inicializa la lista de venta con un controlador opcional para cambios en la cantidad.

        Args:
            on_cantidad_change (Callable, opcional): Función que se ejecuta cuando se cambia la cantidad de un producto.
        """
        self.on_cantidad_change = on_cantidad_change
        self.list_view = ft.ListView(
            spacing=10,
            padding=10,
            expand=True,
            height=200,
            controls=[self._get_header()],
        )

    def _get_header(self):
        """Genera la cabecera de la lista de productos.

        Returns:
            ft.Row: Fila de cabecera con los títulos de columna.
        """
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
        """Actualiza la lista de productos con los datos proporcionados.

        Crea filas para cada producto con su nombre, cantidad y total. Los botones de incremento y
        decremento permiten modificar la cantidad de productos.

        Args:
            items (List[dict]): Lista de diccionarios que representan los productos a mostrar,
                                 donde cada diccionario debe contener 'nombre', 'cantidad',
                                 'total', y 'producto_id'.
        """
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
        """Disminuye la cantidad del producto seleccionado.

        Este método es llamado cuando el botón de disminución es presionado. Si hay un controlador
        para el cambio de cantidad, se ejecuta con un valor negativo.

        Args:
            e (ft.ControlEvent): El evento del control, que contiene la referencia al producto.
        """
        if self.on_cantidad_change:
            self.on_cantidad_change(e.control.data, -1)

    def _handle_increase(self, e):
        """Aumenta la cantidad del producto seleccionado.

        Este método es llamado cuando el botón de incremento es presionado. Si hay un controlador
        para el cambio de cantidad, se ejecuta con un valor positivo.

        Args:
            e (ft.ControlEvent): El evento del control, que contiene la referencia al producto.
        """
        if self.on_cantidad_change:
            self.on_cantidad_change(e.control.data, 1)

    def clear(self):
        """Limpia la lista, pero mantiene la cabecera.

        Este método remueve todos los productos de la lista, pero deja la cabecera visible.
        """
        self.list_view.controls = [self._get_header()]
