# Casos de Uso - Sistema Marck

## Actores
- Administrador
- Operador
- Afiliado
- Sistema (BD)

## UC-01: Iniciar sesión
Actor: Operador/Administrador
Propósito: Autenticar al usuario.
Precondición: Cuenta existente.
Flujo principal:
1. Ingresar usuario/contraseña.
2. Validar credenciales.
3. Mostrar pantalla principal.
Alternativas:
- Credenciales inválidas: mensaje de error.

## UC-02: Gestionar Afiliados
Actor: Operador
Propósito: Crear/editar/buscar afiliados.
Precondición: Usuario autenticado.
Flujo principal:
1. Abrir módulo Afiliados.
2. Crear o editar datos.
3. Guardar en BD.

## UC-03: Registrar Ingreso/Pago
Actor: Operador
Propósito: Registrar cobros y movimientos de caja.
Precondición: Usuario autenticado.
Flujo principal:
1. Abrir módulo Caja/Ingresos.
2. Seleccionar afiliado y concepto.
3. Registrar y persistir movimiento.

## UC-04: Gestionar Alquileres
Actor: Operador
Propósito: Registrar reservas y pagos por alquileres.
Flujo principal:
1. Crear alquiler con fecha, cliente, monto.
2. Guardar y actualizar calendario.

## UC-05: Gestionar Eventos/Calendario
Actor: Operador/Administrador
Propósito: Crear y listar eventos.
Flujo principal:
1. Crear evento.
2. Guardar y mostrar en calendario.

## UC-06: Ver Historial y Generar Informe
Actor: Administrador/Operador
Propósito: Consultar historial de afiliado y exportar reportes.
Flujo principal:
1. Seleccionar afiliado.
2. Exportar informe (CSV/PDF).