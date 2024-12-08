import flet as ft
import flet as ft
from backend.data.managers.csv_manager import CSVManager
from backend.models.deudor import Deudor
from frontend.deudores.presenter import DeudoresPresenter
from backend.models.deudor import Deudor
from frontend.deudores.presenter import DeudoresPresenter


def mostrar_deudores(page: ft.Page, data_manager: CSVManager) -> ft.View:
    view = DeudoresView(page, data_manager)
    return view.build()


class DeudoresView:
    def __init__(self, page: ft.Page, data_manager: CSVManager):
        self.page = page
        self.presenter = DeudoresPresenter(self, data_manager)
        self.deudores_list = ft.ListView(spacing=10, padding=20, expand=True)
        self.init_view()

    def mostrar_modal_deudas(self, deudor_id: int):
        deudas = self.presenter.obtener_deudas_de_deudor(deudor_id)
        contenido = ft.Column(
            [
                ft.Text(f'Deuda #{d.id} por ${d.valor_deuda} pesos.', weight=ft.FontWeight.W_500)
                for d in deudas
            ],
            spacing=10,
        )
        dialog = ft.AlertDialog(
            title=ft.Text('Detalle de deudas'),
            content=contenido,
            actions=[
                ft.TextButton('Cerrar', on_click=lambda e: self.cerrar_dialogo()),
            ],
        )
        self.page.dialog = dialog
        self.page.dialog.open = True
        self.page.update()

    def abrir_modal_abono_deudor(self, deudor_id: int):
        input_abono = ft.TextField(label='Ingrese el monto del abono', keyboard_type='number')

        def confirmar_abono(e):
            if input_abono.value.isdigit():
                valor_abono = int(input_abono.value)
                saldo_actual = self.presenter.saldo_de_deudor(deudor_id)
                if 0 < valor_abono <= saldo_actual:
                    self.presenter.registrar_abono_deudor(deudor_id, valor_abono)
                    self.cerrar_dialogo()

        dialog = ft.AlertDialog(
            title=ft.Text('Registrar Abono'),
            content=input_abono,
            actions=[
                ft.TextButton('Cancelar', on_click=lambda e: self.cerrar_dialogo()),
                ft.TextButton('Confirmar', on_click=confirmar_abono),
            ],
        )
        self.page.dialog = dialog
        self.page.dialog.open = True
        self.page.update()

    def cerrar_dialogo(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()

    def crear_panel_deudor(self, deudor: Deudor):
        saldo_total = self.presenter.saldo_de_deudor(deudor.id)
        abonos_de_deudor = self.presenter.obtener_abonos_de_deudor(deudor.id)

        # Historial de abonos
        abonos_content = (
            ft.Column(
                [
                    ft.Text('Historial de abonos:', weight=ft.FontWeight.W_700),
                ]
                + [
                    ft.Text(
                        f"Abono de ${a.valor_abono} en {a.fecha_abono.strftime('%Y-%m-%d %H:%M:%S')}",
                        size=12,
                    )
                    for a in abonos_de_deudor
                ],
                spacing=5,
            )
            if abonos_de_deudor
            else ft.Text('No hay abonos registrados.', size=12, color=ft.colors.GREY_600)
        )

        # Content del panel
        panel_content = ft.Column([abonos_content], spacing=15)

        # Header con el saldo total y botón de abonar
        header = ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.icons.PERSON, size=24),
                    width=40,
                    height=40,
                    bgcolor=ft.colors.SECONDARY_CONTAINER,
                    border_radius=20,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    [
                        ft.Text(deudor.nombre, weight=ft.FontWeight.W_500),
                        ft.TextButton(
                            text=f'Saldo Total: ${saldo_total}',
                            on_click=lambda e, d_id=deudor.id: self.mostrar_modal_deudas(d_id),
                        ),
                    ],
                    alignment=ft.alignment.center,
                    spacing=2,
                ),
                ft.Column(
                    [
                        ft.IconButton(
                            icon=ft.icons.MONEY_OFF,
                            icon_color='white',
                            bgcolor='red',
                            icon_size=20,
                            width=35,
                            height=35,
                            style=ft.ButtonStyle(shape=ft.CircleBorder()),
                            on_click=lambda e, d_id=deudor.id: self.abrir_modal_abono_deudor(d_id),
                        ),
                    ],
                    alignment=ft.alignment.center,
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        return ft.ExpansionPanel(
            header=header,
            content=panel_content,
            expanded=False,
        )

    def init_view(self):
        self.deudores_list.controls.clear()
        deudores = self.presenter.obtener_deudores_con_deuda()
        panel_list = ft.ExpansionPanelList(
            expand=False,
            controls=[self.crear_panel_deudor(deudor) for deudor in deudores],
        )
        self.deudores_list.controls.append(panel_list)
        self.page.update()

    def build(self):
        return ft.View(
            '/deudores',
            [
                ft.AppBar(
                    title=ft.Text('Mis deudores 💸'),
                    center_title=True,
                ),
                ft.Container(
                    content=self.deudores_list,
                    padding=ft.padding.all(1),
                    expand=True,
                ),
            ],
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

    def actualizar_vista(self):
        self.init_view()
        self.page.update()
