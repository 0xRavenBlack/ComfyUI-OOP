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
- Language: Python 3, no type annotations. Runtime dependency: ComfyUI itself — but **nothing
  from ComfyUI is imported at module level**, so the modules can be imported standalone (see §7).
- License: MIT (`LICENSE`, "Copyright (c) 2025 Mike Ravenblack") — do not alter.
- Published to the Comfy Registry via `pyproject.toml` `[tool.comfy]` (`PublisherId = "ravenblack"`).

---

## 2. Repository layout

| Path | Role | Editable? |
|---|---|---|
| `__init__.py` | **Package loader.** Imports each node module from an explicit `node_list`, then merges `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS`. | Yes — and **must** be edited whenever a node module is added |
| `oop_node.py` | Terminal/aggregation node: consumes `CLIP` + the 6 top-level OOP types → `CONDITIONING`, `STRING` | Yes |
| `oop_person_node.py` | Aggregator: consumes the 5 body-part OOP types → `OOP_PERSON` | Yes |
| `oop_{hair,eyes,mouth,clothing,pose,style,view,location,animal,environment}_node.py` | Leaf "attribute" nodes | Yes |
| `oop_shared.py` | **Not a node.** The single shared module owning the prompt contract: `NO_VALUE` sentinel, `PROMPT_BULLET`, `random_value(pool)`, `format_pairs(pairs)`. Every node module reaches it with `from .oop_shared import …` | Yes — deliberately **not** in `node_list` |
| `pyproject.toml` | Comfy Registry metadata (project `name = "oop"`, `version = "1.1.0"`) | Yes — bump `version` when publishing a release |
| `README.md` | User-facing docs + the canonical example prompt | Yes |
| `workflow/ComfyUIOOP.json` | Saved ComfyUI graph (19-node demo workflow) | Only when intentionally re-exporting |
| `screenshot/{workflow,prompt}.png` | README assets | No |
| `.github/workflows/publish.yml` | Registry publish action | No |
| `.gitignore` | Generic Python/Django template ignore list | No |

**Package-root rule — 13 `.py` files, exactly.** The root holds the 12 `node_list` node modules
plus the one shared module `oop_shared.py`. ComfyUI loads the package by compiling its
`__init__.py` (`nodes.py:load_custom_node`, `spec_from_file_location(name, "<folder>/__init__.py")`),
so the only code that runs at startup is `__init__.py` plus whatever `node_list` pulls in; a new root
module is invisible until `node_list` lists it, and once listed it is registered by class-name key
with no per-module isolation. Therefore:
- a fourth tier, a spike/scratch file, or a `*_old.py` backup at the root is unregistered dead weight
  that still ships in the package download and still gets picked up by `python3 -m py_compile *.py`
  and the §8 root check — it can be neither trusted nor safely removed by reading `node_list` alone
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

ComfyUI discovers nodes through module-level dicts. Three rules are absolute:

1. `__init__.py` merges mappings from the modules named in `node_list`:
   ```python
   imported_module = importlib.import_module(f".{module_name}", __name__)
   NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
   ```
2. **`node_list` is the single source of registration truth.** A `*_node.py` file that is not
   listed there is never imported and never appears in ComfyUI. This is the #1 cause of
   "my new node doesn't show up" — check `node_list` before debugging anything else.
3. Mapping keys are the exact class names (`"OOPHairNode": OOPHairNode`). Because of the
   `{**existing, **new}` merge, **later entries in `node_list` silently override earlier ones**
   on key collision. Keys must stay globally unique across all 12 modules.

Relative import (`".oop_node"`, `__name__`) means the package must be importable as a package.
ComfyUI puts `custom_nodes/` on `sys.path` and imports the folder name; the hyphen in
`ComfyUI-OOP` is fine because `importlib.import_module` accepts non-identifier names.

---

## 4. The type system and the DAG

Every leaf node emits a plain Python `str` under a bespoke connection type:

`OOP_STYLE` · `OOP_VIEW` · `OOP_PERSON` · `OOP_ANIMAL` · `OOP_LOCATION` · `OOP_ENVIRONMENT`
· `OOP_HAIR` · `OOP_EYES` · `OOP_MOUTH` · `OOP_CLOTHING` · `OOP_POSE`

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

class OOPThingNode:                 # OOP + PascalCase noun + "Node" suffix
    THING_OPTIONS = [               # SCREAMING_SNAKE case for value pools
        " ", "RealValue", ...       # " " is the "no value" sentinel — keep it at index 0
    ]

    def __init__(self):             # optional; only sets self.name (unused state, kept for parity)
        self.name = "Thing"

    @classmethod
    def INPUT_TYPES(cls):           # MUST reference cls.<POOL> so dropdowns resolve
        return {
            "required": {"thing": (cls.THING_OPTIONS, {"default": "RealValue"})},
            "optional": {"randomize": ("BOOLEAN", {"default": False})},
        }

    RETURN_TYPES = ("OOP_THING",)   # 1-tuple, matching the type consumed downstream
    FUNCTION = "generate_thing"     # verb_name, equal to the method name below
    CATEGORY = "Object-Oriented Prompting"   # identical in ALL 12 files — never vary it

    def generate_thing(self, thing, randomize=False):
        if randomize:
            thing = random.choice(self.THING_OPTIONS[1:])
        return (f"thing:{thing}",)  # always returns a TUPLE

    @classmethod
    def IS_CHANGED(cls, thing, randomize):
        if randomize:
            return random.getrandbits(32)   # forces re-evaluation on every run

NODE_CLASS_MAPPINGS = {"OOPThingNode": OOPThingNode}
NODE_DISPLAY_NAME_MAPPINGS = {"OOPThingNode": "OOP Thing 🧵"}   # "OOP <Name> <emoji>"
```

---

## 6. Prompt-string conventions (this is a format contract — preserve byte-for-byte)

- `key:value` pairs, joined with `, `, **fixed field order per node**.
- **`" "` (one single space) is the "no value" sentinel** inside dropdown lists. It is always
  the first element of a palette list. Emitters test `if value != " "`; randomizers use
  `LIST[1:]` to skip it. **Never reorder, prepend, or delete entries without keeping the
  sentinel at index 0** — both the `[1:]` slices and the `!= " "` comparisons depend on that index.
- Person's optional OOP inputs use `""` (empty string) as their sentinel instead, tested with
  `.strip()`.
- Person bullet lines are `"\n*  "` — **two** spaces after the `*`.
- Hair concatenates `main_color` + `optional_color.strip()` with **no separator**
  (`color:OliveBeige`), matching the README example.
- Known inconsistencies in existing output — intentional-looking, so **do not "fix" them
  without an explicit instruction**:
  - `OOPAnimalNode` emits `color: {color}` (stray space after the colon), while every other node
    emits `color:{color}`.
  - `AGE_CATEGORIES` key `(16, 19)` maps to label `"18-19Years"`; the age randomizer draws
    `random.randint(16, 99)` while the widget's `min` is `18`, so ranges do not line up.
  - `ANIMAL_TYPES` contains `"Horse"` twice; `COLORS` in the animal node contains `"Turquoise"`
    twice (duplicate dropdown labels).

---

## 7. Known quirks, hard-coded values, and do-not-touch areas

`OOPNode.create_prompt` (in `oop_node.py`):

- `clip_skip = -2` is **hard-coded**, applied via `Clip.clip_layer(clip_skip)` and also injected
  into the conditioning metadata. It is not a user-facing input.
- Conditioning metadata hard-codes `original_size (1024, 1024)`, `crop_coords (0, 0)`,
  `target_size (1024, 1024)`. These are SDXL assumptions and are wrong for non-SDXL checkpoints.
- `gc.collect()` is called on every execution (`import gc`) — memory hygiene for GPU-resident CLIP.
- The prompt is tokenized **twice** (`tokens = Clip.tokenize(prompt)` and
  `tokens["l"] = Clip.tokenize(prompt)["l"]`), then padded so `l`/`g` token lists match length.
  This is deliberate workaround code; do not simplify it while "cleaning up".
- `INPUT_TYPES` declares `"Clip": ("CLIP",)` with **no** `forceInput` — that is how ComfyUI's
  text-encoder object is threaded through.
- README does not document `OOPNode`, `OOP Animal`, `OOP Clothing`, or `OOP Environment`
  sections. That is a docs gap, not a code bug.

Caching asymmetry (`IS_CHANGED`):

- Present and randomize-aware in: hair, clothing, mouth, eyes, pose, location, animal,
  environment (all `random.getrandbits(32)` when `randomize`) and view (returns
  `hash((angle, viewType, backgroundBlur))` always).
- **Absent** in: `OOPNode`, `OOPPersonNode`, `OOPStyleNode`. `OOPPersonNode` randomizes its own
  `age` but has no `IS_CHANGED`, so it only re-runs when a child's output changes. If you touch
  caching, this is the place to reason about — never delete an existing `IS_CHANGED`.
- An `IS_CHANGED` that falls through returns `None`, which is the intended "use default cache
  behaviour" signal.

Sentinel/`__init__` asymmetry: several classes define `__init__` setting only `self.name`
(plus `self.randomize` in `OOPEyesNode`), which is never read by the ComfyUI call path
(`INPUT_TYPES`/`FUNCTION` are invoked without instance state in practice). Keep it consistent
with the file you are editing; do not mass-delete it.

`pyproject.toml` notes: project `name = "oop"` (not `ComfyUI-OOP`), no `requires-python`,
no `dependencies`. The publish workflow triggers **only** on a push whose diff touches
`pyproject.toml` — so version bumps must go through `pyproject.toml` to reach the Registry.

---

## 8. Commands

### Build / sanity check (no build system — these are the real checks)

```bash
# Syntax-check every module
python3 -m py_compile *.py

# Import the package exactly the way ComfyUI does, and list what got registered
python3 - <<'PY'
import importlib, os, sys
sys.path.insert(0, os.path.dirname(os.getcwd()))        # simulate ComfyUI/custom_nodes
package = importlib.import_module(os.path.basename(os.getcwd()))
print(sorted(package.NODE_CLASS_MAPPINGS))              # must contain all 12 keys
print(package.NODE_DISPLAY_NAME_MAPPINGS)
PY
```

Expected registered keys (12):
`OOPNode, OOPPersonNode, OOPHairNode, OOPClothingNode, OOPMouthNode, OOPEyesNode, OOPPoseNode,
OOPStyleNode, OOPViewNode, OOPLocationNode, OOPAnimalNode, OOPEnvironmentNode`

If a key is missing, the module is missing from `node_list` in `__init__.py`.

```bash
# Package-root hygiene (§2): root modules must equal node_list + oop_shared + __init__
python3 - <<'PY'
import importlib, os, sys
sys.path.insert(0, os.path.dirname(os.getcwd()))        # simulate ComfyUI/custom_nodes
package = importlib.import_module(os.path.basename(os.getcwd()))
allowed = set(package.node_list) | {"oop_shared", "__init__"}
root = {os.path.splitext(f)[0] for f in os.listdir(".") if f.endswith(".py")}
print(sorted(root - allowed))     # must be []
print(sorted(allowed - root - {"__init__"}))  # must be []
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

1. Create `oop_<something>_node.py` following the template in §5.
2. Emit a new bespoke type `OOP_<SOMETHING>`; pick a name that does not collide with §4's list.
3. Decide its DAG position: does a consumer need it (add the `optional` input with
   `{"forceInput": True, "default": ""}` to that consumer's `INPUT_TYPES` **and** to its
   `FUNCTION` signature, with a `=""` default)?
4. Add the module name (no `.py`) to `node_list` in `__init__.py`.
5. Register the class key + display name; keep `CATEGORY` exactly `"Object-Oriented Prompting"`.
6. If it randomizes, add the randomize-aware `IS_CHANGED` pattern (otherwise the RNG result is
   cached and the workflow produces identical output).
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
