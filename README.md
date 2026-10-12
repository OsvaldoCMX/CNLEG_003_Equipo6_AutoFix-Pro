# AutoFix Pro — Diseño arquitectural del sistema (Unidad 3)

**Materia:** Componentes de Lógica de Negocio · FIME UANL
**Profesor:** Miguel Ángel Gómez Marroquín
**Equipo 6:**

| Integrante | Matrícula |
|---|---|
| Jesus Eduardo Moreno Osoria | 2136063 |
| Osvaldo Salvador Cárdenas Mejorado | 2141553 |
| Abraham Sandoval De León | 2136604 |

AutoFix Pro es un taller automotriz de diagnóstico y reparación. Este repositorio convierte el análisis de la Unidad 2 (BRD, User Stories con Gherkin, Glosario y BPMN) en una propuesta de arquitectura de software, que servirá de base para construir la aplicación en el proyecto final.

## Alcance del diseño

Proceso principal: **cotización → autorización → gestión de refacciones → entrega** (fases 2, 3, 4 y 6 del BPMN).

| CU | Caso de uso | Actor | User Stories | Flujo de rechazo o alterno |
|---|---|---|---|---|
| CU-01 | Generar cotización | Asesor de Servicio | US-004, US-005 | Más de $15,000 MXN pasa al Gerente; sin diagnóstico no se cotiza |
| CU-02 | Revisar cotización por el Gerente | Gerente de Taller | US-005 | Rechazo con observaciones → «Requiere Ajuste» |
| CU-03 | Registrar decisión del cliente | Asesor de Servicio | US-006, US-016 | Rechazo total; en flotilla el conductor no puede autorizar |
| CU-04 | Crear solicitud de compra | Técnico | US-010 | Trabajo no autorizado → se rechaza |
| CU-05 | Registrar entrega del vehículo | Asesor de Servicio | US-024 | Sin pago ni crédito → se rechaza |

## Decisiones principales (ADR)

Los cinco ADR completos están reunidos en un solo documento: [docs/adr/adr-autofix-pro.pdf](docs/adr/adr-autofix-pro.pdf).

| ADR | Decisión |
|---|---|
| ADR-001 | **Domain Model** para las operaciones que cambian datos y lecturas simples para las consultas |
| ADR-002 | Aggregates **Orden de Servicio**, **Cotización** y **Cliente**; Unidad de Trabajo cuando CU-03 modifica dos de ellos |
| ADR-003 | **Service Layer** con un servicio por caso de uso y **CQRS básico** |
| ADR-004 | **Repository** en términos del dominio: en memoria en esta fase y la base de datos del Data Center en el proyecto final |
| ADR-005 | La regla de $15,000 MXN como **política del dominio** |

## Estructura del repositorio

```
AutoFixPro-Arquitectura-U3/
├── docs/
│   ├── informe-arquitectura.pdf        Informe general (guía de la Unidad 3 llenada)
│   ├── adr/                            Los 5 ADR en un solo documento (.pdf)
│   ├── trazabilidad/                   Matriz de trazabilidad (.xlsx editable y .pdf)
│   ├── bitacora-ia/                    Bitácora de uso de IA (.pdf)
│   └── unidad2/                        Insumos de la Unidad 2 (BRD, User Stories, Glosario, BPMN)
├── diagramas/
│   ├── _estilo.iuml                    Estilo común de PlantUML
│   ├── dominio/                        Mapa de dominio (.puml, .pdf, .png)
│   └── uml/                            Diagrama de clases y 2 diagramas de secuencia (.puml, .pdf, .png)
├── src/autofix/                        Código base (entregable 06)
│   ├── dominio/                        Aggregates, entidades, Value Objects, reglas, eventos e interfaces de Repository
│   ├── aplicacion/                     Application Services, Commands, Queries, Unidad de Trabajo y puertos
│   ├── infraestructura/                Implementaciones en memoria (proyecto final: base de datos del Data Center)
│   └── composicion.py                  Único lugar donde se eligen las implementaciones concretas
├── tests/
│   ├── test_casos_de_uso.py            17 escenarios redactados desde los criterios Gherkin
│   ├── test_arquitectura.py            3 pruebas de la regla de dependencias entre capas
│   ├── escenarios.py                   Datos de apoyo para las pruebas
│   ├── reporte-pruebas.pdf             Escenarios, resultados esperados y obtenidos
│   └── evidencias/                     Capturas de la ejecución (prueba-01.png, prueba-02.png)
└── README.md
```

## Entregables

| # | Entregable | Ubicación |
|---|---|---|
| 01 | Informe de arquitectura | [docs/informe-arquitectura.pdf](docs/informe-arquitectura.pdf) |
| 02 | Mapa de dominio y diagrama de clases | [diagramas/dominio/mapa-dominio.pdf](diagramas/dominio/mapa-dominio.pdf) · [diagramas/uml/01-diagrama-clases.pdf](diagramas/uml/01-diagrama-clases.pdf) |
| 03 | Diagramas de secuencia (2) | [02-secuencia-registrar-decision.pdf](diagramas/uml/02-secuencia-registrar-decision.pdf) (flujo principal) · [03-secuencia-generar-cotizacion.pdf](diagramas/uml/03-secuencia-generar-cotizacion.pdf) (regla y excepción) |
| 04 | Matriz de trazabilidad | [docs/trazabilidad/matriz-trazabilidad.xlsx](docs/trazabilidad/matriz-trazabilidad.xlsx) · [.pdf](docs/trazabilidad/matriz-trazabilidad.pdf) |
| 05 | Bitácora de IA | [docs/bitacora-ia/bitacora-uso-ia.pdf](docs/bitacora-ia/bitacora-uso-ia.pdf) |
| 06 | Código base | [src/autofix](src/autofix) · [tests](tests) |
| 07 | Repositorio GitHub | Este repositorio |
| 08 | Presentación y defensa | En clase |

## Mapa de dominio

![Mapa de dominio](diagramas/dominio/mapa-dominio.png)

Cada recuadro grande es un Aggregate y su caja naranja es la raíz. Los elementos con borde punteado pertenecen al alcance del BRD y se construirán en el proyecto final.

## Tecnologías

- **Diagramas:** PlantUML.
- **Código base:** Python 3.10 o superior, solo con la biblioteca estándar (sin dependencias que instalar).
- **Persistencia:** en memoria en esta fase; en el proyecto final, la base de datos del Data Center que proporcionará el profesor (gestor por definir).

## Código base

La guía pide como entregable 06 una «estructura de carpetas y código mínimo que represente la arquitectura propuesta». Este código **no es la aplicación final**: es el esqueleto que demuestra que el diseño funciona y que las capas están bien separadas. Las clases tienen los mismos nombres que en los diagramas. La aplicación (interfaz, base de datos del Data Center y el resto de los casos de uso) se construirá en el proyecto final a partir de este diseño.

## Cómo revisar los archivos

1. **Documentos:** abrir los PDF de `docs/` y `diagramas/`. Se recomienda empezar por el informe y después revisar el documento de ADR.
2. **Ejecutar las pruebas** (requiere Python 3.10+), desde la carpeta del repositorio:

   ```bash
   python -m unittest discover -s tests -v
   ```

   Resultado esperado: `Ran 20 tests ... OK`. El detalle está en [tests/reporte-pruebas.pdf](tests/reporte-pruebas.pdf).

3. **Editar o regenerar un diagrama** (requiere Java y PlantUML, o el editor en línea de plantuml.com), desde la carpeta `diagramas`:

   ```bash
   java -jar plantuml.jar -tpng dominio/mapa-dominio.puml uml/*.puml
   ```

## Uso de IA

La IA (Claude, de Anthropic) se usó como apoyo en la revisión de la Unidad 2, el diseño, el código base y los diagramas. La [bitácora](docs/bitacora-ia/bitacora-uso-ia.pdf) registra 15 iteraciones en el orden de las etapas; cada prompt indica qué integrante lo escribió (Jesús: etapas 1 y 2; Abraham: etapas 3 a 5; Osvaldo: preparación de la Unidad 2, etapas 6 a 9, código base y pruebas), junto con el error o supuesto detectado y lo que el equipo aceptó, cambió o descartó.
