# mdcheckx

`mdcheckx` counts markdown task checkboxes and reports progress.

## Install

```bash
pip install mdcheckx
```

## Usage

```bash
mdcheckx TODO.md
mdcheckx notes.md --json
mdcheckx - < notes.md
```

## Output

- `done` = checked boxes
- `todo` = unchecked boxes
- `percent` = done / total

## Development

```bash
python -m pip install -e . pytest
pytest
```
