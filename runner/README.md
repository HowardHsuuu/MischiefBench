# MischiefBench Runner

Read scenario files, prompt model, write JSONL logs.

## Usage

```bash
python -m runner.run_bench \
    model \
    scenario \
    output \
    framing \
    [--dry-run] \
    [--skip]
```

| Option | Description |
| ------ | ----------- |
| model | Short name of model |
| scenario | Path to json file describing scenario |
| output | Path to jsonl file to save output to |
| framing | Select framing from scenario |
| --dry-run | Do not query model, use random responses |
| --skip | Skip if output file exists |


Supported model:
| Shortname | Full name |
| --------- | --------- |
| llama | meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo |
| mistral | mistralai/Mistral-7B-Instruct-v0.3 |
| qwen | Qwen/Qwen2.5-7B-Instruct-Turbo |

Be default we query the `together.ai` API. A different endpoint can be specified in `runner/config.json`. The API key is stored in `api_key.txt`. If this file is not present, the user is prompted to enter a key.
