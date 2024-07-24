# llamda-cli

A set of command line tools for working with LLMs.

## Installation

To install the CLI, run:

```bash
pip install llamda-cli
```

## Usage

```bash
lld [OPTIONS] COMMAND [ARGS]...
```

### `lld docs`

Useful in case you use [Anthropic's Claude](https://console.anthropic.com/).

Collects all markdown files from a directory (recursively) and writes them to an xml file.

```bash
 Usage: lld docs [OPTIONS] PATH                                                                
                                                                                               
 Collect docs from a path and write them to an xml file ready for Anthropic's Claude.          
                                                                                               
╭─ Options ───────────────────────────────────────────────────────────────────────────────────╮
│ --outfile  -o  PATH  The output file path. Defaults to: /{current_dir}/{source_dirname}.xml │
│ --verbose  -v        Verbose output.                                                        │
│ --yes      -y        Automatically confirm all prompts.                                     │
│ --help               Show this message and exit.                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```

Output file format:

```xml
<collection>
<title>Title</title>
<document><path>path/to/file</path>
<content>
# Document Title

Document content
</content>
</document>
...
</collection>
```
