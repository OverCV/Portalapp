# backend/app/services/ventas.py
from datetime import datetime
from typing import List, Dict, Any, Optional
from backend.models.venta import Venta
from backend.models.venta_producto import VentaProducto
from backend.models.producto import Producto
from backend.models.deuda import Deuda
from backend.models.deudor import Deudor  # Asegúrate de importar Deudor
from backend.data.managers.csv_manager import CSVManager


class VentaService:
    def __init__(self, data_manager: CSVManager):
        self.data_manager = data_manager

    def create_venta(
        self,
        productos: List[Dict[str, Any]],
        monto_pagado: float,
        deudor_info: Optional[Dict[str, str]] = None,
    ) -> Venta:
        # 1. Validar productos y stock
        total_venta = 0
        for prod_info in productos:
            producto = self.data_manager.get_data_by_id(Producto, prod_info['id_producto'])
            if not producto:
                raise ValueError(f"Producto {prod_info['id_producto']} no existe")
            if producto.stock < prod_info['cantidad']:
                raise ValueError(f'Stock insuficiente para {producto.nombre}')
            total_venta += producto.precio * prod_info['cantidad']

        # 2. Validar monto si no es a crédito
        if not deudor_info and monto_pagado < total_venta:
            raise ValueError('Monto insuficiente')

        # 3. Crear venta
        venta = Venta(
            id=-1, fecha=datetime.now(), ganancia=min(monto_pagado, total_venta), total=total_venta
        )
        venta = self.data_manager.add_data(venta)

        # 4. Registrar productos y actualizar stock
        for prod_info in productos:
            # Registrar venta-producto
            venta_producto = VentaProducto(
                id=-1,
                id_venta=venta.id,
                id_producto=prod_info['id_producto'],
                cantidad=prod_info['cantidad'],
                fecha=datetime.now(),
            )
            producto_guardado = self.data_manager.add_data(venta_producto)

            # Actualizar stock
            producto = self.data_manager.get_data_by_id(Producto, prod_info['id_producto'])
            producto.stock -= prod_info['cantidad']
            self.data_manager.put_data(Producto, producto.id, {'stock': producto.stock})

        # 5. Crear deuda si aplica
        if deudor_info:
            # Crear o recuperar deudor
            deudor = Deudor(
                id=-1, nombre=deudor_info['nombre'], telefono=deudor_info.get('telefono')
            )
            deudor = self.data_manager.add_data(deudor)

            deuda = Deuda(
                id=-1,
                id_venta=venta.id,
                id_deudor=deudor.id,
                valor_deuda=total_venta - monto_pagado,
                creacion_deuda=datetime.now(),
            )
            self.data_manager.add_data(deuda)

        return venta

    # Implementar otros métodos según sea necesario...