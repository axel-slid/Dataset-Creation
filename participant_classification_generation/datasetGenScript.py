import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from PIL import Image

import geminiPrompts as p

load_dotenv()

PROMPTS = {
    "no_non": p.NO_NON_PROMPT,
    "some_non": p.SOME_NON_PROMPT,
    "most_non": p.MOST_NON_PROMPT,
}

DEFAULT_OUTPUT_PREFIX = {
    "no_non": "no_non_participants",
    "some_non": "some_non_participants",
    "most_non": "most_non_participants",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate participant/non-participant edited images with Gemini."
    )
    parser.add_argument(
        "--input-folder",
        type=Path,
        default=Path("base_images"),
        help="Folder containing source images.",
    )
    parser.add_argument(
        "--output-folder",
        type=Path,
        default=Path("generated_images"),
        help="Folder where generated images will be written.",
    )
    parser.add_argument(
        "--prompt",
        choices=sorted(PROMPTS),
        default="most_non",
        help="Prompt scenario to use.",
    )
    parser.add_argument(
        "--output-prefix",
        help="Filename prefix for generated images. Defaults to the prompt scenario.",
    )
    parser.add_argument(
        "--model",
        default="gemini-2.5-flash-image",
        help="Gemini image model name.",
    )
    parser.add_argument(
        "--max-images",
        type=int,
        default=50,
        help="Maximum number of source images to process.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_folder = args.input_folder
    output_folder = args.output_folder
    prompt = PROMPTS[args.prompt]
    output_prefix = args.output_prefix or DEFAULT_OUTPUT_PREFIX[args.prompt]

    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError(
            "Missing GEMINI_API_KEY. Set it in the environment or in a local .env file."
        )

    if not input_folder.exists():
        raise FileNotFoundError(f"Input folder not found: {input_folder}")

    output_folder.mkdir(parents=True, exist_ok=True)

    client = genai.Client()

    valid_exts = {".png", ".jpg", ".jpeg", ".webp"}
    image_paths = sorted(
        path for path in input_folder.iterdir()
        if path.is_file() and path.suffix.lower() in valid_exts
    )[:args.max_images]

    if not image_paths:
        raise FileNotFoundError(
            f"No supported images found in {input_folder}. "
            f"Supported types: {', '.join(sorted(valid_exts))}"
        )

    print(f"Processing {len(image_paths)} image(s)...")

    for i, image_path in enumerate(image_paths, start=1):
        print(f"[{i}/{len(image_paths)}] Editing {image_path.name}")

        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")

                response = client.models.generate_content(
                    model=args.model,
                    contents=[prompt, img],
                )

            output_path = output_folder / f"{output_prefix}_{i:03d}.png"
            saved = False

            for part in response.parts:
                if getattr(part, "inline_data", None) is not None:
                    edited_image = part.as_image()
                    edited_image.save(output_path)
                    print(f"Saved to {output_path}")
                    saved = True
                    break

                if getattr(part, "text", None):
                    print(f"Model message for {image_path.name}: {part.text}")

            if not saved:
                print(f"No image output returned for {image_path.name}")

        except Exception as e:
            print(f"Failed on {image_path.name}: {e}")


if __name__ == "__main__":
    main()
