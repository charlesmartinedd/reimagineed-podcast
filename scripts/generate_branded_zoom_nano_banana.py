#!/usr/bin/env python3
"""Generate a branded Zoom background using Nano Banana (Gemini 2.5 Flash Image) via OpenRouter."""

import os
import sys
import requests
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY not found in .env file")
    sys.exit(1)

# Paths
SCRIPT_DIR = Path(__file__).parent
ASSETS_DIR = SCRIPT_DIR.parent / "assets"
OUTPUT_DIR = ASSETS_DIR / "zoom-backgrounds"
LOGO_PATH = ASSETS_DIR / "the-right-path-logo.png"
DOWNLOADS_DIR = Path("C:/Users/MarieLexisDad/Downloads")

# Brand colors
PURPLE = (107, 45, 139)  # #6B2D8B
CHARCOAL = (44, 44, 44)  # #2C2C2C


def generate_nano_banana_background():
    """Generate background using Nano Banana (Gemini 2.5 Flash Image) via OpenRouter"""
    print("Generating background with Nano Banana (Gemini 2.5 Flash Image)...")

    prompt = """Create a professional virtual meeting background with an AI and technology theme.

Design elements:
- Abstract digital neural network patterns with glowing nodes
- Circuit board traces and data visualization elements
- Flowing data streams and geometric patterns
- Purple (#6B2D8B) and light purple (#8B4DAB) as primary colors
- Dark sophisticated background (deep navy or charcoal)
- Futuristic but professional aesthetic - corporate tech keynote style

Composition:
- Keep the upper right corner relatively clean/simple for logo placement
- Large open space in the center-left where a video speaker will appear
- 16:9 aspect ratio, 1920x1080 resolution
- Modern, innovative, educational technology aesthetic

Style: Clean, professional, tech-forward. Think Apple keynote or Microsoft Ignite presentation backgrounds.
NO TEXT, NO LOGOS - just abstract AI/tech design elements."""

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://therightpathpodcast.com",
        "X-Title": "The Right Path Podcast Zoom Background Generator"
    }

    payload = {
        "model": "google/gemini-2.5-flash-image",
        "modalities": ["image", "text"],
        "messages": [{
            "role": "user",
            "content": prompt
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()

        # Extract images from response
        images = result['choices'][0]['message'].get('images', [])

        if not images:
            print("No images returned from API")
            return None

        img_data = images[0]

        # Handle different response formats
        if isinstance(img_data, dict):
            if 'image_url' in img_data:
                img_url = img_data['image_url'].get('url', '')
            else:
                img_url = img_data.get('url', '')

            # Decode base64 image
            if img_url and img_url.startswith('data:image'):
                base64_data = img_url.split(',')[1]
                img_bytes = base64.b64decode(base64_data)
                return Image.open(io.BytesIO(img_bytes))

        return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def add_branding(background):
    """Overlay logo and text on the background with white background box."""
    print("Adding logo and text...")

    # Resize background to exact 1920x1080
    background = background.resize((1920, 1080), Image.LANCZOS)

    # Load and resize logo (20% larger: 120 * 1.2 = 144)
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo_size = 144
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Try to use a nice font
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 50)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/times.ttf", 50)
        except:
            font = ImageFont.load_default()

    # Calculate text size for positioning
    text = "The Right Path"
    draw = ImageDraw.Draw(background)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Position in top right with padding
    padding = 40
    total_width = logo_size + 15 + text_width

    # Calculate positions (top right corner)
    logo_x = 1920 - padding - total_width
    logo_y = padding
    text_x = logo_x + logo_size + 15
    text_y = logo_y + (logo_size // 2) - (text_height // 2)

    # Draw white rounded rectangle background behind logo and text
    background = background.convert("RGBA")

    # Create white background rectangle with padding
    bg_padding = 20
    bg_left = logo_x - bg_padding
    bg_top = logo_y - bg_padding
    bg_right = logo_x + total_width + bg_padding
    bg_bottom = logo_y + logo_size + bg_padding

    # Draw white background
    overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(
        [bg_left, bg_top, bg_right, bg_bottom],
        radius=15,
        fill=(255, 255, 255, 245)  # White, nearly opaque
    )
    background = Image.alpha_composite(background, overlay)

    # Paste logo onto background
    background.paste(logo, (logo_x, logo_y), logo)

    # Add text
    draw = ImageDraw.Draw(background)
    draw.text((text_x, text_y), text, font=font, fill=CHARCOAL)

    # Convert back to RGB for saving as PNG
    background = background.convert("RGB")
    return background


def main():
    print("=" * 60)
    print("Generating Branded Zoom Background with Nano Banana")
    print("=" * 60)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate background
    background = generate_nano_banana_background()

    if background is None:
        print("Failed to generate background image")
        return None

    # Add branding
    final_image = add_branding(background)

    # Save to zoom-backgrounds folder
    output_path = OUTPUT_DIR / "05_ai_tech_branded_nano_banana.png"
    final_image.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")

    # Also save to Downloads
    downloads_path = DOWNLOADS_DIR / "05_ai_tech_branded_nano_banana.png"
    final_image.save(downloads_path, "PNG", quality=95)
    print(f"Saved: {downloads_path}")

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)

    return str(output_path)


if __name__ == "__main__":
    main()
