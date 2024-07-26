# llamda-cli

![llamda-cli](https://img.shields.io/pypi/v/llamda-cli?label=llamda-cli)(https://pypi.org/project/llamda-cli/)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/llamda-ai/llamda-cli/release.yml?label=release)
![GitHub](https://img.shields.io/github/license/llamda-ai/llamda-cli)

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

### Common options

```bash
╭─ Options ───────────────────────────────────────────────────────╮
│ --verbose    -v        Verbose output.                          │
│ --yes        -y        Automatically confirm all prompts.       │
│ --help                 Show this message and exit.              │
╰─────────────────────────────────────────────────────────────────╯
```

### Files

Tools to collect files from a directory, recursively, and write them to a single xml file; useful for Anthropic's Claude.

```bash
╭─ Options ───────────────────────────────────────────────────────╮
│ --outfile  -o  PATH  The output file path. Defaults to:         │
│                      /{current_dir}/{source_dirname}.xml        │
╰─────────────────────────────────────────────────────────────────╯
```

<details>
<summary>Example output for a markdown file):</summary>

```xml
<collection>
<title>Title</title>
<document><path>path/to/file</path>
<content>
# Document Title

Document content


#### `lld files`

Generic file collector, allows you to specify one or more file types to collect.

```bash
 Usage: lld files [OPTIONS] PATH
 ...
</content>
</document>
...
</collection>
```

</details>
(see [template](https://github.com/llamda-ai/llamda-cli/blob/main/llamda_cli/lld/files/template.jinja2) for more details)

#### `lld files`

Collects all files from a directory and writes them to an xml file ready for Anthropic's Claude.

```bash
 Usage: lld files [OPTIONS] PATH
                            
╭─ Options ───────────────────────────────────────────────────────
│ *common options*                                                │
│ --extension  -e  TEXT  The extension(s) of the files to search  │
╰─────────────────────────────────────────────────────────────────╯
```

<details>
  <summary>See full options</summary>
  ```bash
  ╭─ Options ───────────────────────────────────────────────────────╮
  │ --verbose    -v        Verbose output.                          │
  │ --yes        -y        Automatically confirm all prompts.       │
  │ --extension  -e  TEXT  The extension(s) of the files to search  │
  │                        for.                                     │
  │ --outfile    -o  PATH  The output file path. Defaults to:       │
  │                        /{current_dir}/{source_dirname}.xml      │
  │ --help                 Show this message and exit.              │
  ╰─────────────────────────────────────────────────────────────────╯
  ```
</details>

<details>
  <summary>Deprecated</summary>
  
#### `lld docs` (deprecated)

Equivalent to [`lld files --extension md`](#lld-files).

    ```bash
    Usage: lld docs [OPTIONS] PATH                                                                
                                                                                                  
    Collect docs from a path and write them to an xml file ready for Anthropic\'s Claude.          
                                                                                                  
    ╭─ Options ───────────────────────────────────────────────────────────────────────────────────╮
    │ --outfile  -o  PATH  The output file path. Defaults to: /{current_dir}/{source_dirname}.xml │
    │ --verbose  -v        Verbose output.                                                        │
    │ --yes      -y        Automatically confirm all prompts.                                     │
    │ --help               Show this message and exit.                                            │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────╯
    ```

</details>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.