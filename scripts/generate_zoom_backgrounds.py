#!/usr/bin/env python3
"""Generate Zoom background images for The Right Path Podcast using OpenAI DALL-E API."""

import os
import requests
from openai import OpenAI
from pathlib import Path

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "assets" / "zoom-backgrounds"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize OpenAI client
client = OpenAI()

# Image prompts
PROMPTS = {
    "01_minimal_geometric": """A professional Zoom background with a clean white backdrop (90% of the image).
Subtle geometric pattern in the lower right corner using purple (#6B2D8B) -
thin intersecting lines forming an abstract network/pathway design.
The pattern should be understated and not distracting.
Soft gradient shadow effect for depth.
16:9 aspect ratio, 1920x1080 resolution.
Minimalist, editorial, corporate aesthetic.""",

    "02_abstract_flow": """A professional Zoom background with predominantly white space (85%).
Soft, flowing abstract purple (#6B2D8B) curves sweeping from bottom left
toward upper right, suggesting a pathway or journey.
Lighter purple (#8B4DAB) secondary accents blending smoothly.
Clean, uncluttered composition with ample negative space in the center
where the speaker will appear.
16:9 aspect ratio, 1920x1080 resolution.
Modern, sophisticated, calming aesthetic.""",

    "03_professional_grid": """A professional Zoom background with white base (90%).
A subtle light gray grid pattern across the entire background (very faint).
Purple (#6B2D8B) accent elements: a thin horizontal line at the bottom
with three small circular icons representing education, employment, and
empowerment. Clean typography-inspired design elements.
Architectural, structured feel suggesting stability and guidance.
16:9 aspect ratio, 1920x1080 resolution.
Corporate, polished, trustworthy aesthetic."""
}

def generate_image(name: str, prompt: str) -> str:
    """Generate an image using DALL-E 3 and save it."""
    print(f"\n{'='*60}")
    print(f"Generating: {name}")
    print(f"{'='*60}")

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",  # Closest to 16:9 available
        quality="hd",
        n=1
    )

    image_url = response.data[0].url
    revised_prompt = response.data[0].revised_prompt

    print(f"Revised prompt: {revised_prompt[:100]}...")

    # Download the image
    image_response = requests.get(image_url)
    output_path = OUTPUT_DIR / f"{name}.png"

    with open(output_path, "wb") as f:
        f.write(image_response.content)

    print(f"Saved: {output_path}")
    return str(output_path)

def main():
    print("="*60)
    print("The Right Path Podcast - Zoom Background Generator")
    print("="*60)

    generated_files = []

    for name, prompt in PROMPTS.items():
        try:
            path = generate_image(name, prompt)
            generated_files.append(path)
        except Exception as e:
            print(f"Error generating {name}: {e}")

    print("\n" + "="*60)
    print("Generation Complete!")
    print("="*60)
    print(f"\nGenerated {len(generated_files)} images:")
    for f in generated_files:
        print(f"  - {f}")

    return generated_files

if __name__ == "__main__":
    main()
