# productos/view.py
import shutil
import uuid
import flet as ft
from frontend.app.enums.app import AppParams, AppRoutes
from backend.data.managers.csv_manager import CSVManager

from frontend.productos.components import ProductoCard
from frontend.productos.presenter import ProductosPresenter

from backend.models.producto import Producto


def mostrar_productos(page: ft.Page, sql_manager: CSVManager) -> ft.View:
    view = ProductosView(page, sql_manager)
    return view.view  # Retornamos la vista inicializada


class ProductosView:
    def __init__(self, page: ft.Page, sql_manager: CSVManager):
        self.page = page
        self.presenter = ProductosPresenter(self, sql_manager)
        self.productos_list = ft.ListView(
            expand=True,
        )
        self.init_view()

    def init_view(self):
        self.view = ft.View(
            AppRoutes.PRODUCTOS,
            [
                self.__build_app_bar(),
                self.__build_content(),
            ],
            padding=0,
        )
        self.refresh_productos()
        return self.view

    def __build_app_bar(self):
        return ft.AppBar(
            title=ft.Text('Mis productos 📦'),
            center_title=True,
            actions=[
                ft.IconButton(
                    icon=ft.icons.ADD,
                    tooltip='Agregar producto',
                    on_click=lambda _: self.show_product_dialog(),
                )
            ],
        )

    def handle_search(self, e):
        self.presenter.search_productos(e.control.value)

    def __build_content(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.TextField(
                        prefix_icon=ft.icons.SEARCH,
                        hint_text='Buscar productos...',
                        # Quitamos el expand de aquí
                        on_change=lambda e: self.handle_search(e),
                        border_radius=20,
                    ),
                    ft.Container(  # Agregamos un container para el GridView
                        content=self.productos_list,
                        expand=True,  # Este expand es clave
                    ),
                ],
                spacing=10,
                expand=True,  # La columna también debe expandirse
            ),
            padding=ft.padding.only(left=20, right=20, top=10),
            expand=True,  # El container |principal también se expande
        )

    def refresh_productos(self):
        productos = self.presenter.load_productos()
        self.productos_list.controls = [
            ProductoCard(p, on_edit=self.show_product_dialog, on_delete=self.handle_delete)
            for p in productos
        ]
        self.page.update()

    def show_error(self, message: str):
        self.page.open(ft.SnackBar(content=ft.Text(message)))

    def handle_delete(self, producto: Producto):
        def confirm_delete(e):
            self.presenter.delete_producto(producto)
            dialog.open = False
            self.page.update()
            self.refresh_productos()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text('Confirmar eliminación'),
            content=ft.Text(f'¿Estás seguro de eliminar {producto.nombre}?'),
            actions=[
                ft.TextButton(
                    'Cancelar',
                    on_click=lambda e: (setattr(dialog, 'open', False), self.page.update()),
                ),
                ft.TextButton(
                    'Eliminar',
                    on_click=confirm_delete,
                    style=ft.ButtonStyle(color=ft.colors.ERROR),
                ),
            ],
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def show_product_dialog(self, producto: Producto = None):
        # Variable para almacenar la ruta de la imagen temporalmente
        imagen_seleccionada = None

        # Si estamos editando, inicializamos con la imagen actual
        if producto:
            imagen_seleccionada = producto.imagen_ruta

        def on_file_picked(e: ft.FilePickerResultEvent):
            nonlocal imagen_seleccionada
            if not e.files or not e.files[0].path:
                return

            file_path = e.files[0].path
            new_filename = f"{uuid.uuid4()}.{file_path.split('.')[-1]}"
            new_path = f'{AppParams.APP_ASSETS_PATH}/productos/{new_filename}'

            # Copiar archivo
            shutil.copy(file_path, new_path)
            # Actualizamos la imagen seleccionada
            imagen_seleccionada = new_filename

        image_picker = ft.FilePicker(on_result=on_file_picked)
        self.page.overlay.append(image_picker)

        nombre_field = ft.TextField(
            label='Nombre', value=producto.nombre if producto else '', autofocus=True
        )
        precio_field = ft.TextField(
            label='Precio',
            value=str(producto.precio) if producto else '',
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        stock_field = ft.TextField(
            label='Stock',
            value=str(producto.stock) if producto else '',
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        def handle_save(e):
            # Creamos o actualizamos el producto
            success = self.presenter.save_producto(
                nombre_field.value,
                precio_field.value,
                stock_field.value,
                imagen_seleccionada,  # Pasamos la imagen actual o la nueva
                producto.id if producto else None,
            )

            if success:
                dialog.open = False
                # Removemos el file picker del overlay
                self.page.overlay.remove(image_picker)
                self.page.update()
                # Refrescamos la lista de productos
                self.refresh_productos()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text('Editar producto' if producto else 'Nuevo producto'),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.icons.ADD_A_PHOTO,
                                    on_click=lambda _: (
                                        image_picker.pick_files(),
                                        print(image_picker),
                                    ),
                                ),
                                bgcolor=ft.colors.SECONDARY_CONTAINER,
                                border_radius=8,
                                padding=8,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    nombre_field,
                    precio_field,
                    stock_field,
                ],
                tight=True,
                spacing=20,
            ),
            actions=[
                ft.TextButton(
                    'Cancelar',
                    on_click=lambda e: (setattr(dialog, 'open', False), self.page.update()),
                ),
                ft.TextButton('Guardar', on_click=handle_save),
            ],
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
