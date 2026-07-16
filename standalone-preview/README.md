<!-- Authored with Claude (Anthropic). This whole file is Claude-generated. -->

# Standalone single-file STACK previews

The demo in the repository root serves many questions from a running container and fetches each question's XML at runtime. This folder is a complementary approach: turn **one** STACK question into **one self-contained HTML file** that anyone can double-click — no server, no build step, no sibling files.

It's handy for sharing a single question with a colleague, attaching a "try it" link to a question you're drafting, or embedding a live example in notes.

## How it works

`build_preview.py` stamps a question into `preview_template.html`:

- The whole Moodle question XML is **base64-embedded** in the output. Browsers block
  `fetch()` of local files on `file://`, so the preview must not depend on loading the
  `.xml` at runtime — embedding sidesteps that and makes the file portable.
- On open, the page calls a **CORS-enabled STACK API** to `render`, `validate` (as you
  type) and `grade` (on submit), exactly like the repo's `js/stackapicalls.js`. The client
  logic here is adapted from that file and the upstream `stackjsvle.js`.
- Buttons: **Submit answers**, **New variant** (cycles deployed seeds), **Show correct
  answer**, **Fill in correct answers** (populates the model answer), and **Open a
  different question XML…** (reads any local STACK XML with the file picker, so one file
  doubles as a general player).

## Usage

```bash
python3 build_preview.py path/to/question.xml
# -> path/to/question-preview.html
```

Options:

- `-o OUT.html` — output path.
- `--api URL` — STACK API base URL (default `https://stack-api.maths.ed.ac.uk`, the
  University of Edinburgh public demo, which allows cross-origin browser calls).
- `--title T` — header title (defaults to the question's `<name>`).

## Reproduce the bundled example

```bash
cd standalone-preview
python3 build_preview.py "../questions/Partial fraction decomposition.xml" \
  -o "examples/Partial fraction decomposition-preview.html"
```

Then open `examples/Partial fraction decomposition-preview.html` in a browser.

## The one requirement: CORS

A `file://` page has an opaque origin, so the STACK API must send `Access-Control-Allow-Origin` for the calls to succeed. If the page shows a red CORS/network error and nothing renders:

- use a CORS-enabled endpoint (the default Edinburgh demo is one), **or**
- serve the file over http instead of `file://`
  (`python3 -m http.server`, then open `http://localhost:8000/...`), **or**
- enable CORS on your own STACK API and pass `--api https://your-instance`.

Randomised questions must contain `<deployedseed>` entries, or the API reports "no deployed variants"; the script warns when a question has none.

## Files

| File | What it is |
| --- | --- |
| `preview_template.html` | The template. Placeholders `{{API_URL}}`, `{{TITLE}}`, `{{QUESTION_B64}}`. Contains MathJax 3 (CDN), a verbatim `stackjsvle.js` with a `CustomEvents` no-op shim, and the render/validate/grade client. |
| `build_preview.py` | Stamps a question XML into the template. |
| `examples/` | A generated sample built from `../questions/Partial fraction decomposition.xml`. |

## Attribution & licence

Ben Lloyd-Hurwitz prompted Claude (Opus 4.8). The embedded client is adapted from Sam Fearn's `stackapicalls.js` and the upstream `stackjsvle.js` from [`maths/moodle-qtype_stack`](https://github.com/maths/moodle-qtype_stack), which are GPLv3; this folder is distributed under the same terms as the rest of the repository.
