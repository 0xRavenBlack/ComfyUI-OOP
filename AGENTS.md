# AGENTS.md — ComfyUI-OOP

Guidance for AI agents (and humans) working in this repository.
Read this file **before** changing anything. Every claim below is derived from the code in this repo.

---

## 1. What this repo is

A **ComfyUI custom-node package**. It implements "Object-Oriented Prompting": a set of nodes
that build a structured, `key:value` text prompt (e.g. `Hair: color:BlackBeige, style:Short`)
from many small typed "attribute" nodes, then assembles it into a CLIP-encoded conditioning
tensor.

- **The entire repository *is* the package.** The repo root is what gets cloned into
  `ComfyUI/custom_nodes/ComfyUI-OOP`. There is no `src/`, no build step, no CLI, no app.
- Language: Python 3, V3 node classes carry a few `io` type annotations (the V3 schema API
  returns typed objects). Runtime dependency: ComfyUI itself — each module imports **only
  `comfy_api.latest` (the interface layer)** at module level, so the modules stay importable
  standalone as long as the ComfyUI root is on `sys.path` (see §8).
- License: MIT (`LICENSE`, "Copyright (c) 2025 Mike Ravenblack") — do not alter.
- Published to the Comfy Registry via `pyproject.toml` `[tool.comfy]` (`PublisherId = "ravenblack"`).

---

## 2. Repository layout

| Path | Role | Editable? |
|---|---|---|
| `__init__.py` | **Package loader.** Imports the 12 node classes explicitly, then exposes `async comfy_entrypoint() -> ComfyExtension` (V3 registration; `NODE_CLASS_MAPPINGS` deliberately absent — if present the V1 path would shadow V3). | Yes — and **must** be edited whenever a node module is added |
| `oop_node.py` | Terminal/aggregation node: consumes `CLIP` + the 6 top-level OOP types → `CONDITIONING`, `STRING` | Yes |
| `oop_person_node.py` | Aggregator: consumes the 5 body-part OOP types → `OOP_PERSON` | Yes |
| `oop_{hair,eyes,mouth,clothing,pose,style,view,location,animal,environment}_node.py` | Leaf "attribute" nodes | Yes |
| `oop_shared.py` | **Not a node.** The single shared module owning the prompt contract: `NO_VALUE` sentinel, `PROMPT_BULLET`, `random_value(pool)`, `format_pairs(pairs)`, and the eleven `io.Custom("OOP_*")` connection types. Every node module reaches it with `from .oop_shared import …` | Yes — deliberately **not imported as a node** |
| `pyproject.toml` | Comfy Registry metadata (project `name = "oop"`, `version = "1.2.0"`) | Yes — bump `version` when publishing a release |
| `README.md` | User-facing docs + the canonical example prompt | Yes |
| `workflow/ComfyUIOOP.json` | Saved ComfyUI graph (19-node demo workflow) | Only when intentionally re-exporting |
| `screenshot/{workflow,prompt}.png` | README assets | No |
| `.github/workflows/publish.yml` | Registry publish action | No |
| `.gitignore` | Generic Python/Django template ignore list | No |

**Package-root rule — 13 `.py` files, exactly.** The root holds the 12 node modules
plus the one shared module `oop_shared.py`. ComfyUI loads the package by compiling its
`__init__.py` (`nodes.py:load_custom_node`, `spec_from_file_location(name, "<folder>/__init__.py")`),
so the only code that runs at startup is `__init__.py` plus whatever its imports pull in; a new root
module is invisible until `__init__.py` imports it **and** `OOPExtension.get_node_list` lists its class,
and once listed it is registered by `io.Schema.node_id` with no per-module isolation. Therefore:
- a fourth tier, a spike/scratch file, or a `*_old.py` backup at the root is unregistered dead weight
  that still ships in the package download and still gets picked up by `python3 -m py_compile *.py`
  and the §8 root check — it can be neither trusted nor safely removed by reading `__init__.py` alone
  (that is also how loose `.py` files at the `custom_nodes/` level get imported straight into the
  node table by the same loader).
- shared code goes **into `oop_shared.py`**, not into a second helper module.
- throwaway experiments go outside the package, in `/tmp`.
- `__pycache__/` and `.disabled` are the only non-module entries allowed to sit in the folder
  (`__pycache__` is stripped by the loader; `.disabled` suffixes are skipped).

There are **no** `requirements.txt`, `tests/`, `examples/`, `WEB_DIRECTORY` assets,
lint/format/typing config (`pyproject.toml` has no `[tool.ruff]`, `[tool.black]`, `[tool.mypy]`,
or any `dependencies` / `requires-python` fields), and no issue templates.
Do not introduce tooling that is not already here unless the task explicitly asks for it.

---

## 3. The node registry contract

ComfyUI discovers nodes through the `__init__.py` it compiles (`nodes.py:load_custom_node`).
The loader checks for the legacy V1 `NODE_CLASS_MAPPINGS` first and only falls back to the V3
path when those dicts are absent. Three rules are absolute:

1. This package registers **V3 only**: `__init__.py` deliberately defines **no**
   `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS` — as long as either dict exists at the
   package root, the V1 path wins and shadows the entrypoint. Registration is the callable
   `async comfy_entrypoint()` returning a `ComfyExtension`, whose `get_node_list()` yields the
   12 `io.ComfyNode` classes.
2. **The imports + `OOPExtension.get_node_list` in `__init__.py` are the single source of
   registration truth.** A `*_node.py` whose class is not imported and listed is never registered
   and never appears in ComfyUI. This is the #1 cause of "my new node doesn't show up" — check
   `__init__.py` before debugging anything else.
3. The registry key is `io.Schema.node_id` (the exact class name, e.g. `"OOPHairNode"`) and the
   display name is `io.Schema.display_name`. `node_id`s must stay globally unique across all 12
   modules; `Schema.validate()` also requires **unique output ids per node**, which is why every
   leaf output now carries an explicit id (`OOP_HAIR.Output("hair", …)`).

Relative import (`".oop_node"`, `__name__`) means the package must be importable as a package.
ComfyUI puts `custom_nodes/` on `sys.path` and imports the folder name; the hyphen in
`ComfyUI-OOP` is fine because `importlib.import_module` accepts non-identifier names.

---

## 4. The type system and the DAG

Every leaf node emits a plain Python `str` under a bespoke connection type:

`OOP_STYLE` · `OOP_VIEW` · `OOP_PERSON` · `OOP_ANIMAL` · `OOP_LOCATION` · `OOP_ENVIRONMENT`
· `OOP_HAIR` · `OOP_EYES` · `OOP_MOUTH` · `OOP_CLOTHING` · `OOP_POSE`

These are now single shared V3 connection types: `oop_shared.py` defines each once as
`io.Custom("OOP_…")` and every module imports them — a node module must never re-declare a
bespoke type string or use a bare `"OOP_X"` literal.

Data flow is a strict two-level DAG:

```
hair, eyes, mouth, clothing, pose  ──▶ OOPPersonNode ─┐
style, view ───────────────────────────────────────── │
animal, location, environment ────────────────────────┼─▶ OOPNode (CLIP + 6 sections) ─▶ CONDITIONING, STRING
                                                      ┘                                        │
                                                                        KSampler.positive / ShowText|pysssss
```

- `OOPPersonNode` re-emits child output verbatim, prefixed with `*  ` bullet lines.
- `OOPNode` prefixes each section with its label (`Style:`, `Perspective:`, `Person:`,
  `Animal:`, `Location:`, `Environment:`) and joins sections with `\n`.
- Any new node must plug into this DAG. A third tier changes the prompt format that
  `README.md` documents and that the sample images were generated against.

`workflow/ComfyUIOOP.json` is the reference graph. It also uses nodes from **other** extensions
(`SDXL Quick Empty Latent (WLSH)`, `ShowText|pysssss`) plus core nodes
(`CheckpointLoaderSimple`, `KSampler`, `VAEDecode`, `PreviewImage`, `ConditioningZeroOut`,
`CLIPTextEncode` for the negative prompt). Do not assume those types exist in this package.

---

## 5. File template — follow it exactly

```python
import random                       # only if the node randomizes
from comfy_api.latest import io     # V3 interface layer — required in every node module
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_THING


class OOPThingNode(io.ComfyNode):   # OOP + PascalCase noun + "Node" suffix
    THING_OPTIONS = [               # SCREAMING_SNAKE case for value pools
        " ", "RealValue", ...       # " " is the "no value" sentinel — keep it at index 0
    ]

    @classmethod
    def define_schema(cls):         # MUST reference cls.<POOL> so dropdowns resolve
        return io.Schema(
            node_id="OOPThingNode",                 # == class name == registry key
            display_name="OOP Thing 🧵",            # "OOP <Name> <emoji>"
            category="Object-Oriented Prompting",   # identical in ALL 12 files — never vary it
            description="…",
            inputs=[
                io.Combo.Input("thing", options=cls.THING_OPTIONS, default="RealValue"),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_THING.Output("thing")],    # explicit unique output id per node
        )

    @classmethod
    def execute(cls, thing, randomize=False) -> io.NodeOutput:
        if randomize:
            thing = random_value(cls.THING_OPTIONS)  # skips the " " sentinel at index 0
        return io.NodeOutput(format_pairs([("thing", thing)]))  # NodeOutput, not a tuple

    @classmethod
    def fingerprint_inputs(cls, **kwargs):          # replaces V1 IS_CHANGED
        if kwargs.get("randomize"):
            return random.getrandbits(32)           # forces re-evaluation on every run
```

---

## 6. Prompt-string conventions (this is a format contract — preserve byte-for-byte)

- `key:value` pairs, joined with `, `, **fixed field order per node**.
- **`" "` (one single space) is the "no value" sentinel** inside dropdown lists. It is always
  the first element of a palette list. Emitters test `if value != " "`; randomizers use
  `LIST[1:]` to skip it. **Never reorder, prepend, or delete entries without keeping the
  sentinel at index 0** — both the `[1:]` slices and the `!= " "` comparisons depend on that index.
- Person's optional OOP link inputs arrive as `None` when unconnected (the V1 `""` default no
  longer exists); the person join filters with `if value and value.strip()`. Never reintroduce an
  unguarded `.strip()` on optional values.
- Person bullet lines are `"\n*  "` — **two** spaces after the `*`.
- Person bullet lines are `"\n*  "` — **two** spaces after the `*`.
- Hair joins `main_color` + `" "` + `optional_color.strip()` and strips the result
  (`color:Black Beige`, or `color:Black` when the second colour is blank).
- The old V1 inconsistencies (stray space in animal `color:`, duplicate dropdown labels, mismatched
  age ranges) were already normalized: `OOPPersonNode.AGE_BUCKETS` is the single source of truth for
  the slider range, the age label and the randomizer, and every emitter goes through `format_pairs`.
  Do not reintroduce hand-built pair strings.

---

## 7. Known quirks, hard-coded values, and do-not-touch areas

`OOPNode` (in `oop_node.py`):

- `clip_skip` is now a **user input** (`io.Int`, default `0`, range −24..0). `0` means "keep the
  layer the checkpoint loaded" and calls `encode_from_tokens_scheduled(tokens)` directly, which is
  correct for SDXL, SD1.5, Flux/Flux2/Flux3, Krea2, Ernie and friends. A negative value calls
  `Clip.clip_layer(clip_skip)` around **one** encode and restores the wrapper's previous
  `layer_idx` afterwards, because the shared `CLIP` wrapper would otherwise leak the skip into
  every later encode in the graph.
- No conditioning metadata is injected any more; `encode_from_tokens_scheduled` owns it, so
  non-SDXL size assumptions are gone.
- The `l`/`g` token padding runs **only when both keys exist and lengths differ** (dual encoders
  like SDXL's); single-encoder tokenizers pass through untouched.
- No `gc.collect()`, no double tokenize, no hard-coded SDXL sizes — the Phase-1 model-agnostic
  rewrite removed them; do not resurrect that workaround code.
- `io.Clip.Input("Clip")` is the required socket; the input id keeps its capital `P` from the V1
  graph so saved workflows still connect.
- README documents all 12 nodes as of the V3 migration; docs gaps are no longer expected.

Caching asymmetry (`fingerprint_inputs`, the V3 replacement for `IS_CHANGED`):

- Present and randomize-aware (return `random.getrandbits(32)` when `randomize`): hair, clothing,
  mouth, eyes, pose, location, animal, environment — and now **also `OOPPersonNode`**, which
  randomizes its own `age`; V1 had no `IS_CHANGED` there and left the roll cached, so adding the
  fingerprint fixed that stale-cache quirk.
- `OOPViewNode` fingerprints a `sha256` of `angle|viewType|backgroundBlur` always (stable across
  server restarts, unlike built-in `hash()`).
- **Absent** in: `OOPNode` and `OOPStyleNode` — both are pure functions of their inputs, so the
  default value-cache behaviour is correct for them. Never delete an existing fingerprint.
- `fingerprint_inputs(cls, **kwargs)` is how the randomizers read the flag; nodes with a fixed
  fingerprint list their inputs positionally instead.

No node class defines `__init__` any more: the V3 call path (`define_schema`/`execute`/`fingerprint_inputs`
as class methods) never carries instance state, and the V1 `self.name` vestigial state was dropped
with the migration. Do not add `__init__` or store `self.*` in node classes.

`pyproject.toml` notes: project `name = "oop"` (not `ComfyUI-OOP`), no `requires-python`,
no `dependencies`. The publish workflow triggers **only** on a push whose diff touches
`pyproject.toml` — so version bumps must go through `pyproject.toml` to reach the Registry.

---

## 8. Commands

### Build / sanity check (no build system — these are the real checks)

```bash
# Syntax-check every module (bare python is enough)
python3 -m py_compile *.py

# Import the package exactly the way ComfyUI does, and list what got registered —
# V3 needs comfy_api/torch, so use the ComfyUI venv and put the ComfyUI root on sys.path
/home/ravenblack/ComfyUI/.venv/bin/python3 - <<'PY'
import importlib, os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.getcwd()))        # simulate ComfyUI/custom_nodes
sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())))  # ComfyUI root (comfy_api)
package = importlib.import_module(os.path.basename(os.getcwd()))
assert not hasattr(package, "NODE_CLASS_MAPPINGS")      # the V1 path would shadow V3
nodes = asyncio.run(asyncio.run(package.comfy_entrypoint()).get_node_list())
print(sorted(n.GET_SCHEMA().node_id for n in nodes))    # must contain all 12 ids
PY
```

Expected registered node_ids (12):
`OOPNode, OOPPersonNode, OOPHairNode, OOPClothingNode, OOPMouthNode, OOPEyesNode, OOPPoseNode,
OOPStyleNode, OOPViewNode, OOPLocationNode, OOPAnimalNode, OOPEnvironmentNode`

If an id is missing, the module is not imported by `__init__.py` or its class is missing from
`OOPExtension.get_node_list`.

```bash
# Package-root hygiene (§2): root modules must equal the 12 node modules + oop_shared + __init__
python3 - <<'PY'
import os
expected = {"oop_node", "oop_person_node", "oop_hair_node", "oop_clothing_node", "oop_mouth_node",
            "oop_eyes_node", "oop_pose_node", "oop_style_node", "oop_view_node", "oop_location_node",
            "oop_animal_node", "oop_environment_node", "oop_shared", "__init__"}
root = {os.path.splitext(f)[0] for f in os.listdir(".") if f.endswith(".py")}
print(sorted(root - expected))     # must be []
print(sorted(expected - root))     # must be []
PY
```

### Install / run (needs ComfyUI; not available in this sandbox)

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/0xRavenBlack/ComfyUI-OOP
# then restart ComfyUI; "Object-Oriented Prompting" category appears in the node menu
```

### Publish to Comfy Registry

Edit `pyproject.toml` → bump `version` → push to `main`/`master`. The
`.github/workflows/publish.yml` action then runs (owner-gated to `0xRavenBlack`, requires
`REGISTRY_ACCESS_TOKEN` repo secret). `workflow_dispatch` is the manual alternative.

### Git

- Trunk: `main` (single branch, `origin/HEAD -> origin/main`). History mixes lowercase imperative
  subjects (`add more Mouth options`, `fix installation instructions`) with scoped conventional
  commits (`chore(publish): …`). Match the neighbourhood you are editing; keep subjects short and imperative.

---

## 9. How to add a new node (recipe)

1. Create `oop_<something>_node.py` following the V3 template in §5.
2. Emit a new bespoke type: define `io.Custom("OOP_<SOMETHING>")` **in `oop_shared.py`** (the single
   type contract) and import it; pick a name that does not collide with §4's list.
3. Decide its DAG position: if a consumer needs it, add `io.<TYPE>.Input("<name>", optional=True)`
   to that consumer's `io.Schema.inputs` **and** the matching `="<default>"-friendly` parameter to
   its `execute` signature (unconnected arrives as `None`).
4. Import the class in `__init__.py` and list it in `OOPExtension.get_node_list`.
5. The `node_id` (== class name) and `display_name` live in the schema; keep `category` exactly
   `"Object-Oriented Prompting"`.
6. If it randomizes, add the randomize-aware `fingerprint_inputs` pattern (otherwise the RNG result
   is cached and the workflow produces identical output).
7. Run the §8 checks. Then update `README.md` with a node section matching the existing style
   (`### OOP X Node <emoji>` + one sentence) — README currently lists only 8 of the nodes, so
   add only what you changed.
8. Optionally regenerate `workflow/ComfyUIOOP.json` from ComfyUI if the demo workflow changes.

---

## 10. House rules for agents

- **Do not** reformat the whole repo, rename `CATEGORY`, retype connection types, or "modernize"
  the CLIP block in `oop_node.py` — those are load-bearing behaviors for saved workflows
  (see the `ver` hash inside `workflow/ComfyUIOOP.json`).
- **Do not** edit `screenshot/`, `LICENSE`, or `.github/` unless the task demands it.
- Preserve the `" "` sentinel invariant (§6) any time you touch a value list.
- Keep diffs minimal and scoped; one concern per commit/PR.
- Comments are sparse and only explain non-obvious workarounds — match that density, do not
  add docstrings/annotations to files that have none (it would diverge from the codebase).
- If a change would alter emitted prompt strings, say so explicitly and note the downstream
  format/README impact.
- Never claim a workflow "works" without running the §8 checks; ComfyUI itself is not installed
  in this environment, so runtime verification beyond import/registration is out of scope.
