class AppParams:
    APP_NAME: str = 'Portalapp'
    APP_TITLE: str = 'Portable App'
    APP_DESCRIPTION: str = 'App for managing products, sales, debtors and reports.'
    APP_VERSION: str = '1.0.0'
    APP_AUTHORS: str = 'Juan C. L. V. - Jhon E. R. L. - Seider S. G. - Over H. C. V.'
    APP_ASSETS_PATH: str = 'frontend/data/assets'


class AppRoutes:
    HOME: str = '/'
    PRODUCTOS: str = '/productos'
    VENTAS: str = '/ventas'
    DEUDORES: str = '/deudores'
    DEUDAS: str = '/deudas'
    REPORTES: str = '/reportes'
    NOT_FOUND: str = '/404'


class AppLabels:
    HOME: str = 'Inicio'
    PRODUCTOS: str = 'Productos'
    VENTAS: str = 'Ventas'
    DEUDAS: str = 'Deudas'
    DEUDORES: str = 'Deudores'
    REPORTES: str = 'Reportes'
    NOT_FOUND: str = 'Página no encontrada'
