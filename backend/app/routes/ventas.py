# backend/app/routes/ventas.py
from typing import List, Dict, Any
from backend.models.venta import Venta
from backend.app.services.ventas import VentaService


class VentaRoutes:
    def __init__(self, service: VentaService):
        self.service = service

    def create_venta(self, data: Dict[str, Any]) -> Venta:
        """Endpoint para crear una venta"""
        return self.service.create_venta(
            productos=data['productos'],
            monto_pagado=data['monto_pagado'],
            deudor_info=data.get('deudor_info'),  # Añadimos esto para ventas a crédito
        )

    def get_ventas(self) -> List[Venta]:
        """Endpoint para obtener todas las ventas"""
        return self.service.get_ventas()

    def get_venta(self, venta_id: int) -> Venta:
        """Endpoint para obtener una venta específica"""
        return self.service.get_venta(venta_id)

    def update_venta(self, venta_id: int, data: Dict[str, Any]) -> Venta:
        """Endpoint para actualizar una venta"""
        return self.service.update_venta(venta_id, data)