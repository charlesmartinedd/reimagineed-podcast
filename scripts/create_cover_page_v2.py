"""
Create ReimagineED Branding Guide Cover Page V2 - REFINED
Improvements based on GPT Vision feedback:
- Enhanced contrast and sharpness
- Better text readability with shadows/outlines
- Concise mission statement
- Bolder, more unconventional layout
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path

def create_cover_page_v2():
    """Create refined cover page - aiming for 90+ score"""

    # Paths
    assets_dir = Path(__file__).parent.parent / "assets" / "branding-guide"
    hero_image_path = assets_dir / "cover_hero_image_1.png"
    output_path = assets_dir / "cover_page_v2.png"

    # Load hero image
    print("Loading hero image...")
    hero = Image.open(hero_image_path)

    # Convert to RGB
    if hero.mode != 'RGB':
        hero = hero.convert('RGB')

    # Resize to 8.5" x 11" at 300 DPI
    target_size = (2550, 3300)
    print(f"Resizing to {target_size[0]} x {target_size[1]}...")
    hero = hero.resize(target_size, Image.Resampling.LANCZOS)

    # ENHANCED: Increase sharpness
    print("Enhancing sharpness...")
    hero = hero.filter(ImageFilter.SHARPEN)

    # ENHANCED: Darken MORE (50% instead of 30%) for better text contrast
    print("Applying enhanced darkening overlay (50%)...")
    enhancer = ImageEnhance.Brightness(hero)
    hero = enhancer.enhance(0.5)  # 50% darker

    # Increase contrast
    contrast_enhancer = ImageEnhance.Contrast(hero)
    hero = contrast_enhancer.enhance(1.3)  # 30% more contrast

    # Create stronger gradient overlay
    print("Creating enhanced gradient overlay...")
    gradient = Image.new('RGBA', target_size, color=(0, 0, 0, 0))
    draw_gradient = ImageDraw.Draw(gradient)

    navy_rgb = (11, 29, 58)
    for y in range(target_size[1] // 2):  # Top HALF instead of third
        alpha = int(255 * 0.6 * (1 - y / (target_size[1] // 2)))  # 60% opacity at top
        draw_gradient.rectangle(
            [(0, y), (target_size[0], y + 1)],
            fill=(*navy_rgb, alpha)
        )

    # Composite
    hero_rgba = hero.convert('RGBA')
    hero_with_gradient = Image.alpha_composite(hero_rgba, gradient)

    # Create drawing context
    draw = ImageDraw.Draw(hero_with_gradient)

    # Colors
    white = (255, 255, 255, 255)
    gold = (255, 211, 58, 255)
    electric_blue = (0, 217, 255, 255)
    white_90 = (255, 255, 255, 230)
    white_70 = (255, 255, 255, 179)
    black_shadow = (0, 0, 0, 128)  # For text shadows

    # Font sizes
    logo_size = 380  # LARGER - was 350
    tagline_size = 95  # LARGER - was 88
    mission_size = 72  # LARGER - was 66
    pillars_size = 44  # LARGER - was 40
    doc_title_size = 55  # LARGER - was 51

    # Load fonts
    try:
        logo_font = ImageFont.truetype("arialbd.ttf", logo_size)
        tagline_font = ImageFont.truetype("arialbd.ttf", tagline_size)  # BOLD for tagline
        mission_font = ImageFont.truetype("arial.ttf", mission_size)
        pillars_font = ImageFont.truetype("courbd.ttf", pillars_size)  # BOLD courier
        doc_title_font = ImageFont.truetype("arial.ttf", doc_title_size)
    except:
        print("Using default fonts...")
        logo_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
        mission_font = ImageFont.load_default()
        pillars_font = ImageFont.load_default()
        doc_title_font = ImageFont.load_default()

    # Helper function: Draw text with shadow for better legibility
    def draw_text_with_shadow(xy, text, font, fill, shadow_offset=4):
        x, y = xy
        # Draw shadow
        draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=black_shadow)
        # Draw text
        draw.text((x, y), text, font=font, fill=fill)

    # 1. LOGO - MORE DRAMATIC placement
    print("Adding enhanced logo...")
    logo_x = int(target_size[0] * 0.08)
    logo_y = int(target_size[1] * 0.08)  # Higher up - was 0.10

    # "REIMAGINE" in white with shadow
    draw_text_with_shadow((logo_x, logo_y), "REIMAGINE", logo_font, white, shadow_offset=6)

    # "ED" in GLOWING gold
    ed_y = logo_y + int(logo_size * 0.80)

    # Add multiple layers for GLOW effect
    for offset in range(8, 2, -1):
        glow_alpha = int(255 * (offset / 10))
        draw.text((logo_x - offset, ed_y - offset), "ED", font=logo_font, fill=(*gold[:3], glow_alpha))
        draw.text((logo_x + offset, ed_y - offset), "ED", font=logo_font, fill=(*gold[:3], glow_alpha))

    # Final "ED" text
    draw.text((logo_x, ed_y), "ED", font=logo_font, fill=gold)

    # 2. TAGLINE - with glow
    print("Adding enhanced tagline...")
    tagline_y = ed_y + int(logo_size * 1.1)
    tagline_text = "THE DISRUPTOR IN AI EDUCATION"

    # Glow effect for tagline
    for offset in range(6, 1, -1):
        glow_alpha = int(255 * (offset / 8))
        draw.text(
            (logo_x + offset, tagline_y + offset),
            tagline_text,
            font=tagline_font,
            fill=(*electric_blue[:3], glow_alpha)
        )

    draw.text((logo_x, tagline_y), tagline_text, font=tagline_font, fill=electric_blue)

    # 3. MISSION STATEMENT - STREAMLINED & CONCISE
    print("Adding streamlined mission statement...")
    mission_y = int(target_size[1] * 0.42)

    # NEW: Shorter, punchier mission
    mission_text = "Leading the AI Revolution in Education"

    # Large text box with dark semi-transparent background for contrast
    mission_bbox = draw.textbbox((0, 0), mission_text, font=mission_font)
    mission_width = mission_bbox[2] - mission_bbox[0]
    mission_height = mission_bbox[3] - mission_bbox[1]

    # Dark background box for legibility
    box_padding = 30
    draw.rectangle(
        [
            logo_x - box_padding,
            mission_y - box_padding,
            logo_x + mission_width + box_padding,
            mission_y + mission_height + box_padding
        ],
        fill=(11, 29, 58, 200)  # Navy with 78% opacity
    )

    # Draw mission text
    draw.text((logo_x, mission_y), mission_text, font=mission_font, fill=white)

    # 4. BRAND PILLARS - More prominent
    print("Adding brand pillars...")
    pillars_y = int(target_size[1] * 0.85)
    pillars_text = "AI • WORKFORCE • EQUITY • INNOVATION • COMMUNITY"

    # Center and add shadow
    pillars_bbox = draw.textbbox((0, 0), pillars_text, font=pillars_font)
    pillars_width = pillars_bbox[2] - pillars_bbox[0]
    pillars_x = (target_size[0] - pillars_width) // 2

    draw_text_with_shadow((pillars_x, pillars_y), pillars_text, pillars_font, gold, shadow_offset=3)

    # 5. DOCUMENT TITLE
    print("Adding document title...")
    doc_title_y = int(target_size[1] * 0.94)
    draw.text((logo_x, doc_title_y), "BRAND GUIDE 2025", font=doc_title_font, fill=white_70)

    # 6. BOLD TECH ELEMENTS - More prominent
    print("Adding enhanced tech elements...")
    tech_overlay = Image.new('RGBA', target_size, (0, 0, 0, 0))
    tech_draw = ImageDraw.Draw(tech_overlay)

    # Larger, more visible shapes
    tech_x_start = int(target_size[0] * 0.60)

    # Large gold hexagon
    hex_size = 250  # Was 150
    hex_x = tech_x_start + 300
    hex_y = int(target_size[1] * 0.22)
    tech_draw.regular_polygon(
        (hex_x, hex_y, hex_size),
        n_sides=6,
        rotation=30,
        fill=(*gold[:3], 60)  # More visible - was 38
    )

    # Electric blue circle
    circle_x = tech_x_start + 500
    circle_y = int(target_size[1] * 0.48)
    circle_radius = 180  # Was 100
    tech_draw.ellipse(
        [circle_x - circle_radius, circle_y - circle_radius,
         circle_x + circle_radius, circle_y + circle_radius],
        fill=(*electric_blue[:3], 45)  # More visible - was 25
    )

    # Add a purple hexagon too
    hex2_size = 200
    hex2_x = tech_x_start + 100
    hex2_y = int(target_size[1] * 0.65)
    purple = (123, 47, 255)  # #7B2FFF
    tech_draw.regular_polygon(
        (hex2_x, hex2_y, hex2_size),
        n_sides=6,
        rotation=0,
        fill=(*purple, 40)
    )

    # Composite tech elements
    hero_with_gradient = Image.alpha_composite(hero_with_gradient, tech_overlay)

    # Convert to RGB
    final_image = hero_with_gradient.convert('RGB')

    # FINAL ENHANCEMENT: Slight sharpening pass
    final_image = final_image.filter(ImageFilter.SHARPEN)

    # Save
    print(f"Saving refined cover page to {output_path}...")
    final_image.save(output_path, 'PNG', quality=100, dpi=(300, 300))

    print(f"\nCover page V2 created successfully!")
    print(f"File: {output_path}")
    print(f"Improvements:")
    print("  - 50% darker hero image for better contrast")
    print("  - Text shadows and glows for legibility")
    print("  - Streamlined mission statement")
    print("  - Larger, bolder typography")
    print("  - More prominent tech elements")
    print("  - Enhanced sharpness and contrast")

    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("ReimagineED Cover Page Creator V2 (REFINED)")
    print("=" * 60)

    cover_page = create_cover_page_v2()

    print("\nNext: Validate with GPT-5 Vision (target: >=90/100)")
