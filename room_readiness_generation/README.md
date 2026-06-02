# Room Readiness Dataset Generation

Creates paired synthetic room images for environment-monitoring tasks.

## Pipeline

Run commands from this folder:

```bash
python generate_base_images.py
python main.py
python change_format.py
```

### Stage 1: Base Images

`generate_base_images.py` creates base room images with Gemini:

```text
base_images/
  meeting_room/meeting_room_01.png
  open_space/open_space_01.png
```

The current prompt lists contain 25 meeting-room prompts and 25 open-space prompts, for 50 base images total.

Useful command:

```bash
python generate_base_images.py --dry-run
```

### Stage 2: Variant Images

`main.py` creates paired variants for each base image:

| Change type | Clean/reference state | Changed state |
| --- | --- | --- |
| `whiteboard` | `whiteboard_clean` | `whiteboard_dirty` |
| `chairs` | `chairs_neat` | `chairs_messy` |
| `blinds` | `blinds_up` | `blinds_down` |
| `tables` | `tables_clean` | `tables_cluttered` |

Each base image produces 8 variant images, so the current 50 base images produce up to 400 variants.

Output layout:

```text
output/
  meeting_room/
    chairs_neat/meeting_room_01__chairs_neat.png
    chairs_messy/meeting_room_01__chairs_messy.png
  labels.json
  labels.csv
  cost_log.json
```

The changed state is generated from the clean/reference state for that subtask. For example, `chairs_messy` is generated from `chairs_neat`, not directly from the original base image.

Useful commands:

```bash
python main.py --dry-run
python main.py --subtask chairs
python main.py --subtask chairs --dry-run
```

### Stage 3: ML-Ready Format

`change_format.py` flattens `output/` into category folders:

```text
new_outputs/
  blinds/annotations.json
  chairs/annotations.json
  originals/
  tables/annotations.json
  whiteboard/annotations.json
```

This stage is local only and does not call an API.

## Interactive UI

```bash
python app.py
```

Open the Flask URL printed in the terminal, usually `http://127.0.0.1:5000`.

## Cost and Timing

The scripts sleep for 10 seconds after each API call, or about 6 calls per minute.

Approximate current run:

- Base images: 50 calls, about 8 minutes.
- Variants: 400 calls, about 67 minutes.
- Image generation cost estimate: about `450 * $0.039 = $17.55`, plus small token costs.

Use `--dry-run` before paid runs to verify folder layout and labels.
