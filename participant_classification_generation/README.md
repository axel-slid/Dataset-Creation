# Participant Classification Generation

Generates images for participant-vs-non-participant datasets.

## Inputs

Place source workplace images in:

```text
participant_classification_generation/base_images/
```

Supported image extensions are `.png`, `.jpg`, `.jpeg`, and `.webp`.

## Generate Edited Images

```bash
python datasetGenScript.py --prompt most_non --max-images 50
```

Options:

- `--prompt`: one of `no_non`, `some_non`, or `most_non`.
- `--input-folder`: source image folder. Defaults to `base_images`.
- `--output-folder`: generated image folder. Defaults to `generated_images`.
- `--output-prefix`: output filename prefix. Defaults to the selected prompt.
- `--model`: Gemini image model. Defaults to `gemini-2.5-flash-image`.

Requires `GEMINI_API_KEY`.

## Generate Automatic Boxes

Start Roboflow inference locally:

```bash
inference server start
```

Then run:

```bash
python roboflow_autoBounding.py --image-folder generated_images --output-json auto_boxes.json
```

Requires `ROBOFLOW_API_KEY`.

## Preview Boxes

```bash
python visualizeBoxes.py --image-folder generated_images --json-file auto_boxes.json --output-folder preview_boxes
```
