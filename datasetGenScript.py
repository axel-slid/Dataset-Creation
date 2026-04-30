from pathlib import Path
from google import genai
from PIL import Image
import geminiPrompts as p

#export GEMINI_API_KEY=""

INPUT_FOLDER = Path("base_images/open_spaceXall_participants")
OUTPUT_FOLDER = Path("generated_images/zoom")
MODEL_NAME = "gemini-2.5-flash-image"
MAX_IMAGES = 25

PROMPT = p.SOME_NON_PROMPT #depends on whether the generated image is filled with participants or includes non-participants
def main():
    if not INPUT_FOLDER.exists():
        raise FileNotFoundError(f"Input folder not found: {INPUT_FOLDER}")

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    client = genai.Client()

    valid_exts = {".png", ".jpg", ".jpeg", ".webp"}
    image_paths = sorted(
        p for p in INPUT_FOLDER.iterdir()
        if p.is_file() and p.suffix.lower() in valid_exts
    )[:MAX_IMAGES]

    if not image_paths:
        raise FileNotFoundError(
            f"No supported images found in {INPUT_FOLDER}. "
            f"Supported types: {', '.join(sorted(valid_exts))}"
        )

    print(f"Processing {len(image_paths)} image(s)...")

    for i, image_path in enumerate(image_paths, start=1):
        print(f"[{i}/{len(image_paths)}] Editing {image_path.name}")

        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=[PROMPT, img],
                )

            #output_path = OUTPUT_FOLDER / f"no_non_participants_{i}.png"
            #output_path = OUTPUT_FOLDER / f"some_non_participants_{i}.png"
            output_path = OUTPUT_FOLDER / f"most_non_participants_{i}.png"
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