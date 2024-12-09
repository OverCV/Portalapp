from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List
import flet as ft

from backend.data.managers.csv_manager import CSVManager
from backend.models.deudor import Deudor
from backend.models.producto import Producto
from backend.models.venta import Venta

from backend.app.routes.productos import ProductoRoutes
from backend.app.services.productos import ProductoService
from backend.app.routes.ventas import VentaRoutes
from backend.app.services.ventas import VentaService


@dataclass
class ItemVenta:
    """Clase auxiliar para manejar productos en la venta actual"""

    producto: Producto
    cantidad: int

    @property
    def total(self) -> float:
        return self.producto.precio * self.cantidad


class VentasPresenter:
    def __init__(self, view, data_manager: CSVManager):
        self.view = view
        self.productos_venta: List[ItemVenta] = []
        self.total_actual = 0.0

        # Inicializar servicios
        self.venta_service = VentaService(data_manager)
        self.producto_service = ProductoService(data_manager)

        # Inicializar rutas
        self.venta_routes = VentaRoutes(self.venta_service)
        self.producto_routes = ProductoRoutes(self.producto_service)

        # Cargar productos iniciales
        self.productos = self.producto_routes.get_productos_disponibles()

        # Cargar los deudores existentes
        self.deudores: list[Deudor] = data_manager.get_data(Deudor)

        self.indice_deudor: Deudor | None = None

        # Inicializar diálogo de deuda
        self._init_deuda_dialog()

    def _init_deuda_dialog(self):
        """Inicializa el diálogo de deuda"""
        # Inicializamos el estado de búsqueda
        self.busqueda_activa = True

        # Creando el input de nombre usando AutoComplete (por defecto)
        self.nombre_input = ft.AutoComplete(
            suggestions=[
                ft.AutoCompleteSuggestion(key=deudor.nombre, value=deudor.nombre)
                for deudor in self.deudores
            ],
            on_select=lambda e: self.set_deudor_seleccionado(e.control),
        )

        # Creando el input de teléfono usando AutoComplete
        self.telefono_input = ft.TextField(label="Teléfono", width=200)

        # Botón de búsqueda o agregar nuevo deudor
        self.buscar_icon = ft.IconButton(
            ft.icons.ADD,  # ícono de añadir por defecto
            width=40,
            height=40,
            on_click=self.toggle_busqueda,
        )

        # Crear el diálogo de deuda
        self.deuda_dialog = ft.AlertDialog(
            title=ft.Text("Generar deuda"),
            content=ft.Column(
                [
                    ft.Text(
                        "El monto ingresado es insuficiente para realizar la venta."
                    ),
                    # Primera fila con el nombre_input y el botón de búsqueda
                    ft.Row(
                        [
                            ft.Column([self.nombre_input], width=200),
                            ft.Column([self.buscar_icon], width=80),
                        ],
                    ),
                    # Segunda fila con teléfono_input
                    ft.Row([ft.Column([self.telefono_input], width=200)]),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Confirmar deuda", on_click=self._confirmar_deuda),
                ft.TextButton("Cancelar", on_click=lambda _: self._cerrar_dialog()),
            ],
        )

    def toggle_busqueda(self, e):
        """Alterna entre búsqueda y agregar nuevo deudor"""
        self.busqueda_activa = not self.busqueda_activa
        if self.busqueda_activa:
            # Cambiar a búsqueda (AutoComplete)
            self.nombre_input = ft.AutoComplete(
                suggestions=[
                    ft.AutoCompleteSuggestion(key=deudor.nombre, value=deudor.nombre)
                    for deudor in self.deudores
                ],
                on_select=lambda e: self.set_deudor_seleccionado(e.control),
            )
            self.buscar_icon.icon = ft.icons.ADD  # Cambiar el ícono a lupa
        else:
            # Cambiar a agregar nuevo deudor (TextField)
            self.nombre_input = ft.TextField(label="Nombre del Deudor", width=200)
            self.buscar_icon.icon = ft.icons.SEARCH  # Cambiar el ícono a "+"

        # Volver a renderizar el diálogo
        self.deuda_dialog.content = self._get_deuda_dialog_content()
        self.view.page.update()

    def _get_deuda_dialog_content(self):
        """Genera el contenido del diálogo de deuda basado en el estado actual"""
        return ft.Column(
            [
                ft.Text("El monto ingresado es insuficiente para realizar la venta."),
                # Primera fila con nombre_input y botón de búsqueda
                ft.Row(
                    [
                        ft.Column([self.nombre_input], width=200),
                        ft.Column([self.buscar_icon], width=80),
                    ],
                ),
                # Segunda fila con teléfono_input
                ft.Row([ft.Column([self.telefono_input], width=200)]),
            ],
            tight=True,
        )

    def set_deudor_seleccionado(self, datos_deudor: ft.AutoComplete):
        print(datos_deudor)
        print(datos_deudor.data)
        self.indice_deudor = datos_deudor.selected_index

    def filtrar_productos_con_stock(self) -> List[ft.dropdown.Option]:
        """Crea las opciones del dropdown solo con productos que tienen stock"""
        return [
            ft.dropdown.Option(key=str(p.id), text=p.nombre)
            for p in self.productos
            if p.stock > 0
        ]

    def handle_producto_seleccionado(self, producto_id: str):
        if not producto_id:
            return

        producto = next((p for p in self.productos if p.id == int(producto_id)), None)
        if not producto:
            return

        # Buscar si el producto ya está en la venta
        producto_venta = next(
            (pv for pv in self.productos_venta if pv.producto.id == producto.id), None
        )

        if producto_venta:
            if producto_venta.cantidad < producto.stock:
                producto_venta.cantidad += 1
            else:
                self.view.mostrar_error(f"Stock insuficiente para {producto.nombre}")
                return
        else:
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
            self.view.mostrar_error(
                f"Stock insuficiente para {producto_venta.producto.nombre}"
            )
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
            self.view.mostrar_error("El monto debe ser un número válido")
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
                "nombre": pv.producto.nombre,
                "cantidad": pv.cantidad,
                "total": pv.total,
                "producto_id": pv.producto.id,
            }
            for pv in self.productos_venta
        ]
        self.view.venta_list.update_items(items_venta)

        # Actualizar opciones del dropdown
        self.view.actualizar_productos_disponibles(self.filtrar_productos_con_stock())

        # Forzar actualización de la página
        self.view.page.update()

    def handle_vender(self, monto_pagado: float = 0):
        if not self.productos_venta:
            self.view.mostrar_error("No hay productos en la venta")
            return

        try:
            if monto_pagado < self.total_actual:
                self._mostrar_dialog_deuda()
                return

            productos = [
                {"id_producto": item.producto.id, "cantidad": item.cantidad}
                for item in self.productos_venta
            ]

            self.venta_routes.create_venta(
                {"productos": productos, "monto_pagado": monto_pagado}
            )

            # Recargar productos para tener el stock actualizado
            self.productos = self.producto_routes.get_productos_disponibles()

            # Limpiar estado y UI
            self.productos_venta.clear()
            self._actualizar_vista()
            self.view.limpiar_formulario()
            self.view.mostrar_error("Venta registrada correctamente")

        except ValueError as e:
            self.view.mostrar_error(str(e))
        except Exception as e:
            print(e)
            self.view.mostrar_error(f"Error al procesar la venta: {str(e)}")

    def _mostrar_dialog_deuda(self):
        """Muestra el diálogo para crear una deuda"""
        self.view.page.dialog = self.deuda_dialog
        self.deuda_dialog.open = True
        self.view.page.update()

    def _confirmar_deuda(self, e):
        """Procesa la confirmación de una deuda"""
        if self.busqueda_activa:
            # Si es búsqueda, se usa el AutoComplete para seleccionar
            if self.indice_deudor is None:
                # Mostrar un error si no se seleccionó un deudor
                self.view.show_error("Por favor, seleccione un deudor.")
                return
            nombre_deudor = self.deudores[self.indice_deudor].nombre
            telefono_deudor = self.deudores[self.indice_deudor].telefono
        else:
            # Si no es búsqueda, se usa el TextField para agregar un nuevo deudor
            nombre_deudor = self.nombre_input.value.strip()
            telefono_deudor = self.telefono_input.value.strip()
            if not self.validar_deudor(nombre_deudor, telefono_deudor):
                return
            # Guardar nuevo deudor en el sistema
            nuevo_deudor = Deudor(id=-1, nombre=nombre_deudor, telefono=telefono_deudor)
            self.deudores.append(nuevo_deudor)
            self.view.mostrar_error(f"Nuevo deudor agregado: {nombre_deudor}")

        if not nombre_deudor:
            self.view.mostrar_error("El nombre del cliente es obligatorio")
            return

        try:
            # Preparar datos
            productos = [
                {"id_producto": item.producto.id, "cantidad": item.cantidad}
                for item in self.productos_venta
            ]

            # Crear venta a crédito
            self.venta_routes.create_venta(
                {
                    "productos": productos,
                    "monto_pagado": 0,
                    "deudor_info": {
                        "nombre": nombre_deudor,
                        "telefono": telefono_deudor,
                    },
                }
            )

            # Limpiar estado y UI
            self.productos_venta.clear()
            self._actualizar_vista()
            self.view.limpiar_formulario()
            self._cerrar_dialog()
            self.view.mostrar_error("Venta a crédito registrada correctamente")

        except Exception as e:
            self.view.mostrar_error(f"Error al registrar la venta a crédito: {str(e)}")

    def validar_deudor(self, nombre: str, telefono: str):
        """Valida los datos de un deudor antes de guardarlo.

        Args:
            nombre (str): Nombre del deudor.
            telefono (str): Teléfono del deudor.
        """
        if not nombre:
            self.view.mostrar_error("El nombre del deudor es obligatorio.")
            return False

        if len(nombre) > 50:
            self.view.mostrar_error(
                "El nombre del deudor no puede exceder los 50 caracteres."
            )
            return False

        if telefono and (not telefono.isdigit() or len(telefono) > 10):
            self.view.mostrar_error(
                "El teléfono debe ser un número de hasta 10 dígitos."
            )
            return False

        return True

    def _cerrar_dialog(self):
        """Cierra el diálogo actual"""
        if self.deuda_dialog:
            self.deuda_dialog.open = False
            self.view.page.update()
