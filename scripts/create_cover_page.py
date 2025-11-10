"""
Create ReimagineED Branding Guide Cover Page
Composite design using PIL/Pillow according to cover-page-design-spec.md
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path

def create_cover_page():
    """Create cover page composite image"""

    # Paths
    assets_dir = Path(__file__).parent.parent / "assets" / "branding-guide"
    hero_image_path = assets_dir / "cover_hero_image_1.png"
    output_path = assets_dir / "cover_page_final.png"

    # Load hero image
    print("Loading hero image...")
    hero = Image.open(hero_image_path)

    # Convert to RGB if needed
    if hero.mode != 'RGB':
        hero = hero.convert('RGB')

    # Resize to standard dimensions: 8.5" x 11" at 300 DPI = 2550 x 3300 pixels
    target_size = (2550, 3300)
    print(f"Resizing to {target_size[0]} x {target_size[1]}...")
    hero = hero.resize(target_size, Image.Resampling.LANCZOS)

    # Create darkening overlay (20% darker)
    print("Applying darkening overlay...")
    enhancer = ImageEnhance.Brightness(hero)
    hero = enhancer.enhance(0.7)  # 30% darker for better text contrast

    # Create gradient overlay (Navy to transparent, top to bottom)
    print("Creating gradient overlay...")
    gradient = Image.new('RGBA', target_size, color=(0, 0, 0, 0))
    draw_gradient = ImageDraw.Draw(gradient)

    navy_rgb = (11, 29, 58)  # #0B1D3A
    for y in range(target_size[1] // 3):  # Top third
        alpha = int(255 * 0.4 * (1 - y / (target_size[1] // 3)))  # Fade from 40% to 0%
        draw_gradient.rectangle(
            [(0, y), (target_size[0], y + 1)],
            fill=(*navy_rgb, alpha)
        )

    # Composite hero with gradient
    hero_rgba = hero.convert('RGBA')
    hero_with_gradient = Image.alpha_composite(hero_rgba, gradient)

    # Create drawing context
    draw = ImageDraw.Draw(hero_with_gradient)

    # Define colors
    white = (255, 255, 255, 255)
    gold = (255, 211, 58, 255)  # #FFD33A
    electric_blue = (0, 217, 255, 255)  # #00D9FF
    white_90 = (255, 255, 255, 230)
    white_70 = (255, 255, 255, 179)

    # Font sizes (scaled for 300 DPI)
    logo_size = 350  # 96pt @ 300 DPI
    tagline_size = 88  # 24pt @ 300 DPI
    mission_size = 66  # 18pt @ 300 DPI
    pillars_size = 40  # 11pt @ 300 DPI
    doc_title_size = 51  # 14pt @ 300 DPI

    # Load fonts (using system fonts - Arial as fallback)
    try:
        # Try to use better fonts if available
        logo_font = ImageFont.truetype("arialbd.ttf", logo_size)
        tagline_font = ImageFont.truetype("arial.ttf", tagline_size)
        mission_font = ImageFont.truetype("arial.ttf", mission_size)
        pillars_font = ImageFont.truetype("cour.ttf", pillars_size)  # Courier as mono fallback
        doc_title_font = ImageFont.truetype("arial.ttf", doc_title_size)
    except:
        print("Using default fonts...")
        logo_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
        mission_font = ImageFont.load_default()
        pillars_font = ImageFont.load_default()
        doc_title_font = ImageFont.load_default()

    # 1. Draw Logo "REIMAGINED" (split into two lines)
    print("Adding logo...")
    logo_x = int(target_size[0] * 0.08)  # 8% from left
    logo_y = int(target_size[1] * 0.10)  # 10% from top

    # "REIMAGINE" in white
    draw.text((logo_x, logo_y), "REIMAGINE", font=logo_font, fill=white)

    # "ED" in gold with slight offset
    ed_y = logo_y + int(logo_size * 0.85)  # Below "REIMAGINE"
    draw.text((logo_x, ed_y), "ED", font=logo_font, fill=gold)

    # 2. Draw Tagline
    print("Adding tagline...")
    tagline_y = ed_y + int(logo_size * 1.2)
    draw.text(
        (logo_x, tagline_y),
        "THE DISRUPTOR IN AI EDUCATION",
        font=tagline_font,
        fill=electric_blue
    )

    # 3. Draw Mission Statement (multi-line)
    print("Adding mission statement...")
    mission_y = int(target_size[1] * 0.40)  # 40% from top
    mission_lines = [
        "Centering Black and Latino Educators at the",
        "Forefront of the AI Revolution in Education"
    ]

    for i, line in enumerate(mission_lines):
        draw.text(
            (logo_x, mission_y + i * int(mission_size * 1.6)),
            line,
            font=mission_font,
            fill=white_90
        )

    # 4. Draw Brand Pillars (bottom third)
    print("Adding brand pillars...")
    pillars_y = int(target_size[1] * 0.80)  # 80% from top
    pillars_text = "AI LITERACY  |  WORKFORCE DEVELOPMENT  |  EQUITY  |  INNOVATION  |  COMMUNITY"

    # Center the pillars
    pillars_bbox = draw.textbbox((0, 0), pillars_text, font=pillars_font)
    pillars_width = pillars_bbox[2] - pillars_bbox[0]
    pillars_x = (target_size[0] - pillars_width) // 2

    draw.text(
        (pillars_x, pillars_y),
        pillars_text,
        font=pillars_font,
        fill=gold
    )

    # 5. Draw Document Title (bottom)
    print("Adding document title...")
    doc_title_y = int(target_size[1] * 0.92)  # 92% from top
    draw.text(
        (logo_x, doc_title_y),
        "BRAND GUIDE 2025",
        font=doc_title_font,
        fill=white_70
    )

    # 6. Add subtle tech elements (geometric shapes)
    print("Adding tech visual elements...")
    # Draw some subtle hexagons and circles on the right side
    tech_x_start = int(target_size[0] * 0.65)  # Right third

    # Semi-transparent shapes
    tech_overlay = Image.new('RGBA', target_size, (0, 0, 0, 0))
    tech_draw = ImageDraw.Draw(tech_overlay)

    # Gold hexagon (subtle)
    hex_size = 150
    hex_x = tech_x_start + 200
    hex_y = int(target_size[1] * 0.25)
    tech_draw.regular_polygon(
        (hex_x, hex_y, hex_size),
        n_sides=6,
        rotation=30,
        fill=(*gold[:3], 38)  # 15% opacity
    )

    # Electric blue circle
    circle_x = tech_x_start + 400
    circle_y = int(target_size[1] * 0.50)
    circle_radius = 100
    tech_draw.ellipse(
        [circle_x - circle_radius, circle_y - circle_radius,
         circle_x + circle_radius, circle_y + circle_radius],
        fill=(*electric_blue[:3], 25)  # 10% opacity
    )

    # Composite tech elements
    hero_with_gradient = Image.alpha_composite(hero_with_gradient, tech_overlay)

    # Convert back to RGB for final save
    final_image = hero_with_gradient.convert('RGB')

    # Save
    print(f"Saving cover page to {output_path}...")
    final_image.save(output_path, 'PNG', quality=95, dpi=(300, 300))

    print(f"\nCover page created successfully!")
    print(f"File: {output_path}")
    print(f"Size: {final_image.size}")
    print(f"File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("ReimagineED Cover Page Creator")
    print("=" * 60)

    cover_page = create_cover_page()

    print("\nNext step: Validate with GPT-5 Vision")
    print("Expected score: >= 90/100")
