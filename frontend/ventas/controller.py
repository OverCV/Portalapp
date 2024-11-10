# frontend/controllers/ventas_controller.py

import flet as fl
from backend.app.routes.ventas import (
    registrar_venta,
    obtener_productos_disponibles,
    obtener_total_venta,
)

from backend.models.venta_producto import VentaProducto
from backend.models.producto import Producto


class VentasController:
    def __init__(self, page, data_manager):
        self.page = page
        self.data_manager = data_manager
        self.venta_productos: list[VentaProducto] = []
        self.productos: list[Producto] = obtener_productos_disponibles(data_manager)
        self.total_venta = fl.Text(value='0', color='blue')
        self.devolucion_text = fl.Text(
            '$0.00', size=16, weight=fl.FontWeight.BOLD, color=fl.colors.BLUE
        )
        self.monto_insuficiente_dialog = fl.AlertDialog(
            title=fl.Text('Monto insuficiente'),
            content=fl.Text('El monto ingresado es insuficiente para realizar la venta.'),
            actions=[fl.TextButton('OK', on_click=lambda e: self.close_dialog())],
            open=False,
        )

    def filtrar_productos_con_stock(self):
        # Filtrar productos con stock > 0 y crear opciones para el Dropdown
        return [
            fl.dropdown.Option(key=p.id, text=p.nombre) for p in self.productos if int(p.stock) > 0
        ]

    def handle_producto_seleccionado(self, e, producto_list, ventas_list, monto_input):
        producto_seleccionado = next(
            (p for p in self.productos if p.id == producto_list.value), None
        )
        if producto_seleccionado:
            venta_existente = next(
                (v for v in self.productos if v.nombre == producto_seleccionado.nombre),
                None,
            )
            if venta_existente:
                # Si el producto ya está en la lista y tiene stock suficiente, incrementa la cantidad
                if venta_existente['cantidad'] < int(producto_seleccionado['stock']):
                    venta_existente['cantidad'] += 1
                else:
                    # Mostrar un SnackBar si se intenta exceder el stock
                    snack = fl.SnackBar(
                        content=fl.Text(
                            f"Stock insuficiente para {producto_seleccionado['nombre']}"
                        ),
                        action='OK',
                    )
                    self.page.overlay.append(snack)
                    snack.open = True  # Asegura que el SnackBar se abra
                    self.page.update()
            else:
                # Añadir el producto a la lista de ventas si aún no está
                self.venta_productos.append(
                    {
                        'id': producto_seleccionado['id'],
                        'nombre': producto_seleccionado['nombre'],
                        'cantidad': 1,
                        'precio': float(producto_seleccionado['precio']),
                        'stock': int(producto_seleccionado['stock']),
                    }
                )
            self.actualizar_lista_ventas(ventas_list, monto_input)

    def actualizar_lista_ventas(self, ventas_list, monto_input):
        ventas_list.controls.clear()
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
        for venta in self.venta_productos:
            ventas_list.controls.append(
                fl.Row(
                    [
                        fl.Text(venta['nombre']),
                        fl.Row(
                            [
                                fl.IconButton(
                                    icon=fl.icons.REMOVE_CIRCLE_OUTLINE_ROUNDED,
                                    selected_icon=fl.icons.REMOVE_CIRCLE,
                                    on_click=lambda e, v=venta: self.modificar_cantidad(
                                        v, -1, ventas_list, monto_input
                                    ),
                                ),
                                fl.Text(str(venta['cantidad'])),
                                fl.IconButton(
                                    icon=fl.icons.ADD_CIRCLE_OUTLINE_ROUNDED,
                                    selected_icon=fl.icons.ADD_CIRCLE,
                                    on_click=lambda e, v=venta: self.modificar_cantidad(
                                        v, 1, ventas_list, monto_input
                                    ),
                                ),
                            ]
                        ),
                        fl.Text(f"{venta['precio'] * venta['cantidad']}"),
                    ],
                    alignment='spaceBetween',
                )
            )
        ventas_list.update()
        self.actualizar_total(monto_input)  # Recalcula la devuelta después de actualizar la lista

    def modificar_cantidad(self, venta, delta, ventas_list, monto_input):
        # Si intenta aumentar la cantidad más allá del stock disponible, muestra mensaje
        if delta > 0 and venta['cantidad'] >= venta['stock']:
            snack = fl.SnackBar(
                content=fl.Text(f"Stock insuficiente para {venta['nombre']}"),
                action='OK',
            )
            self.page.overlay.append(snack)
            snack.open = True  # Asegura que el SnackBar se abra
            self.page.update()
            return
        venta['cantidad'] = max(1, venta['cantidad'] + delta)
        self.actualizar_lista_ventas(
            ventas_list, monto_input
        )  # Recalcula devuelta después de modificar cantidades

    def actualizar_total(self, monto_input):
        total = obtener_total_venta(self.venta_productos)
        self.total_venta.value = f'{total:.2f}'
        self.total_venta.update()
        # Recalcula la devuelta si hay un monto ingresado
        if monto_input:
            self.calcular_devolucion(None, monto_input)

    def calcular_devolucion(self, e, monto_input):
        try:
            monto = int(monto_input.value) if monto_input.value else 0
            devolucion = monto - float(self.total_venta.value)
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
        devolucion = float(self.devolucion_text.value.replace('$', ''))
        if devolucion < 0:
            self.monto_insuficiente_dialog.open = True
            self.page.dialog = self.monto_insuficiente_dialog
            self.page.update()
            return
        if self.venta_productos:
            # venta_data = {
            #     'fecha_venta': datetime.now().isoformat(),
            #     'ganancia': obtener_total_venta(self.productos_venta),
            # }
            registrar_venta(self.data_manager, self.venta_productos)
            self.venta_productos.clear()
            self.actualizar_lista_ventas(ventas_list, monto_input)
            # Mostrar mensaje de confirmación de venta
            self.page.overlay.append(
                fl.SnackBar(content=fl.Text('Venta registrada correctamente'), action='OK')
            )
            self.page.update()
            # Refrescar la lista de productos después de la venta
            self.productos = obtener_productos_disponibles(self.data_manager)
            producto_list.options = self.filtrar_productos_con_stock()
            producto_list.update()

    def close_dialog(self):
        self.monto_insuficiente_dialog.open = False
        self.page.update()
