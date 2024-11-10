import flet as fl
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from backend.data.managers.csv_manager import CSVManager

from backend.models.producto import Producto
from backend.models.venta import Venta
from backend.models.venta_producto import VentaProducto
from backend.models.deuda import Deuda


@dataclass
class ItemVenta:
    """Clase auxiliar para manejar productos en la venta actual"""

    producto: Producto
    cantidad: int

    @property
    def total(self) -> float:
        return self.producto.precio * self.cantidad


class VentasController:
    def __init__(self, page: fl.Page, data_manager: CSVManager):
        self.page = page
        self.data_manager: CSVManager = data_manager
        self.__productos_venta: list[ItemVenta] = []
        self.__productos: list[Producto] = self._obtener_productos()

        # Elementos UI
        self.total_venta = fl.Text(value='0', color='blue')
        self.devolucion_text = fl.Text(
            '$0.00', size=16, weight=fl.FontWeight.BOLD, color=fl.colors.BLUE
        )
        self.monto_insuficiente_dialog = fl.AlertDialog(
            title=fl.Text('Monto insuficiente'),
            content=fl.Text('El monto ingresado es insuficiente para realizar la venta.'),
            actions=[fl.TextButton('OK', on_click=self.close_dialog)],
            open=False,
        )

    def _obtener_productos(self) -> list[Producto]:
        """Obtiene los productos disponibles del data manager"""
        productos: list[Producto] = self.data_manager.get_data(Producto)
        return [p for p in productos if p.stock > 0]

    def filtrar_productos_con_stock(self) -> list[fl.dropdown.Option]:
        """Crea las opciones del dropdown solo con productos que tienen stock"""
        return [
            fl.dropdown.Option(key=str(p.id), text=p.nombre)
            for p in self.__productos
            if p.stock > 0
        ]

    def __encontrar_producto(self, producto_id: int) -> Optional[Producto]:
        """Busca un producto por su ID"""
        return next((p for p in self.__productos if p.id == producto_id), None)

    def handle_producto_seleccionado(self, e, producto_list, ventas_list, monto_input):
        if not producto_list.value:
            return

        producto = self.__encontrar_producto(int(producto_list.value))
        if not producto:
            return

        # Buscar si el producto ya está en la venta
        producto_venta = next(
            (pv for pv in self.__productos_venta if pv.producto.id == producto.id), None
        )

        if producto_venta:
            # Verificar stock antes de incrementar
            if producto_venta.cantidad < producto.stock:
                producto_venta.cantidad += 1
            else:
                self.__mostrar_snackbar(f'Stock insuficiente para {producto.nombre}')
                return
        else:
            # Añadir nuevo producto a la venta
            self.__productos_venta.append(ItemVenta(producto=producto, cantidad=1))

        self.actualizar_lista_ventas(ventas_list, monto_input)

    def actualizar_lista_ventas(self, ventas_list, monto_input):
        ventas_list.controls.clear()

        # Cabecera
        ventas_list.controls.append(
            fl.Row(
                [
                    fl.Text('Producto', weight='bold'),
                    fl.Text('Cantidad', weight='bold'),
                    fl.Text('Precio', weight='bold'),
                ],
                alignment='spaceBetween',
            )
        )

        # Lista de productos
        for producto_venta in self.__productos_venta:
            ventas_list.controls.append(
                fl.Row(
                    [
                        fl.Text(producto_venta.producto.nombre),
                        fl.Row(
                            [
                                fl.IconButton(
                                    icon=fl.icons.REMOVE_CIRCLE_OUTLINE_ROUNDED,
                                    selected_icon=fl.icons.REMOVE_CIRCLE,
                                    on_click=lambda e, pv=producto_venta: self.modificar_cantidad(
                                        pv, -1, ventas_list, monto_input
                                    ),
                                ),
                                fl.Text(str(producto_venta.cantidad)),
                                fl.IconButton(
                                    icon=fl.icons.ADD_CIRCLE_OUTLINE_ROUNDED,
                                    selected_icon=fl.icons.ADD_CIRCLE,
                                    on_click=lambda e, pv=producto_venta: self.modificar_cantidad(
                                        pv, 1, ventas_list, monto_input
                                    ),
                                ),
                            ]
                        ),
                        fl.Text(f'${producto_venta.total}'),
                    ],
                    alignment='spaceBetween',
                )
            )

        ventas_list.update()
        self.actualizar_total(monto_input)

    def modificar_cantidad(self, producto_venta: ItemVenta, delta: int, ventas_list, monto_input):
        nueva_cantidad = producto_venta.cantidad + delta

        if delta > 0 and nueva_cantidad > producto_venta.producto.stock:
            self.__mostrar_snackbar(f'Stock insuficiente para {producto_venta.producto.nombre}')
            return

        if nueva_cantidad < 1:
            self.__productos_venta.remove(producto_venta)
        else:
            producto_venta.cantidad = nueva_cantidad

        self.actualizar_lista_ventas(ventas_list, monto_input)

    def actualizar_total(self, monto_input):
        total = sum(pv.total for pv in self.__productos_venta)
        self.total_venta.value = f'${total:.2f}'
        self.total_venta.update()

        if monto_input.value:
            self.calcular_devolucion(None, monto_input)

    def calcular_devolucion(self, e, monto_input):
        try:
            monto = float(monto_input.value or 0)
            total = float(self.total_venta.value.replace('$', ''))
            devolucion = monto - total

            self.devolucion_text.value = f'${devolucion:.2f}'
            self.devolucion_text.color = fl.colors.RED if devolucion < 0 else fl.colors.BLUE
            self.devolucion_text.update()
        except ValueError:
            self.devolucion_text.value = '$0.00'
            self.devolucion_text.color = fl.colors.RED
            monto_input.value = ''
            monto_input.update()
            self.devolucion_text.update()

    def handle_vender(self, monto_input, producto_list, ventas_list):
        if not monto_input.value or float(monto_input.value) < float(
            self.total_venta.value.replace('$', '')
        ):
            # Llama a la función para gestionar la deuda si el monto es insuficiente
            self.generar_deuda()
            return
        if not self.__productos_venta:
            self.__mostrar_snackbar('No hay productos en la venta')
            return

        devolucion = float(self.devolucion_text.value.replace('$', ''))
        if devolucion < 0:
            self.monto_insuficiente_dialog.open = True
            self.page.dialog = self.monto_insuficiente_dialog
            self.page.update()
            return

        # Procesar la venta
        venta = Venta(
            id=0,
            fecha=datetime.now(),
            ganancia=int(float(self.total_venta.value.replace('$', ''))),
        )
        venta = self.data_manager.add_data(venta)

        # Registrar productos y actualizar stock
        for producto_venta in self.__productos_venta:
            venta_producto = VentaProducto(
                id=0,
                id_venta=venta.id,
                id_producto=producto_venta.producto.id,
                cantidad=producto_venta.cantidad,
            )
            self.data_manager.add_data(venta_producto)

            producto = producto_venta.producto
            producto.stock -= producto_venta.cantidad
            self.data_manager.put_data(Producto, producto.id, {'stock': producto.stock})

        self.__productos_venta.clear()
        self.__productos = self._obtener_productos()

        # Actualizar UI
        self.actualizar_lista_ventas(ventas_list, monto_input)
        producto_list.options = self.filtrar_productos_con_stock()
        producto_list.value = None
        producto_list.update()
        monto_input.value = ''
        monto_input.update()

        self.__mostrar_snackbar('Venta registrada correctamente')

    def __mostrar_snackbar(self, mensaje: str):
        """Utilidad para mostrar mensajes al usuario"""
        snack = fl.SnackBar(content=fl.Text(mensaje), action='OK')
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def close_dialog(self, e=None):
        self.monto_insuficiente_dialog.open = False
        self.page.update()

    """ DEUDA """

    def generar_deuda(self):
        # Campos de entrada para el nombre y el teléfono del cliente
        nombre_input = fl.TextField(label='Nombre del Cliente', width=200)
        telefono_input = fl.TextField(label='Teléfono (opcional)', width=200)

        # Configurar el diálogo de deuda
        self.monto_insuficiente_dialog = fl.AlertDialog(
            title=fl.Text('Generar deuda'),
            content=fl.Column(
                [
                    fl.Text(
                        f'El monto ingresado es insuficiente para realizar la venta.\n'
                        f'Se generará una deuda de ${self.total_venta.value.replace("$", "")}.'
                    ),
                    nombre_input,
                    telefono_input,
                ],
                tight=True,
            ),
            actions=[
                fl.TextButton(
                    'Confirmar deuda',
                    on_click=lambda e: self.confirmar_deuda(e, nombre_input, telefono_input),
                ),
                fl.TextButton('Cancelar', on_click=self.close_dialog),
            ],
            open=True,
        )

        # Mostrar el diálogo
        self.page.dialog = self.monto_insuficiente_dialog
        self.page.update()

    def confirmar_deuda(self, e, nombre_input, telefono_input):
        nombre_cliente = nombre_input.value.strip()
        telefono_cliente = telefono_input.value.strip()

        # Validación del nombre del cliente
        if not nombre_cliente:
            self.__mostrar_snackbar('El nombre del cliente es obligatorio para registrar la deuda')
            return

        # Crear instancia de Deuda
        deuda = Deuda(
            id=0,
            id_venta=0,  # Ajusta según el ID de venta si aplica
            id_deudor=-1,  # ID de deudor o el cliente actual
            valor_deuda=float(self.total_venta.value.replace('$', '')),
            creacion_deuda=datetime.now(),
        )
        # Registrar la deuda en el sistema
        # self.data_manager.add_data(deuda)

        # Cerrar el diálogo y mostrar confirmación
        self.monto_insuficiente_dialog.open = False
        self.page.update()
        self.__mostrar_snackbar('Deuda registrada correctamente')
