import argparse
import json
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render bounding box preview images.")
    parser.add_argument(
        "--image-folder",
        type=Path,
        default=Path("generated_images"),
        help="Folder containing images referenced by the JSON file.",
    )
    parser.add_argument(
        "--json-file",
        type=Path,
        default=Path("auto_boxes.json"),
        help="Bounding box annotation JSON file.",
    )
    parser.add_argument(
        "--output-folder",
        type=Path,
        default=Path("preview_boxes"),
        help="Folder where preview images will be written.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_folder.mkdir(parents=True, exist_ok=True)

    with open(args.json_file, "r") as f:
        data = json.load(f)

    for item in data:
        img_path = args.image_folder / item["file_name"]
        img = cv2.imread(str(img_path))

        if img is None:
            print("Could not read:", img_path)
            continue

        for person in item["people"]:
            x1, y1, x2, y2 = person["bbox"]
            pid = person["id"]

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label_text = f"id:{pid}"

            (w, h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(img, (x1, y1 - h - 5), (x1 + w, y1), (0, 255, 0), -1)
            cv2.putText(
                img,
                label_text,
                (x1, y1 - 3),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                1,
            )

        out_path = args.output_folder / item["file_name"]
        cv2.imwrite(str(out_path), img)

    print(f"Done. Check the folder: {args.output_folder}")


if __name__ == "__main__":
    main()
