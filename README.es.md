# Agent Compensation Map

[Français](README.md) · [English](README.en.md)

**Dos llamadas sin respuesta pueden dejar cero, uno o dos efectos. Deshacer puede exigir observar primero.**

Reconstruye mundos posibles, busca un árbol condicional de compensación y reproduce cada rama por separado. Planifica **sin ejecutar acciones externas**. Una notificación enviada no se convierte en un botón ficticio para deshacerla.

![Plan condicional sintético y tres recorridos verificados](docs/preview-fr.png)

## Probar

Python 3.11 o posterior, biblioteca estándar; sin clave.

```sh
python3 -m compensation_map serve --lang es
```

Abrir `http://127.0.0.1:8769/?lang=es`. Dos intentos de pago ambiguos generan tres mundos. El plan observa su número, compensa cero/una/dos veces según la lectura, cancela el pedido simulado y libera stock. Coste máximo declarado: **9 unidades**, verificado en cada mundo. Sin observación o con notificación irreversible se requiere revisión.

```sh
python3 -m compensation_map demo > prueba.json
python3 -m compensation_map plan compensation_map/examples/ambiguous-charge.json
```

`pip install .` ofrece `compensation-map`. Interfaz y mensajes FR/EN/ES; identificadores conservados.

## Modelo

- `domains` e `initial`: hechos finitos tipados; distingue booleanos y enteros.
- `operations`: efectos originales. `confirmed` confirma el efecto; `unknown` conserva ambas opciones; `not_applied` confirma ausencia de efecto; `not_started` indica que no se intentó. Un error de red debe seguir **unknown**, no suponerse sin efecto.
- `compensations`: operaciones declaradas, precondiciones y costes. No inventa inversas.
- `observations`: revela hechos y crea ramas. Las precondiciones deben cumplirse en todos los mundos de la rama.
- `goal`: estado deseado. Observaciones explícitas reducen incertidumbre; se rechazan contradicciones.

La búsqueda AND/OR minimiza **coste del peor recorrido dentro de la profundidad dada**, sin probabilidades supuestas. Un intérprete independiente recorre cada mundo, comprueba precondiciones y objetivo, y recalcula costes. La prueba incluye caso fuente, SHA-256, árbol y recorridos.

`minimum_cost_within_depth_proven` solo es verdadero al completar la exploración acotada. Límites de tiempo/profundidad no prueban imposibilidad general. Si el objetivo exige cambiar un hecho que ninguna compensación toca, un testigo explica imposibilidad **dentro del modelo declarado**.

## MCP de solo lectura

```sh
python3 -m compensation_map mcp
```

Configurar la ruta absoluta del Python instalado:

```json
{
  "mcpServers": {
    "compensation-map": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "compensation_map", "mcp"]
    }
  }
}
```

`compensation_plan` acepta `{ "case": ... }` y devuelve datos estructurados. Anotado solo lectura, no destructivo y cerrado al mundo externo. Inicialización, descubrimiento y llamadas probados con **SDK MCP oficial 1.32.1**, protocolo 2025-11-25. Sin instalación real OpenClaw/Hermes validada ni conversión automática de sus errores a este modelo.

## Existente y límites

[Temporal ya documenta sagas y compensaciones](https://temporal.io/blog/compensating-actions-part-of-a-complete-breakfast-with-sagas); existe también [planificación condicional](https://unified-planning.readthedocs.io/en/latest/plan_representation.html). No se inventan esos métodos. Se muestra **efecto ambiguo → creencias → observación necesaria → compensación condicional → reproducción independiente**. Complementa [Agent Commerce Ledger](https://github.com/gbesse/agent-commerce-ledger) y [Jev Proxy](https://github.com/gbesse/jev-proxy).

Hasta doce hechos, doce pasos, sesenta y cuatro mundos y nueve niveles. Las futuras acciones/lecturas se suponen deterministas y fiables en el modelo. Sin resolver concurrencia externa, autorización humana ni fallos de compensación. Costes declarados, no dinero ni latencia medidos. Ejemplo sintético; sin pagos, mensajes ni inventario reales modificados. Sin demostrar restauración de producción ni superioridad SOTA.

## Verificar

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run test:mcp
npm run format:check
```

Trece pruebas: creencias, ramas, coste, irreversibilidad, profundidad, contradicciones y MCP stdio. SDK oficial adicional; navegador FR/EN/ES y móvil; CI Python 3.11/3.12 y rueda fuera de fuentes. Salida 1: requiere revisión; 2: entrada no válida. Licencia MIT; alfa de investigación.
