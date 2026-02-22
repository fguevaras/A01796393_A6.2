# Programming Assignment 6.2

## Overview
This project implements a hotel reservation system in Python using three
classes: `Hotel`, `Customer`, and `Reservation`. Each class supports
create, read, update, and delete operations, with data persisted to JSON
files. The project follows clean-code principles and is fully covered by
unit tests.

## Project Structure
- **Source Code:**
  - `source/hotel.py` — Hotel class (create, delete, display, modify, reserve room, cancel reservation)
  - `source/customer.py` — Customer class (create, delete, display, modify)
  - `source/reservation.py` — Reservation class (create, cancel)
- **Unit Tests:**
  - `tests/test_hotel.py` — 22 test cases for the Hotel class
  - `tests/test_customer.py` — 15 test cases for the Customer class
  - `tests/test_reservation.py` — 12 test cases for the Reservation class
- **Linter Config:** `.pylintrc` — project-wide pylint settings

## Requirements
- Python 3.x
- `unittest` (built-in, for writing unit tests)
- `pytest` (for running unit tests)
- `pylint` (for static code analysis)
- `flake8` (for style checking)
- `autopep8` (for automatic PEP 8 formatting)

## Execution

### Running Tests
Unit tests are written with `unittest.TestCase`. Each test uses a
temporary JSON file so tests are fully isolated. Run all tests from the
project root:
```bash
python -m unittest discover -s tests -v
```

To run a single test file:
```bash
python -m unittest tests.test_hotel -v
python -m unittest tests.test_customer -v
python -m unittest tests.test_reservation -v
```

### Running Linters and Style Checks

**Pylint**
```bash
pylint source/ tests/
```

**Flake8**
```bash
flake8 source/ tests/
```

**autopep8** (auto-fix PEP 8 issues in-place)
```bash
autopep8 --in-place --aggressive source/hotel.py source/customer.py source/reservation.py
```

## Linter Decisions

### `.pylintrc` configuration
A `.pylintrc` file was added to address pylint warnings that were either
false positives or intentional design choices:

| Setting | Reason |
|---------|--------|
| `source-roots=source` | Tells pylint where to find the source modules so that imports in test files resolve correctly and `E0401` (import-error) is eliminated. |
| `disable=R0801` | `R0801` (duplicate-code) flagged structural similarities across the three classes (Hotel, Customer, Reservation). These similarities are intentional and a natural result of the uniform CRUD interface; suppressing the check avoids noise without hiding real issues. |
| `max-public-methods=25` | The `Hotel` class exposes more than the default limit of 20 public methods due to its richer API (reserve room, cancel reservation, etc.). Raising the limit to 25 reflects the domain requirement rather than poor design. |

### `# pylint: disable=wrong-import-position` (block-level)
The test files insert the `source/` directory into `sys.path` before
importing the source modules. This pattern is required for the imports to
work but triggers both flake8 `E402` (module-level import not at top)
and pylint `C0413` (wrong-import-position).

- **flake8 E402** is suppressed with `# noqa: E402` on the import line.
- **pylint C0413** is suppressed with a block-level `disable/enable` pair
  wrapping only the affected import line:

  ```python
  # pylint: disable=wrong-import-position
  from customer import Customer  # noqa: E402
  # pylint: enable=wrong-import-position
  ```

  An inline comment was not used because the combined `# noqa: E402  # pylint: disable=...`
  comment made the line exceed the 79-character PEP 8 limit for the
  longer module names (`customer`, `reservation`), triggering `E501`.
  The block approach keeps each import line short and both tools clean.

## Author
- **Name:** Fabiola Guevara Soriano
- **ID:** A01796393
