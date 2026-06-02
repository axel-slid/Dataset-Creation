# Dataset Creation

Utilities for generating synthetic workplace datasets with Gemini image generation and optional Roboflow-assisted bounding boxes.

The repository has two independent workflows:

- `room_readiness_generation/`: creates paired room-state images for whiteboards, chairs, blinds, and tables.
- `participant_classification_generation/`: edits base workplace images to add meeting participants and non-participants, then optionally generates and previews person/head bounding boxes.

Generated images, labels, previews, API keys, virtual environments, and local cache files are intentionally ignored by git. A fresh clone should contain code and documentation only.

## Setup

Use Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with the API keys you need:

- `GEMINI_API_KEY` for Gemini image generation.
- `ROBOFLOW_API_KEY` for Roboflow inference.

Most scripts also read exported environment variables, so this works too:

```bash
export GEMINI_API_KEY="..."
export ROBOFLOW_API_KEY="..."
```

## Room Readiness Workflow

Run from the repository root:

```bash
cd room_readiness_generation
python generate_base_images.py
python main.py
python change_format.py
```

Outputs:

- `room_readiness_generation/base_images/`: generated base rooms.
- `room_readiness_generation/output/`: paired variant images plus labels and cost logs.
- `room_readiness_generation/new_outputs/`: flattened category folders with `annotations.json`.

Useful dry-run commands:

```bash
python generate_base_images.py --dry-run
python main.py --dry-run
python main.py --subtask chairs --dry-run
```

Interactive review UI:

```bash
python app.py
```

Then open the local Flask URL printed by Flask, usually `http://127.0.0.1:5000`.

## Participant Classification Workflow

Put source images in `participant_classification_generation/base_images/`, then run:

```bash
cd participant_classification_generation
python datasetGenScript.py --prompt most_non --max-images 50
```

Prompt choices:

- `no_non`: all visible people should be meeting participants.
- `some_non`: a few visible non-participants are present.
- `most_non`: many visible non-participants are present.

To generate automatic boxes with Roboflow, start the local inference server first:

```bash
inference server start
```

Then run:

```bash
python roboflow_autoBounding.py \
  --image-folder generated_images \
  --output-json auto_boxes.json

python visualizeBoxes.py \
  --image-folder generated_images \
  --json-file auto_boxes.json \
  --output-folder preview_boxes
```

## Reproducibility Notes

- Keep prompt edits in source files so future runs are explainable.
- Keep generated datasets out of git; publish large outputs through a dataset store or release artifact instead.
- Use `--dry-run` where available before spending API credits.
- `room_readiness_generation/main.py` writes token and cost metadata to `output/cost_log.json`.
