# frontend/ventas/view.py
import flet as ft
from backend.data.managers.csv_manager import CSVManager
from frontend.ventas.components.form import VentaForm
from frontend.ventas.components.list import VentaList
from frontend.ventas.presenter import VentasPresenter


def mostrar_ventas(page: ft.Page, sql_manager: CSVManager) -> ft.View:
    view = VentasView(page, sql_manager)
    return view.build()


class VentasView:
    """Vista para la gestión de ventas.

    Esta clase representa la interfaz de usuario para el proceso de registro de ventas,
    incluyendo la selección de productos, el cálculo de montos y devoluciones, y la 
    finalización de la venta.

    Atributos:
        page (ft.Page): La página de Flet donde se renderiza la vista.
        presenter (VentasPresenter): El presentador que maneja la lógica de la aplicación.
        venta_list (VentaList): Componente que muestra la lista de productos en venta.
        venta_form (VentaForm): Componente que permite ingresar la información de la venta.
    """
    def __init__(self, page: ft.Page, data_manager):
        """Inicializa la vista de ventas.

        Args:
            page (ft.Page): La página de Flet donde se renderiza la vista.
            data_manager: El gestor de datos que maneja la información de las ventas y productos.
        """
        self.page = page

        # Primero inicializamos el presenter
        self.presenter = VentasPresenter(self, data_manager)

        # Luego los componentes con sus callbacks del presenter
        self.venta_list = VentaList(
            on_cantidad_change=self.presenter.modificar_cantidad,  # Directo al presenter
        )
        self.venta_form = VentaForm(
            on_producto_change=self._on_producto_change,
            on_monto_change=self._on_monto_change,
            on_vender=self._on_vender,
        )

        # Finalmente inicializamos la vista
        self.init_view()

    def init_view(self):
        """Inicializa el estado inicial de la vista.

        Configura las opciones de productos disponibles en el formulario.
        """
        self.venta_form.producto_list.options = self.presenter.filtrar_productos_con_stock()

    def build(self):
        """Construye la vista de la página de ventas.

        Retorna:
            ft.View: Vista que contiene todos los componentes necesarios para la interfaz de ventas.
        """
        return ft.View(
            '/ventas',
            [
                ft.AppBar(title=ft.Text('Registrar venta 🛒'), center_title=True),
                ft.Container(content=self.venta_form.producto_list, padding=10),
                ft.Divider(),
                ft.Container(content=self.venta_list.list_view, expand=True),
                ft.Divider(),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [ft.Text('Total: '), self.venta_form.total_text],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Row(
                                [
                                    self.venta_form.monto_input,
                                    ft.Container(width=20),
                                    self.venta_form.devolucion_text,
                                ]
                            ),
                            ft.Row(
                                [self.venta_form.vender_button],
                                alignment=ft.MainAxisAlignment.CENTER,
                                expand=True,
                            ),
                        ]
                    ),
                    padding=10,
                ),
            ],
        )

    def actualizar_productos_disponibles(self, opciones):
        """Actualiza las opciones disponibles en el dropdown de productos.

        Args:
            opciones (list): Lista de opciones de productos a mostrar en el dropdown.
        """
        self.venta_form.producto_list.options = opciones
        self.venta_form.producto_list.value = None  # Limpiar selección actual
        self.page.update()

    # Métodos privados para procesar eventos de UI
    def _on_producto_change(self, e):
        """Maneja el cambio en la selección de producto.

        Args:
            e (ft.ControlEvent): El evento que contiene la nueva selección de producto.
        """
        if e.control.value:  # Solo si hay valor seleccionado
            self.presenter.handle_producto_seleccionado(e.control.value)

    def _on_monto_change(self, e):
        """Maneja el cambio en el monto ingresado.

        Args:
            e (ft.ControlEvent): El evento que contiene el valor ingresado para el monto.
        """
        if e.control.value:  # Solo si hay valor ingresado
            self.presenter.calcular_devolucion(e.control.value)

    def _on_vender(self, e):
        """Maneja la acción de vender al presionar el botón 'Vender'.

        Args:
            e (ft.ControlEvent): El evento del clic en el botón de vender.
        """
        try:
            monto = float(self.venta_form.monto_input.value or 0)
            self.presenter.handle_vender(monto)
        except ValueError:
            self.mostrar_error('El monto debe ser un número válido')

    def actualizar_total(self, total: float):
        """Maneja la acción de vender al presionar el botón 'Vender'.

        Args:
            e (ft.ControlEvent): El evento del clic en el botón de vender.
        """
        self.venta_form.total_text.value = f'${total:.2f}'
        # No llamamos a page.update() aquí porque se hará en _actualizar_vista

    def actualizar_devolucion(self, devolucion: float):
        """Actualiza el texto de la devolución en el formulario de venta.

        Args:
            devolucion (float): El monto de la devolución.
        """
        self.venta_form.devolucion_text.value = f'${devolucion:.2f}'
        self.venta_form.devolucion_text.color = ft.colors.RED if devolucion < 0 else ft.colors.BLUE
        self.page.update()

    def mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error o éxito al usuario.

        Args:
            mensaje (str): El mensaje que se desea mostrar al usuario.
        """
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(mensaje)))
        self.page.update()

    def limpiar_formulario(self):
        """Limpia el formulario después de una venta exitosa"""
        self.venta_form.monto_input.value = ''
        self.venta_form.producto_list.value = None
        self.venta_form.total_text.value = '$0.00'
        self.venta_form.devolucion_text.value = '$0.00'
        self.venta_list.clear()

        # Actualizar las opciones disponibles
        self.venta_form.producto_list.options = self.presenter.filtrar_productos_con_stock()
        self.page.update()
