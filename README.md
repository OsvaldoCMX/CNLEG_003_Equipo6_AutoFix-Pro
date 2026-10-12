# AutoFix Pro — Diseño arquitectural del sistema (Unidad 3)

**Materia:** Componentes de Lógica de Negocio · FIME UANL
**Profesor:** Miguel Ángel Gómez Marroquín
**Equipo 6:**

| Integrante | Matrícula |
|---|---|
| Jesus Eduardo Moreno Osoria | 2136063 |
| Osvaldo Salvador Cárdenas Mejorado | 2141553 |
| Abraham Sandoval De León | 2136604 |

Diseño arquitectural del sistema del taller automotriz AutoFix Pro.

## Estructura del repositorio

```
AutoFixPro-Arquitectura-U3/
├── docs/
│   ├── informe-arquitectura.pdf        Informe general (guía de la Unidad 3 llenada)
│   ├── resumen-unidad3.pdf             Resumen integral de la unidad (el que se sube a Netacad)
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
