# draftjs_exporter_wagtaildbhtml 🐍

> Convert the Facebook Draft.js editor’s raw ContentState to Wagtail's DB-HTML.

## Output format

Wagtail's DB-HTML content representation is an HTML-like XML syntax, with a few custom elements and attributes.

Here are examples of representations specific to this format:

```html
<!-- Bold -->
<b>bold</b>
<!-- Italic -->
<i>Italic</i>
<!-- Image -->
<embed alt="Right-aligned image" embedtype="image" format="right" id="49"/>
<!-- Embed -->
<embed embedtype="media" url="https://www.youtube.com/watch?v=y8Kyi0WNg40"/>
<!-- Document link -->
<a id="1" linktype="document">document link</a>
<!-- Internal page link -->
<a id="42" linktype="page">internal page link</a>
```

### Differences in format compared to Wagtail 1 processing

There are a number of differences between the DB-HTML coming from Wagtail 1's rich text processing pipeline, and the DB-HTML produced from Draft.js ContentState by `draftjs_exporter`.

The reasons for those differences are:

- Wagtail 1's DB-HTML comes from Hallo, which doesn't provide much control over its HTML output.
- Working on arbitrary HTML from the editor, Wagtail's DB-HTML pipeline doesn't normalise ambiguous representations.
- In contrast, `draftjs_exporter` operates on a more constrained format with less potential for ambiguities.
- `drafjs_exporter` also further constraints its output to normalise potentially ambiguous representations.

### Spacing unicode character

Hallo inserts `\u00a0` after a comma in some cases (no-break space).

```html
<b>bold</b>,\u00a0<i>italic</i>
```

### Order of tags for multiple styles

- Hallo wraps style tags in the order they are used in the editor
- `draftjs_exporter` always wraps style tags in the same order (alphabetical) ([`style_state.py#L30`](https://github.com/springload/draftjs_exporter/blob/dcfa0491ce78783a20720ed5b557166154a57259/draftjs_exporter/style_state.py#L30))

```html
<!-- Hallo, when activating italic, then bold -->
<i><b>italic bold</b></i>
<!-- Draftail, regardless of activation order -->
<b><i>italic bold</i></b>
```

### Wrapping in `p` tags

- Hallo frequently wraps content within `p` tags.
- `draftjs_exporter` only outputs `p` tags for individual blocks of type `UNSTYLED` (the editor's default format).

```html
<!-- Hallo -->
<p>
    <ul><li>Unordered list item 1</li><li>Unordered list item 2</li><li>Unordered list item 3</li></ul>
    <p>Horizontal rule:</p>
</p>
<!-- Draft.js -->
<ul><li>Unordered list item 1</li><li>Unordered list item 2</li><li>Unordered list item 3</li></ul>
<p>Horizontal rule:</p>
```

### `br` insertions

To confirm – behaviour may be different

```html
<!-- Hallo -->
<ol><li>Ordered list item 1<br/></li></ol>
<!-- Draft.js -->
<ol><li>Ordered list item 1</li></ol>
```

### To test further

Overlapping style ranges

## Installation

> Requirements: `virtualenv`, `pyenv`, `twine`

```sh
git clone git@github.com:thibaudcolas/draftjs_exporter_wagtaildbhtml.git
cd draftjs_exporter_wagtaildbhtml/
# Install the git hooks.
./.githooks/deploy
# Install the Python environment.
virtualenv .venv
source ./.venv/bin/activate
make init
# Install required Python versions
pyenv install --skip-existing 2.7.11
pyenv install --skip-existing 3.4.4
pyenv install --skip-existing 3.5.1
# Make required Python versions available globally.
pyenv global system 2.7.11 3.4.4 3.5.1
```

## Commands

```sh
make help            # See what commands are available.
make init            # Install dependencies and initialise for development.
make lint            # Lint the project.
make test            # Test the project.
make test-watch      # Restarts the tests whenever a file changes.
make test-coverage   # Run the tests while generating test coverage data.
make test-ci         # Continuous integration test suite.
make dev             # Restarts the example whenever a file changes.
make clean-pyc       # Remove Python file artifacts.
make publish         # Publishes a new version to pypi.
```

## Debugging

- Always run the tests. `npm install -g nodemon`, then `make test-watch`.
- Use a debugger. `pip install ipdb`, then `import ipdb; ipdb.set_trace()`.
