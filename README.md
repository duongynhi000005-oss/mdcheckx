# mdcheckx

`mdcheckx` counts markdown task checkboxes and reports progress across files or whole directories.

## Install

```bash
pip install mdcheckx
```

## Usage

```bash
mdcheckx TODO.md
mdcheckx notes.md --json
mdcheckx docs/ --per-file
mdcheckx plan.md notes.md --json
mdcheckx - < notes.md
mdcheckx docs/ --fail-under 80
```

## Output

- `done` = checked boxes
- `todo` = unchecked boxes
- `percent` = done / total
- `files` = per-file stats in JSON mode
- `--fail-under` = CI gate; exits 2 below threshold

## Development

```bash
python -m pip install -e . pytest
pytest
```
