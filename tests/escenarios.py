"""Datos y pasos previos compartidos por las pruebas.

Los pasos que no son parte de los 5 casos de uso detallados (recepción, diagnóstico,
inicio de trabajos, pago) se ejecutan directamente sobre el dominio dentro de una
Unidad de Trabajo, para preparar el escenario.
"""
from __future__ import annotations

import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from autofix.aplicacion.comandos import (  # noqa: E402
    GenerarCotizacion,
    RefaccionPropuesta,
    RegistrarDecisionDelCliente,
    TrabajoPropuesto,
)
from autofix.composicion import construir_aplicacion  # noqa: E402
from autofix.dominio.clientes.cliente import Cliente, ResponsableDeFlotilla, TipoCliente  # noqa: E402
from autofix.dominio.compartido.valores import Dinero, NumeroOrden, Placas  # noqa: E402
from autofix.dominio.ordenes.orden_de_servicio import OrdenDeServicio  # noqa: E402
from autofix.dominio.ordenes.valores import FormaDePago, Pago  # noqa: E402
from autofix.infraestructura.adaptadores import RelojFijo  # noqa: E402

INICIO = datetime(2026, 10, 12, 9, 0)        # lunes
PLACAS = "ABC-123-D"

CLIENTE_PARTICULAR = Cliente("CLI-001", "María López", TipoCliente.PARTICULAR)
CLIENTE_FLOTILLA = Cliente("CLI-002", "Transportes del Norte", TipoCliente.FLOTILLA,
                           empresa="Transportes del Norte",
                           responsable=ResponsableDeFlotilla("Carlos Ruiz", "8112345678", "carlos@tdn.mx"))

# Cotización de $6,300 (no requiere Gerente): balatas $2,400 + afinación $3,900
TRABAJOS_NORMALES = (
    TrabajoPropuesto("Cambio de balatas delanteras", Decimal("900"),
                     (RefaccionPropuesta("Juego de balatas", 1, Decimal("1500")),)),
    TrabajoPropuesto("Afinación mayor", Decimal("1500"),
                     (RefaccionPropuesta("Bujía", 4, Decimal("600")),)),
)
# Cotización de $18,500 (requiere Gerente)
TRABAJOS_COSTOSOS = (
    TrabajoPropuesto("Reparación de transmisión", Decimal("6500"),
                     (RefaccionPropuesta("Kit de embrague", 1, Decimal("12000")),)),
)


def nueva_app():
    return construir_aplicacion(RelojFijo(INICIO))


def orden_con_diagnostico(app, cliente: Cliente = CLIENTE_PARTICULAR) -> str:
    """Recepción (US-001), asignación (US-020) y diagnóstico (US-019)."""
    with app.uow as uow:
        uow.clientes.agregar(cliente)
        numero = uow.ordenes.siguiente_numero()
        orden = OrdenDeServicio(numero, cliente.id, cliente.es_de_flotilla, Placas(PLACAS),
                                "Ruido al frenar", app.reloj.ahora())
        orden.asignar_tecnico_para_diagnostico("Técnico Juan", app.reloj.ahora())
        orden.registrar_diagnostico("Balatas gastadas y bujías dañadas", app.reloj.ahora())
        uow.ordenes.agregar(orden)
        uow.confirmar()
    return str(numero)


def orden_cotizada(app, cliente: Cliente = CLIENTE_PARTICULAR, trabajos=TRABAJOS_NORMALES):
    numero = orden_con_diagnostico(app, cliente)
    resultado = app.cotizacion.generar_cotizacion(GenerarCotizacion(numero, trabajos))
    return numero, resultado.id_cotizacion


def orden_autorizada(app, lineas=(1, 2)):
    numero, id_cot = orden_cotizada(app)
    app.autorizacion.registrar_decision_del_cliente(
        RegistrarDecisionDelCliente(id_cot, tuple(lineas), "María López"))
    return numero, id_cot


def completar_y_pagar(app, numero: str) -> None:
    """US-008 y US-014: se ejecutan los trabajos y Caja registra el pago."""
    with app.uow as uow:
        orden = uow.ordenes.obtener(NumeroOrden(numero))
        for trabajo in orden.trabajos:
            if trabajo.esta_autorizado:
                orden.iniciar_trabajo(trabajo.id, app.reloj.ahora())
                orden.completar_trabajo(trabajo.id, app.reloj.ahora())
        orden.registrar_pago(Pago(orden.total_autorizado, FormaDePago.TARJETA, app.reloj.ahora()))
        uow.ordenes.guardar(orden)
        uow.confirmar()


def orden(app, numero: str) -> OrdenDeServicio:
    return app.almacen.datos.ordenes[numero]


__all__ = ["Dinero"]
