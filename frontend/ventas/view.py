# frontend/ventas/views.py

import flet as fl
from frontend.ventas.controller import VentasController

from icecream import ic


def mostrar_ventas(page: fl.Page, data_manager):
    controller = VentasController(page, data_manager)
    # Configuración de elementos de UI
    producto_list = fl.Dropdown(
        label='Producto',
        hint_text='Seleccione un producto',
        options=controller.filtrar_productos_con_stock(),
        expand=True,
    )
    ventas_list = fl.ListView(spacing=10, padding=10, expand=True)
    monto_input = fl.TextField(
        label='Monto… ($)',
        on_change=lambda e: controller.calcular_devolucion(e, monto_input),
        keyboard_type=fl.KeyboardType.NUMBER,
        expand=True,
    )

    # Conectar los eventos del controlador a los componentes de UI
    producto_list.on_change = lambda e: controller.handle_producto_seleccionado(
        e, producto_list, ventas_list, monto_input
    )

    # Crear la vista principal y añadir el contenido
    view = fl.View(
        '/ventas',
        [
            fl.AppBar(title=fl.Text('Registrar venta 🛒'), center_title=True),
            fl.Container(content=producto_list, padding=10),
            fl.Divider(),
            fl.Container(content=ventas_list, expand=True),
            fl.Divider(),
            fl.Container(
                content=fl.Column(
                    [
                        fl.Row(
                            [fl.Text('Total: '), controller.total_venta], alignment='spaceBetween'
                        ),
                        fl.Row([monto_input, fl.Container(width=20), controller.devolucion_text]),
                        fl.Row(
                            [
                                fl.ElevatedButton(
                                    'Vender',
                                    icon=fl.icons.ACCOUNT_BALANCE_WALLET,
                                    expand=True,
                                    on_click=lambda e: controller.handle_vender(
                                        monto_input, producto_list, ventas_list
                                    ),
                                )
                            ],
                            alignment='center',
                            expand=True,
                        ),
                    ]
                ),
                padding=10,
            ),
        ],
    )

    return view
