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
```

## Output

- `done` = checked boxes
- `todo` = unchecked boxes
- `percent` = done / total
- `files` = per-file stats in JSON mode

## Development

```bash
python -m pip install -e . pytest
pytest
```
