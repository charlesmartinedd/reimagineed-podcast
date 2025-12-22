#!/usr/bin/env python3
"""Generate a branded Zoom background with logo and text overlay."""

import os
import requests
from openai import OpenAI
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

# Paths
SCRIPT_DIR = Path(__file__).parent
ASSETS_DIR = SCRIPT_DIR.parent / "assets"
OUTPUT_DIR = ASSETS_DIR / "zoom-backgrounds"
LOGO_PATH = ASSETS_DIR / "the-right-path-logo.png"
DOWNLOADS_DIR = Path("C:/Users/MarieLexisDad/Downloads")

# Brand colors
PURPLE = (107, 45, 139)  # #6B2D8B
CHARCOAL = (44, 44, 44)  # #2C2C2C

# Initialize OpenAI client
client = OpenAI()

def generate_background():
    """Generate a clean branded background."""
    print("Generating background image...")

    prompt = """A professional virtual meeting background with an AI and technology theme.
    Abstract digital neural network patterns, circuit board traces, and data visualization elements
    in purple (#6B2D8B) and light purple (#8B4DAB) on a darker sophisticated background.
    Futuristic but professional - think corporate tech keynote aesthetic.
    Glowing nodes, flowing data streams, subtle geometric patterns.
    Keep the upper right corner relatively clean/simple for logo placement.
    Large open space in the center-left for a speaker.
    16:9 aspect ratio. Modern, innovative, educational technology aesthetic.
    No text, no logos, just abstract AI/tech design elements."""

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="hd",
        n=1
    )

    image_url = response.data[0].url
    image_response = requests.get(image_url)
    return Image.open(io.BytesIO(image_response.content))

def add_branding(background):
    """Overlay logo and text on the background with white background box in top right."""
    print("Adding logo and text...")

    # Resize background to exact 1920x1080
    background = background.resize((1920, 1080), Image.LANCZOS)

    # Load and resize logo (20% larger: 120 * 1.2 = 144)
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo_size = 144
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Remove white background from logo - make white pixels transparent
    logo_data = logo.getdata()
    new_logo_data = []
    for pixel in logo_data:
        # If pixel is white or near-white, make it transparent
        if pixel[0] > 240 and pixel[1] > 240 and pixel[2] > 240:
            new_logo_data.append((255, 255, 255, 0))  # Fully transparent
        else:
            new_logo_data.append(pixel)
    logo.putdata(new_logo_data)

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

    # Create frosted glass effect behind logo and text
    background = background.convert("RGBA")

    # Larger padding for frosted glass area
    bg_padding = 30
    bg_left = int(logo_x - bg_padding)
    bg_top = int(logo_y - bg_padding)
    bg_right = int(logo_x + total_width + bg_padding)
    bg_bottom = int(logo_y + logo_size + bg_padding)

    # Crop the region where frosted glass will be
    frost_region = background.crop((bg_left, bg_top, bg_right, bg_bottom))

    # Apply strong Gaussian blur for frosted effect
    frost_region = frost_region.filter(ImageFilter.GaussianBlur(radius=15))

    # Create semi-transparent white overlay for the frost
    frost_overlay = Image.new('RGBA', frost_region.size, (255, 255, 255, 180))

    # Composite the blur and white overlay
    frost_region = Image.alpha_composite(frost_region, frost_overlay)

    # Paste frosted region back
    background.paste(frost_region, (bg_left, bg_top))

    # Add subtle border/glow around the frosted area
    overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(
        [bg_left, bg_top, bg_right, bg_bottom],
        radius=20,
        outline=(255, 255, 255, 100),
        width=2
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
    print("Generating Branded Zoom Background")
    print("=" * 60)

    # Generate background
    background = generate_background()

    # Add branding
    final_image = add_branding(background)

    # Save to zoom-backgrounds folder
    output_path = OUTPUT_DIR / "05_ai_tech_branded.png"
    final_image.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")

    # Also save to Downloads
    downloads_path = DOWNLOADS_DIR / "05_ai_tech_branded.png"
    final_image.save(downloads_path, "PNG", quality=95)
    print(f"Saved: {downloads_path}")

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)

    return str(output_path)

if __name__ == "__main__":
    main()
