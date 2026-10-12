"""Estados de la Orden de Servicio, del Trabajo y de la Solicitud de Compra.

Los nombres son exactamente los del Glosario (sección «Estados del sistema»).
Las transiciones viven en una tabla separada para que OrdenDeServicio no crezca
con condicionales por cada estado (hallazgo SOLID H6).
"""
from __future__ import annotations

from enum import Enum

from autofix.dominio.compartido.errores import TransicionDeEstadoNoPermitida


class EstadoOrden(Enum):
    RECIBIDA = "Recibida"
    EN_DIAGNOSTICO = "En Diagnóstico"
    COTIZADA = "Cotizada"
    AUTORIZADA = "Autorizada"
    EN_REPARACION = "En Reparación"
    EN_ESPERA_DE_REFACCION = "En Espera de Refacción"
    PAUSADA_POR_RETIRO_DE_VEHICULO = "Pausada por Retiro de Vehículo"
    LISTA_PARA_ENTREGA = "Lista para Entrega"
    PAGADA = "Pagada"
    POR_COBRAR_CREDITO = "Por Cobrar (Crédito)"
    CERRADA = "Cerrada"
    CERRADA_SIN_REPARACION = "Cerrada sin Reparación"


class EstadoTrabajo(Enum):
    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En Progreso"
    COMPLETADO = "Completado"
    NO_AUTORIZADO = "No Autorizado"


class EstadoSolicitud(Enum):
    SOLICITADA = "Solicitada"
    DISPONIBLE = "Disponible"


O = EstadoOrden

TRANSICIONES_DE_ORDEN: dict[EstadoOrden, set[EstadoOrden]] = {
    O.RECIBIDA: {O.EN_DIAGNOSTICO},
    O.EN_DIAGNOSTICO: {O.COTIZADA},
    O.COTIZADA: {O.AUTORIZADA, O.CERRADA_SIN_REPARACION},
    O.AUTORIZADA: {O.EN_REPARACION, O.EN_ESPERA_DE_REFACCION},
    O.EN_REPARACION: {O.EN_ESPERA_DE_REFACCION, O.LISTA_PARA_ENTREGA},
    O.EN_ESPERA_DE_REFACCION: {O.AUTORIZADA, O.EN_REPARACION, O.PAUSADA_POR_RETIRO_DE_VEHICULO},
    O.PAUSADA_POR_RETIRO_DE_VEHICULO: {O.EN_ESPERA_DE_REFACCION, O.AUTORIZADA},
    O.LISTA_PARA_ENTREGA: {O.PAGADA, O.POR_COBRAR_CREDITO},
    O.PAGADA: {O.CERRADA},
    O.POR_COBRAR_CREDITO: {O.CERRADA},
    O.CERRADA: set(),
    O.CERRADA_SIN_REPARACION: set(),
}


def validar_transicion(actual: EstadoOrden, nuevo: EstadoOrden) -> None:
    if nuevo not in TRANSICIONES_DE_ORDEN[actual]:
        raise TransicionDeEstadoNoPermitida(
            f"La orden no puede pasar de «{actual.value}» a «{nuevo.value}»."
        )
