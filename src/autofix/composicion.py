"""Raíz de composición: único lugar donde se eligen las implementaciones concretas.

Cambiar la memoria por la base de datos del Data Center solo modifica este archivo
y la carpeta infraestructura; dominio y aplicación no se tocan (principio D, ADR-004).
"""
from __future__ import annotations

from dataclasses import dataclass

from autofix.aplicacion.consultas.consultas import (
    ManejadorConsultarEstadoDeOrden,
    ManejadorListarCotizacionesPendientesDeAprobacion,
    ManejadorListarSolicitudesPendientes,
)
from autofix.aplicacion.puertos import Reloj
from autofix.aplicacion.servicios.servicio_de_aprobacion_gerencial import ServicioDeAprobacionGerencial
from autofix.aplicacion.servicios.servicio_de_autorizacion import ServicioDeAutorizacion
from autofix.aplicacion.servicios.servicio_de_cotizacion import ServicioDeCotizacion
from autofix.aplicacion.servicios.servicio_de_entrega import ServicioDeEntrega
from autofix.aplicacion.servicios.servicio_de_refacciones import ServicioDeRefacciones
from autofix.dominio.compartido.calendario import CalendarioHabil
from autofix.dominio.cotizaciones.politica_de_aprobacion import PoliticaPorMontoDeCotizacionInicial
from autofix.dominio.servicios.verificador_de_autorizante import VerificadorDeAutorizante
from autofix.infraestructura.adaptadores import (
    GeneradorDeDocumentosSimulado,
    PublicadorDeAlertasInternas,
    RelojDelSistema,
)
from autofix.infraestructura.memoria.almacen import AlmacenEnMemoria
from autofix.infraestructura.memoria.lector import LectorDeOrdenesEnMemoria
from autofix.infraestructura.memoria.unidad_de_trabajo import UnidadDeTrabajoEnMemoria


@dataclass
class Aplicacion:
    almacen: AlmacenEnMemoria
    reloj: Reloj
    publicador: PublicadorDeAlertasInternas
    uow: UnidadDeTrabajoEnMemoria
    cotizacion: ServicioDeCotizacion
    aprobacion_gerencial: ServicioDeAprobacionGerencial
    autorizacion: ServicioDeAutorizacion
    refacciones: ServicioDeRefacciones
    entrega: ServicioDeEntrega
    consultar_estado: ManejadorConsultarEstadoDeOrden
    solicitudes_pendientes: ManejadorListarSolicitudesPendientes
    cotizaciones_por_aprobar: ManejadorListarCotizacionesPendientesDeAprobacion


def construir_aplicacion(reloj: Reloj | None = None) -> Aplicacion:
    reloj = reloj or RelojDelSistema()
    almacen = AlmacenEnMemoria()
    uow = UnidadDeTrabajoEnMemoria(almacen)
    publicador = PublicadorDeAlertasInternas()
    lector = LectorDeOrdenesEnMemoria(almacen, CalendarioHabil())
    return Aplicacion(
        almacen=almacen, reloj=reloj, publicador=publicador, uow=uow,
        cotizacion=ServicioDeCotizacion(uow, PoliticaPorMontoDeCotizacionInicial(), reloj, publicador,
                                        GeneradorDeDocumentosSimulado()),
        aprobacion_gerencial=ServicioDeAprobacionGerencial(uow, reloj, publicador),
        autorizacion=ServicioDeAutorizacion(uow, VerificadorDeAutorizante(), reloj, publicador),
        refacciones=ServicioDeRefacciones(uow, reloj, publicador),
        entrega=ServicioDeEntrega(uow, reloj, publicador),
        consultar_estado=ManejadorConsultarEstadoDeOrden(lector),
        solicitudes_pendientes=ManejadorListarSolicitudesPendientes(lector, reloj),
        cotizaciones_por_aprobar=ManejadorListarCotizacionesPendientesDeAprobacion(lector),
    )
