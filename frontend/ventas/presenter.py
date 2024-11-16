# frontend/ventas/presenter.py
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List
import flet as ft

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


class VentasPresenter:
    def __init__(self, view, data_manager):
        self.view = view
        self.data_manager: CSVManager = data_manager
        self.productos_venta: List[ItemVenta] = []
        self.productos: List[Producto] = []
        self.total_actual = 0.0

        # Cargar productos iniciales
        self.cargar_productos()

        # Configurar diálogo de deuda
        self._init_deuda_dialog()

    def _init_deuda_dialog(self):
        """Inicializa el diálogo de deuda"""
        self.nombre_input = ft.TextField(label='Nombre del Cliente', width=200)
        self.telefono_input = ft.TextField(label='Teléfono (opcional)', width=200)

        self.deuda_dialog = ft.AlertDialog(
            title=ft.Text('Generar deuda'),
            content=ft.Column(
                [
                    ft.Text('El monto ingresado es insuficiente para realizar la venta.'),
                    self.nombre_input,
                    self.telefono_input,
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton('Confirmar deuda', on_click=self._confirmar_deuda),
                ft.TextButton('Cancelar', on_click=lambda _: self._cerrar_dialog()),
            ],
        )

    def cargar_productos(self):
        """Obtiene los productos disponibles del data manager"""
        self.productos = self.data_manager.get_data(Producto)
        self.productos = [p for p in self.productos if p.stock > 0]

    def filtrar_productos_con_stock(self) -> list[ft.dropdown.Option]:
        """Crea las opciones del dropdown solo con productos que tienen stock"""
        return [
            ft.dropdown.Option(key=str(p.id), text=p.nombre) for p in self.productos if p.stock > 0
        ]

    def _encontrar_producto(self, producto_id: int) -> Optional[Producto]:
        """Busca un producto por su ID"""
        return next((p for p in self.productos if p.id == producto_id), None)

    def handle_producto_seleccionado(self, producto_id: str):
        """Maneja la selección de un producto"""
        if not producto_id:
            return

        producto = self._encontrar_producto(int(producto_id))
        if not producto:
            return

        # Buscar si el producto ya está en la venta
        producto_venta = next(
            (pv for pv in self.productos_venta if pv.producto.id == producto.id), None
        )

        if producto_venta:
            # Verificar stock antes de incrementar
            if producto_venta.cantidad < producto.stock:
                producto_venta.cantidad += 1
            else:
                self.view.mostrar_error(f'Stock insuficiente para {producto.nombre}')
                return
        else:
            # Añadir nuevo producto a la venta
            self.productos_venta.append(ItemVenta(producto=producto, cantidad=1))

        self._actualizar_vista()

    def modificar_cantidad(self, producto_id: int, delta: int):
        """Modifica la cantidad de un producto en la venta"""
        producto_venta = next(
            (pv for pv in self.productos_venta if pv.producto.id == producto_id), None
        )

        if not producto_venta:
            return

        nueva_cantidad = producto_venta.cantidad + delta

        if delta > 0 and nueva_cantidad > producto_venta.producto.stock:
            self.view.mostrar_error(f'Stock insuficiente para {producto_venta.producto.nombre}')
            return

        if nueva_cantidad < 1:
            self.productos_venta.remove(producto_venta)
        else:
            producto_venta.cantidad = nueva_cantidad

        self._actualizar_vista()

    def calcular_devolucion(self, monto: str):
        """Calcula la devolución basada en el monto ingresado"""
        try:
            monto_pagado = float(monto or 0)
            devolucion = monto_pagado - self.total_actual

            # Actualizar UI con el resultado
            self.view.actualizar_devolucion(devolucion)
            return devolucion
        except ValueError:
            self.view.mostrar_error('El monto debe ser un número válido')
            self.view.limpiar_formulario()
            return 0

    def _actualizar_vista(self):
        """Actualiza todos los elementos de la vista"""
        # Calcular nuevo total
        self.total_actual = sum(pv.total for pv in self.productos_venta)
        self.view.actualizar_total(self.total_actual)

        # Actualizar lista de ventas
        items_venta = [
            {
                'nombre': pv.producto.nombre,
                'cantidad': pv.cantidad,
                'total': pv.total,
                'producto_id': pv.producto.id,
            }
            for pv in self.productos_venta
        ]
        self.view.venta_list.update_items(items_venta)

        # Actualizar opciones del dropdown
        self.view.actualizar_productos_disponibles(self.filtrar_productos_con_stock())

        # Forzar actualización de la página
        self.view.page.update()

    def handle_vender(self, monto_pagado: float = 0):
        """Procesa la venta actual"""

        if not self.productos_venta:
            self.view.mostrar_error('No hay productos en la venta')
            return

        try:
            # 1. Convertir total_actual a float si no lo es
            total_float = float(self.total_actual)
            # 2. Redondear el float
            total_redondeado = round(total_float)
            # 3. Convertir a entero
            total_venta = int(total_redondeado)
            # Mismo proceso para monto_pagado
            monto_float = float(monto_pagado)
            monto_redondeado = round(monto_float)
            monto_pagado_redondeado = int(monto_redondeado)
            # Calcular ganancia
            ganancia = min(monto_pagado_redondeado, total_venta)
            # Verificar si el monto es insuficiente
            if monto_pagado < total_venta:
                self._mostrar_dialog_deuda()
                return

            # Crear la venta con total y ganancia
            venta = Venta(
                id=-1,
                fecha=datetime.now().isoformat(),
                total=total_venta,
                ganancia=ganancia,
            )

            venta = self.data_manager.add_data(venta)

            # Registrar productos y actualizar stock
            productos_actualizados = False
            for producto_venta in self.productos_venta:
                # Registrar venta-producto
                venta_producto = VentaProducto(
                    id=-1,
                    id_venta=venta.id,
                    id_producto=producto_venta.producto.id,
                    cantidad=producto_venta.cantidad,
                    fecha=datetime.now().isoformat(),
                )

                self.data_manager.add_data(venta_producto)

                # Actualizar stock
                producto = producto_venta.producto
                producto.stock -= producto_venta.cantidad

                self.data_manager.put_data(Producto, producto.id, {'stock': producto.stock})
                if producto.stock == 0:
                    productos_actualizados = True

            # Limpiar estado
            self.productos_venta.clear()

            # Recargar productos y actualizar UI
            if productos_actualizados:
                self.cargar_productos()  # Esto actualizará la lista de productos disponibles

            self._actualizar_vista()
            self.view.limpiar_formulario()
            self.view.mostrar_error('Venta registrada correctamente')

        except Exception as e:
            error_msg = f'Error al procesar la venta: {str(e)}'
            self.view.mostrar_error(error_msg)

    def _mostrar_dialog_deuda(self):
        """Muestra el diálogo para crear una deuda"""
        self.view.page.dialog = self.deuda_dialog
        self.deuda_dialog.open = True
        self.view.page.update()

    def _confirmar_deuda(self, e):
        """Procesa la confirmación de una deuda"""
        nombre_cliente = self.nombre_input.value.strip()
        telefono_cliente = self.telefono_input.value.strip()

        if not nombre_cliente:
            self.view.mostrar_error('El nombre del cliente es obligatorio')
            return

        try:
            # Primero creamos la venta
            total_venta = int(self.total_actual)
            monto_pagado = 0  # En caso de deuda, iniciamos con 0 pagado

            venta = Venta(
                id=-1,
                fecha=datetime.now().isoformat(),
                total=total_venta,
                ganancia=monto_pagado,  # La ganancia inicial es 0
            )
            venta = self.data_manager.add_data(venta)

            # Registrar productos y actualizar stock
            for producto_venta in self.productos_venta:
                venta_producto = VentaProducto(
                    id=-1,
                    id_venta=venta.id,
                    id_producto=producto_venta.producto.id,
                    cantidad=producto_venta.cantidad,
                )
                self.data_manager.add_data(venta_producto)

                # Actualizar stock
                producto = producto_venta.producto
                producto.stock -= producto_venta.cantidad
                self.data_manager.put_data(Producto, producto.id, {'stock': producto.stock})

            # Crear la deuda asociada a la venta
            deuda = Deuda(
                id=-1,
                id_venta=venta.id,
                id_deudor=-1,  # TODO: Implementar sistema de deudores
                valor_deuda=total_venta,
                # El valor de la deuda es el total de la venta
                creacion_deuda=datetime.now().isoformat(),
                # Convertir a ISO string para consistencia
            )

            # Guardar la deuda
            self.data_manager.add_data(deuda)

            # Limpiar estado y UI
            self.productos_venta.clear()
            self.cargar_productos()
            self._actualizar_vista()
            self.view.limpiar_formulario()

            # Cerrar diálogo y mostrar confirmación
            self._cerrar_dialog()
            self.view.mostrar_error('Venta a crédito registrada correctamente')

        except Exception as e:
            self.view.mostrar_error(f'Error al registrar la venta a crédito: {str(e)}')

    def _cerrar_dialog(self):
        """Cierra el diálogo actual"""
        if self.deuda_dialog:
            self.deuda_dialog.open = False
            self.view.page.update()
