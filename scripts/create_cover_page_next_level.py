"""
ReimagineED Branding Guide - NEXT LEVEL Cover Page
Ultra-premium Madison Avenue quality with sophisticated design techniques
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path
import math

def create_next_level_cover():
    """Create the ultimate cover page - next level elegance and impact"""

    # Paths
    assets_dir = Path(__file__).parent.parent / "assets" / "branding-guide"
    hero_image_path = assets_dir / "cover_hero_image_1.png"
    output_path = assets_dir / "cover_page_next_level.png"

    print("=" * 70)
    print("CREATING NEXT LEVEL COVER PAGE")
    print("=" * 70)

    # Load and prepare hero image
    print("\n[1/10] Loading hero image...")
    hero = Image.open(hero_image_path)
    if hero.mode != 'RGB':
        hero = hero.convert('RGB')

    # Target: 8.5" x 11" at 300 DPI
    target_size = (2550, 3300)
    print(f"[2/10] Resizing to {target_size[0]}x{target_size[1]}...")
    hero = hero.resize(target_size, Image.Resampling.LANCZOS)

    # NEXT LEVEL: Triple enhancement pass
    print("[3/10] Applying professional image enhancements...")

    # Pass 1: Sharpness
    hero = hero.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Pass 2: Darken for text contrast (60%)
    enhancer = ImageEnhance.Brightness(hero)
    hero = enhancer.enhance(0.4)  # 60% darker

    # Pass 3: Increase contrast dramatically
    contrast_enhancer = ImageEnhance.Contrast(hero)
    hero = contrast_enhancer.enhance(1.5)  # 50% more contrast

    # Pass 4: Color saturation boost
    color_enhancer = ImageEnhance.Color(hero)
    hero = color_enhancer.enhance(1.2)  # 20% more vibrant

    # NEXT LEVEL: Sophisticated gradient overlay system
    print("[4/10] Creating sophisticated gradient system...")
    hero_rgba = hero.convert('RGBA')

    # Multi-layer gradient for depth
    gradient_overlay = Image.new('RGBA', target_size, (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient_overlay)

    navy_rgb = (11, 29, 58)
    gold_rgb = (255, 211, 58)

    # Top-to-middle: Navy gradient (strong)
    for y in range(target_size[1] // 2):
        alpha = int(255 * 0.75 * (1 - y / (target_size[1] // 2)))
        gradient_draw.rectangle([(0, y), (target_size[0], y + 1)], fill=(*navy_rgb, alpha))

    # Bottom accent: Subtle gold gradient
    for y in range(target_size[1] // 2, target_size[1]):
        alpha = int(255 * 0.15 * ((y - target_size[1] // 2) / (target_size[1] // 2)))
        gradient_draw.rectangle([(0, y), (target_size[0], y + 1)], fill=(*gold_rgb, alpha))

    # Composite
    hero_with_gradient = Image.alpha_composite(hero_rgba, gradient_overlay)

    # NEXT LEVEL: Create sophisticated tech pattern overlay
    print("[5/10] Adding premium tech pattern overlay...")
    pattern_overlay = Image.new('RGBA', target_size, (0, 0, 0, 0))
    pattern_draw = ImageDraw.Draw(pattern_overlay)

    # Subtle grid lines (right side only)
    grid_color = (0, 217, 255, 15)  # Electric blue, very subtle
    grid_spacing = 100
    for x in range(target_size[0] // 2, target_size[0], grid_spacing):
        pattern_draw.line([(x, 0), (x, target_size[1])], fill=grid_color, width=1)
    for y in range(0, target_size[1], grid_spacing):
        pattern_draw.line([(target_size[0] // 2, y), (target_size[0], y)], fill=grid_color, width=1)

    hero_with_gradient = Image.alpha_composite(hero_with_gradient, pattern_overlay)

    # Create main drawing context
    draw = ImageDraw.Draw(hero_with_gradient)

    # Premium color palette
    white = (255, 255, 255, 255)
    gold = (255, 211, 58, 255)
    electric_blue = (0, 217, 255, 255)
    white_95 = (255, 255, 255, 242)
    white_80 = (255, 255, 255, 204)
    black_shadow = (0, 0, 0, 180)

    # NEXT LEVEL: Premium font sizing
    logo_size = 420  # Even larger
    tagline_size = 100
    mission_size = 75
    pillars_size = 48
    doc_title_size = 58

    # Load fonts
    try:
        logo_font = ImageFont.truetype("arialbd.ttf", logo_size)
        tagline_font = ImageFont.truetype("arial.ttf", tagline_size)
        mission_font = ImageFont.truetype("arial.ttf", mission_size)
        pillars_font = ImageFont.truetype("courbd.ttf", pillars_size)
        doc_title_font = ImageFont.truetype("arial.ttf", doc_title_size)
    except:
        logo_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
        mission_font = ImageFont.load_default()
        pillars_font = ImageFont.load_default()
        doc_title_font = ImageFont.load_default()

    # NEXT LEVEL: Professional shadow system
    def draw_text_with_premium_shadow(xy, text, font, fill, shadow_color=black_shadow, shadow_offset=6, blur=True):
        """Draw text with professional multi-layer shadow"""
        x, y = xy

        # Create temporary layer for shadow with blur
        if blur:
            shadow_layer = Image.new('RGBA', target_size, (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_layer)
            shadow_draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=4))
            hero_with_gradient.alpha_composite(shadow_layer)
        else:
            draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)

        # Draw main text
        draw.text((x, y), text, font=font, fill=fill)

    # NEXT LEVEL: Multi-layer glow effect
    def draw_text_with_glow(xy, text, font, fill, glow_color, glow_intensity=10):
        """Create professional glow effect"""
        x, y = xy

        # Create glow layer
        glow_layer = Image.new('RGBA', target_size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)

        # Multiple glow passes
        for i in range(glow_intensity, 0, -2):
            alpha = int(255 * (i / glow_intensity) * 0.3)
            glow_draw.text((x, y), text, font=font, fill=(*glow_color[:3], alpha))

        # Blur the glow
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=15))
        hero_with_gradient.alpha_composite(glow_layer)

        # Draw main text
        draw.text((x, y), text, font=font, fill=fill)

    print("[6/10] Adding premium logo with effects...")
    logo_x = int(target_size[0] * 0.08)
    logo_y = int(target_size[1] * 0.10)

    # "REIMAGINE" in white with premium shadow
    draw_text_with_premium_shadow((logo_x, logo_y), "REIMAGINE", logo_font, white, shadow_offset=8)

    # "ED" in GLOWING gold with premium effects
    ed_y = logo_y + int(logo_size * 0.85)
    draw_text_with_glow((logo_x, ed_y), "ED", logo_font, gold, gold_rgb, glow_intensity=12)

    print("[7/10] Adding sophisticated tagline...")
    tagline_y = ed_y + int(logo_size * 1.2)
    tagline_text = "Empowering Educators, Innovating Futures"

    # Premium shadow for tagline
    draw_text_with_premium_shadow((logo_x, tagline_y), tagline_text, tagline_font, electric_blue, shadow_offset=5)

    print("[8/10] Adding refined mission statement...")
    mission_y = int(target_size[1] * 0.50)
    mission_text = "Leading the AI Revolution in Education"

    # Sophisticated background box with gradient
    mission_bbox = draw.textbbox((0, 0), mission_text, font=mission_font)
    mission_width = mission_bbox[2] - mission_bbox[0]
    mission_height = mission_bbox[3] - mission_bbox[1]

    box_padding = 40
    box_left = logo_x - box_padding
    box_top = mission_y - box_padding
    box_right = logo_x + mission_width + box_padding
    box_bottom = mission_y + mission_height + box_padding

    # Create gradient box background
    for i in range(box_top, box_bottom, 2):
        alpha_gradient = 220 - int(20 * ((i - box_top) / (box_bottom - box_top)))
        draw.rectangle([(box_left, i), (box_right, i+2)], fill=(*navy_rgb, alpha_gradient))

    # Gold accent line at bottom of box
    draw.rectangle([(box_left, box_bottom - 4), (box_right, box_bottom)], fill=gold)

    draw.text((logo_x, mission_y), mission_text, font=mission_font, fill=white_95)

    print("[9/10] Adding elegant brand pillars...")
    pillars_y = int(target_size[1] * 0.88)
    pillars_text = "AI LITERACY  •  WORKFORCE DEVELOPMENT  •  EQUITY  •  INNOVATION  •  COMMUNITY"

    # Center pillars
    pillars_bbox = draw.textbbox((0, 0), pillars_text, font=pillars_font)
    pillars_width = pillars_bbox[2] - pillars_bbox[0]
    pillars_x = (target_size[0] - pillars_width) // 2

    draw_text_with_premium_shadow((pillars_x, pillars_y), pillars_text, pillars_font, gold, shadow_offset=4, blur=True)

    print("[10/10] Adding premium geometric elements...")
    # Sophisticated geometric shapes
    geom_overlay = Image.new('RGBA', target_size, (0, 0, 0, 0))
    geom_draw = ImageDraw.Draw(geom_overlay)

    # Large elegant hexagon (gold)
    hex_x = int(target_size[0] * 0.75)
    hex_y = int(target_size[1] * 0.25)
    hex_size = 280

    # Draw hexagon with gradient fill
    for i in range(hex_size, 0, -5):
        alpha = int(70 * (i / hex_size))
        geom_draw.regular_polygon((hex_x, hex_y, i), n_sides=6, rotation=30, fill=(*gold_rgb, alpha))

    # Circle (electric blue)
    circle_x = int(target_size[0] * 0.80)
    circle_y = int(target_size[1] * 0.55)
    circle_radius = 200

    for i in range(circle_radius, 0, -5):
        alpha = int(60 * (i / circle_radius))
        geom_draw.ellipse([circle_x - i, circle_y - i, circle_x + i, circle_y + i],
                         fill=(0, 217, 255, alpha))

    # Small accent hexagon (purple)
    hex2_x = int(target_size[0] * 0.68)
    hex2_y = int(target_size[1] * 0.70)
    hex2_size = 180
    purple_rgb = (123, 47, 255)

    for i in range(hex2_size, 0, -5):
        alpha = int(50 * (i / hex2_size))
        geom_draw.regular_polygon((hex2_x, hex2_y, i), n_sides=6, rotation=0, fill=(*purple_rgb, alpha))

    # Composite geometry
    hero_with_gradient = Image.alpha_composite(hero_with_gradient, geom_overlay)

    # Recreate draw context after composite
    draw = ImageDraw.Draw(hero_with_gradient)

    # Add dark overlay at bottom to cover any unwanted text from hero image
    bottom_overlay_y = int(target_size[1] * 0.83)
    for y in range(bottom_overlay_y, target_size[1]):
        # Strong darkening overlay that fully covers any text
        progress = (y - bottom_overlay_y) / (target_size[1] - bottom_overlay_y)
        alpha = int(200 + (55 * progress))
        draw.rectangle([(0, y), (target_size[0], y + 1)], fill=(*navy_rgb, alpha))

    # Document title (last, on top)
    doc_title_y = int(target_size[1] * 0.95)
    draw.text((logo_x, doc_title_y), "BRAND GUIDE 2025", font=doc_title_font, fill=white_80)

    # Final conversion
    final_image = hero_with_gradient.convert('RGB')

    # NEXT LEVEL: Final polish pass
    final_image = final_image.filter(ImageFilter.UnsharpMask(radius=1, percent=100, threshold=2))

    # Save with maximum quality
    print(f"\nSaving next-level cover page...")
    final_image.save(output_path, 'PNG', quality=100, dpi=(300, 300), optimize=False)

    print("\n" + "=" * 70)
    print("NEXT LEVEL COVER PAGE CREATED")
    print("=" * 70)
    print(f"File: {output_path}")
    print(f"Size: {final_image.size}")
    print(f"File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
    print("\nPremium features applied:")
    print("  - Triple-pass image enhancement")
    print("  - Sophisticated multi-layer gradients")
    print("  - Premium shadow system with blur")
    print("  - Professional glow effects")
    print("  - Gradient-filled geometric elements")
    print("  - Tech grid pattern overlay")
    print("  - Gradient background box")
    print("  - Gold accent line")
    print("  - Final unsharp mask polish")
    print("\nTagline updated: 'Empowering Educators, Innovating Futures'")
    print("=" * 70)

    return output_path

if __name__ == "__main__":
    cover_path = create_next_level_cover()
    print("\nReady for validation!")
