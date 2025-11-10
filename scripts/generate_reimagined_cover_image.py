"""
Generate ReimagineED Cover Hero Image using Nano Banana (Gemini 2.5 Flash Image)
"""
import os
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent.parent / '.env', override=True)

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

def generate_reimagined_cover_image():
    """Generate hero image for ReimagineED branding guide cover"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://alexandriasdesign.com",
        "X-Title": "ReimagineED Branding Guide"
    }

    # Hero image prompt for cover page
    prompt = """Create a stunning, professional hero image for a cutting-edge AI education podcast brand called 'ReimagineED'.

COMPOSITION:
- Dynamic, cinematic shot of a confident Black female educator in her 30s engaging with holographic AI interface
- She's gesturing confidently toward floating digital elements (neural networks, educational icons, data visualizations)
- Modern classroom/tech space in background with other diverse educators collaborating
- Dramatic lighting with neon blue (#00D9FF) and gold (#FFD33A) accents creating tech-forward atmosphere

STYLE:
- Photorealistic with slight futuristic enhancement
- Tech-forward aesthetic: sleek, dynamic, cutting-edge
- Lighting: Dramatic side lighting with colored gels (blue, purple, gold)
- Depth of field: Sharp subject, slightly blurred background to create dimension
- Color grading: Rich navy blues, vibrant golds, electric accents

MOOD:
- Empowered, innovative, forward-thinking
- Professional but disruptive
- Authentic human emotion mixed with technological sophistication
- Confidence and authority

TECHNICAL:
- 8K quality, ultra-sharp detail
- Cinematic composition with rule of thirds
- Professional color grading
- Suitable for large-format printing and digital use"""

    payload = {
        "model": "google/gemini-2.5-flash-image",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "modalities": ["image", "text"]  # CRITICAL for image generation
    }

    print("Generating ReimagineED cover hero image...")
    print(f"Using model: google/gemini-2.5-flash-image")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()

        # Extract images from nested structure
        images = result['choices'][0]['message'].get('images', [])

        if not images:
            print("No images generated")
            return None

        # Create output directory
        output_dir = Path(__file__).parent.parent / "assets" / "branding-guide"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save each generated image
        saved_files = []
        for i, img_data in enumerate(images):
            # Handle nested dictionary structure
            if isinstance(img_data, dict):
                if 'image_url' in img_data:
                    img_url = img_data['image_url'].get('url', '')
                else:
                    img_url = img_data.get('url', '')

                if img_url and img_url.startswith('data:image'):
                    # Extract base64 data
                    base64_data = img_url.split(',')[1]

                    # Decode and save
                    img_bytes = base64.b64decode(base64_data)

                    output_path = output_dir / f"cover_hero_image_{i+1}.png"

                    with open(output_path, 'wb') as f:
                        f.write(img_bytes)

                    saved_files.append(output_path)
                    print(f"Saved: {output_path} ({len(img_bytes):,} bytes)")

        # Print usage stats
        usage = result.get('usage', {})
        print(f"\nToken Usage:")
        print(f"   Total: {usage.get('total_tokens', 0):,}")
        print(f"   Prompt: {usage.get('prompt_tokens', 0):,}")
        print(f"   Completion: {usage.get('completion_tokens', 0):,}")

        return saved_files

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("ReimagineED Cover Image Generator")
    print("=" * 60)

    files = generate_reimagined_cover_image()

    if files:
        print(f"\nSuccessfully generated {len(files)} image(s)!")
        print("\nOutput files:")
        for f in files:
            print(f"   {f}")
    else:
        print("\nImage generation failed")
