import argparse
import os
import json
from pathlib import Path

from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient

load_dotenv()

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate automatic bounding boxes with a local Roboflow inference server."
    )
    parser.add_argument(
        "--image-folder",
        type=Path,
        default=Path("generated_images"),
        help="Folder containing generated images.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("auto_boxes.json"),
        help="Path to write bounding box annotations.",
    )
    parser.add_argument(
        "--model-id",
        default="find-human-heads/1",
        help="Roboflow model id.",
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:9001",
        help="Roboflow inference server URL.",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.6,
        help="Minimum confidence score to keep a prediction.",
    )
    parser.add_argument(
        "--role",
        default="participant",
        help="Role assigned to each generated person annotation.",
    )
    return parser.parse_args()

def convert_bbox(pred):
    """
    Roboflow gives x, y as the CENTER of the box.
    Convert to [x_min, y_min, x_max, y_max].
    """
    x_center = pred["x"]
    y_center = pred["y"]
    width = pred["width"]
    height = pred["height"]

    x_min = x_center - width / 2
    y_min = y_center - height / 2
    x_max = x_center + width / 2
    y_max = y_center + height / 2

    return [
        int(round(x_min)),
        int(round(y_min)),
        int(round(x_max)),
        int(round(y_max))
    ]


def get_predictions(result):
    """
    Handles different Roboflow response formats.
    """
    if isinstance(result, list):
        return result[0].get("predictions", [])

    if isinstance(result, dict):
        if "predictions" in result:
            return result["predictions"]
        if "outputs" in result:
            return result["outputs"][0].get("predictions", [])

    return []


# -----------------------------
# MAIN SCRIPT
# -----------------------------

def main() -> None:
    args = parse_args()
    image_folder = args.image_folder

    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing ROBOFLOW_API_KEY. Run:\n"
            "export ROBOFLOW_API_KEY='your_key_here'"
        )

    client = InferenceHTTPClient(
        api_url=args.api_url,
        api_key=api_key,
    )

    if not image_folder.exists():
        raise FileNotFoundError(f"Image folder not found: {image_folder}")

    output_data = []

    image_files = sorted(
        [file for file in image_folder.iterdir()
         if file.suffix.lower() in VALID_EXTENSIONS],
        key=lambda path: path.name,
    )

    print(f"Found {len(image_files)} images.")

    for image_path in image_files:
        print(f"Processing {image_path.name}...")

        result = client.infer(
            inference_input=str(image_path),
            model_id=args.model_id,
        )

        predictions = get_predictions(result)

        people = []

        for i, pred in enumerate(predictions):
            label = pred.get("class", "")

            confidence = pred.get("confidence", 0)

            if confidence < args.confidence_threshold:
                continue

            bbox = convert_bbox(pred)

            people.append({
                "id": i,
                "bbox": bbox,
                "role": args.role,
                "confidence": round(confidence, 4)
            })

        output_data.append({
            "file_name": image_path.name,
            "people": people
        })

        print(f"  Found {len(people)} people.")

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_json, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"\nDone! Saved results to {args.output_json}")


if __name__ == "__main__":
    main()
