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
    """Muestra la vista de productos inicializada.

    Esta función crea una instancia de la vista de productos (`ProductosView`) y la devuelve. 
    Es utilizada para mostrar la lista de productos en la página proporcionada, 
    utilizando el administrador de datos proporcionado.

    Args:
        page (ft.Page): La página de Flet donde se renderiza la vista de productos.
        sql_manager (CSVManager): El administrador de base de datos para gestionar los productos.

    Returns:
        ft.View: La vista de productos que contiene los controles para mostrar y gestionar los productos.
    """
    view = ProductosView(page, sql_manager)
    return view.view  # Retornamos la vista inicializada


class ProductosView:
    """Representa la vista de productos, mostrando una lista de productos y proporcionando
    la funcionalidad de búsqueda, agregar, editar y eliminar productos.

    Args:
        page (ft.Page): La página principal donde se renderiza la vista.
        sql_manager (CSVManager): El administrador para manejar los datos de productos.
    """
    def __init__(self, page: ft.Page, sql_manager: CSVManager):
        """Inicializa la vista de productos, configurando el presentador y la interfaz de usuario.

        Args:
            page (ft.Page): La página donde se presentarán los datos.
            sql_manager (CSVManager): El administrador para manejar los datos de productos.
        """
        self.page = page
        self.presenter: ProductosPresenter = ProductosPresenter(self, sql_manager)
        self.productos_list = ft.ListView(
            expand=True,
        )
        self.init_view()

    def init_view(self):
        """Inicializa la vista, construyendo la interfaz de usuario y la funcionalidad de búsqueda.

        Returns:
            ft.View: La vista de la página con la lista de productos y los controles de búsqueda.
        """
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
        """Construye la barra de aplicación con el título y el botón para agregar un nuevo producto.

        Returns:
            ft.AppBar: La barra de aplicación con las acciones configuradas.
        """
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
        """Maneja la acción de búsqueda de productos al cambiar el valor del campo de búsqueda.

        Args:
            e: El evento que contiene el nuevo valor de búsqueda.
        """
        self.presenter.search_productos(e.control.value)

    def __build_content(self):
        """Construye el contenido principal de la vista, incluyendo el campo de búsqueda y la lista de productos.

        Returns:
            ft.Container: El contenedor que incluye el campo de búsqueda y la lista de productos.
        """
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
        """Actualiza la lista de productos en la vista.

        Obtiene los productos del presentador y los agrega a la lista de controles de la vista.
        """
        productos = self.presenter.load_productos()
        self.productos_list.controls = [
            ProductoCard(p, on_edit=self.show_product_dialog, on_delete=self.handle_delete)
            for p in productos
        ]
        self.page.update()

    def show_error(self, message: str):
        """Muestra un mensaje de error en la vista.

        Args:
            message (str): El mensaje de error a mostrar.
        """
        self.page.open(ft.SnackBar(content=ft.Text(message)))

    def handle_delete(self, producto: Producto):
        """Maneja la acción de eliminar un producto, mostrando un cuadro de diálogo de confirmación.

        Args:
            producto (Producto): El producto que se desea eliminar.
        """
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
        """Muestra un cuadro de diálogo para agregar o editar un producto.

        Si el producto es proporcionado, se editará. Si no, se agregará un nuevo producto.

        Args:
            producto (Producto, optional): El producto a editar. Si es None, se creará un nuevo producto.
        """
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
        coste_field = ft.TextField(
            label='Coste',
            value=str(producto.coste) if producto else '',
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
                coste_field.value,
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
                    coste_field,
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
