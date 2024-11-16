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
    def __init__(self, page: ft.Page, data_manager):
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
        """Inicializa el estado inicial de la vista"""
        self.venta_form.producto_list.options = self.presenter.filtrar_productos_con_stock()

    def build(self):
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
        """Actualiza las opciones disponibles en el dropdown de productos"""
        self.venta_form.producto_list.options = opciones
        self.venta_form.producto_list.value = None  # Limpiar selección actual
        self.page.update()

    # Métodos privados para procesar eventos de UI
    def _on_producto_change(self, e):
        if e.control.value:  # Solo si hay valor seleccionado
            self.presenter.handle_producto_seleccionado(e.control.value)

    def _on_monto_change(self, e):
        if e.control.value:  # Solo si hay valor ingresado
            self.presenter.calcular_devolucion(e.control.value)

    def _on_vender(self, e):
        try:
            monto = float(self.venta_form.monto_input.value or 0)
            self.presenter.handle_vender(monto)
        except ValueError:
            self.mostrar_error('El monto debe ser un número válido')

    def actualizar_total(self, total: float):
        """Actualiza el texto del total en el formulario"""
        self.venta_form.total_text.value = f'${total:.2f}'
        # No llamamos a page.update() aquí porque se hará en _actualizar_vista

    def actualizar_devolucion(self, devolucion: float):
        """Actualiza el texto de la devolución en el formulario"""
        self.venta_form.devolucion_text.value = f'${devolucion:.2f}'
        self.venta_form.devolucion_text.color = ft.colors.RED if devolucion < 0 else ft.colors.BLUE
        self.page.update()

    def mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error/éxito al usuario"""
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
