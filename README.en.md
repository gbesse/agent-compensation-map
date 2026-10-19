# Agent Compensation Map

[Français](README.md) · [Español](README.es.md)

**Two unanswered calls can mean zero, one or two effects. Undo may require observation first.**

The engine reconstructs possible worlds from a trace, finds a contingent compensation tree and independently replays every branch. It plans **without executing external actions**. A sent notification never becomes a fictional unsend button.

![Synthetic contingent plan and three verified paths](docs/preview-fr.png)

## Try it

Python 3.11 or newer, standard library only; no key.

```sh
python3 -m compensation_map serve --lang en
```

Open `http://127.0.0.1:8769/?lang=en`. Two ambiguous payment attempts create three possible worlds. The plan reads their count, compensates zero/one/two times depending on the observation, cancels the simulated order and releases stock. Declared worst-case cost: **9 units**, checked in every world. Remove observation or enable the irreversible notification to expose the review requirement.

```sh
python3 -m compensation_map demo > evidence.json
python3 -m compensation_map plan compensation_map/examples/ambiguous-charge.json
```

`pip install .` also provides `compensation-map`. FR/EN/ES UI and CLI messages; action identifiers stay unchanged.

## Compensation model

- `domains` and `initial` define finite typed facts; booleans and integers remain distinct.
- `operations` declares original effects. `confirmed` confirms the effect; `unknown` retains both possibilities; `not_applied` confirms no effect; `not_started` means no attempt. A network error must remain **unknown**, not assumed effect-free.
- `compensations` supplies declared operations, preconditions and costs. No inverse is invented.
- `observations` reveals facts and branches the plan. Action preconditions must hold in every world within that branch.
- `goal` declares the desired state. Supplied observations can narrow uncertainty; contradictions are rejected.

AND/OR search minimizes **worst-path cost within the supplied depth**, without assuming world probabilities. An independent interpreter walks each initial world, checks action preconditions and goals, and recomputes costs. Exported evidence includes source case, SHA-256, tree and all paths.

`minimum_cost_within_depth_proven` is true only after bounded exploration completes. Depth/time limits do not prove general impossibility. If a goal requires changing a fact no compensation touches, a witness explains impossibility **within the declared model**.

## Read-only MCP tool

```sh
python3 -m compensation_map mcp
```

Configure the client with its installed Python’s absolute path:

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

`compensation_plan` accepts `{ "case": ... }` and returns structured output. It is annotated read-only, non-destructive and closed-world. Initialization, discovery and calls are tested using **official MCP SDK 1.32.1**, negotiating protocol 2025-11-25. Actual OpenClaw/Hermes installation remains untested; no adapter automatically maps their errors into this model.

## Existing tools and limits

[Temporal already documents sagas and compensation](https://temporal.io/blog/compensating-actions-part-of-a-complete-breakfast-with-sagas); [contingent planning](https://unified-planning.readthedocs.io/en/latest/plan_representation.html) also exists. No invention of those methods is claimed. This demo exposes **ambiguous effect → beliefs → required observation → contingent compensation → independent replay**. It complements [Agent Commerce Ledger](https://github.com/gbesse/agent-commerce-ledger) and [Jev Proxy](https://github.com/gbesse/jev-proxy).

At most twelve facts, twelve trace steps, sixty-four worlds and nine search levels. Future actions/readbacks are assumed deterministic and reliable within the model. External concurrency, human authorization and compensation failures remain unresolved. Costs are declared, not measured real latency or money. Synthetic example; no real payment, message or inventory mutation. Neither production restoration nor SOTA superiority is demonstrated.

## Verify

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run test:mcp
npm run format:check
```

Thirteen tests cover beliefs, branches, cost, irreversibility, depth, contradictory observations and stdio MCP. Additional official SDK test; FR/EN/ES browser flows and mobile; CI Python 3.11/3.12 and wheel installation outside sources. Exit 1 means review is required, 2 means invalid input. MIT license; research alpha.
