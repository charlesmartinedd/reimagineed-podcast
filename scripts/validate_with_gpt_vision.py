"""
Validate branding guide pages using GPT-5 Vision against Madison Avenue quality rubric
"""
import os
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent.parent / '.env', override=True)

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

def validate_image_with_vision(image_path, page_name, assessment_context=""):
    """
    Validate image using GPT-5 Vision against Madison Avenue rubric

    Args:
        image_path: Path to image file
        page_name: Name of the page being assessed
        assessment_context: Additional context for assessment (e.g., "cover hero image")

    Returns:
        dict with score, assessment, and pass/fail status
    """

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://alexandriasdesign.com",
        "X-Title": "ReimagineED Brand Guide Validator"
    }

    # Read and encode image
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # Assessment prompt based on rubric
    prompt = f"""You are a Madison Avenue creative director evaluating a branding guide {'component' if assessment_context else 'page'} for professional quality.

PAGE/COMPONENT: {page_name}
{f'CONTEXT: {assessment_context}' if assessment_context else ''}

Assess this image against 10 criteria (10 points each = 100 total):

1. **Visual Impact & Professional Polish** (10 points)
   - Is this striking and memorable? Professional execution?

2. **Brand Consistency & Cohesion** (10 points)
   - Does it align with tech-forward, disruptor brand archetype?

3. **Strategic Clarity & Purpose** (10 points)
   - Does every element serve the brand story of ReimagineED?

4. **Cultural Authenticity & Representation** (10 points)
   - Genuine, respectful representation of Black and Latino educators?

5. **Typography & Readability** (10 points)
   - Masterful type hierarchy? Sophisticated font pairings?

6. **Color Psychology & Application** (10 points)
   - Sophisticated use of navy blue (#0B1D3A) and gold (#FFD33A)?

7. **Imagery & Visual Storytelling** (10 points)
   - Compelling, authentic imagery that tells the brand story?

8. **Content Quality & Messaging** (10 points)
   - Powerful, clear messaging? Exceptional copywriting?

9. **Innovation & Differentiation** (10 points)
   - Boldly original? Stands apart from competition?

10. **Production Quality & Technical Excellence** (10 points)
    - Flawless technical execution? Print/digital-ready?

REFERENCE STANDARDS:
- Airbnb's brand guide (custom Cereal typeface, Rausch red, mission-driven)
- Spotify's brand guide (duotone treatment, bold gradients, Circular typeface)
- Luxury brands (Cartier, Tiffany, Porsche): elegant fonts, minimalist sophistication

For each criterion, provide:
- **Score (0-10)**
- **Evidence**: Specific observations from the image
- **Recommendations**: Concrete improvements (if score < 10)

FORMAT YOUR RESPONSE AS:

CRITERION 1: Visual Impact & Professional Polish
Score: [X/10]
Evidence: [What you observe]
Recommendations: [What would improve it]

[Continue for all 10 criteria]

SUMMARY:
Total Score: [X/100]
Pass/Fail: [PASS if ≥90, REVISE if <90]

Key Strengths:
- [Strength 1]
- [Strength 2]
- [Strength 3]

Critical Improvements Needed:
- [If any scoring < 9]

Be ruthlessly honest. Hold to Madison Avenue professional standards. This must be stunning, elegant, and perfect."""

    payload = {
        "model": "openai/gpt-4o",  # GPT-5 Vision via OpenRouter
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2000
    }

    print(f"\nValidating {page_name} with GPT-5 Vision...")
    print(f"Image: {image_path}")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        assessment = result['choices'][0]['message']['content']

        # Parse score from assessment
        score_line = [line for line in assessment.split('\n') if 'Total Score:' in line]
        if score_line:
            score_text = score_line[0].split(':')[1].strip()
            score = int(score_text.split('/')[0])
        else:
            score = None

        # Determine pass/fail
        status = "PASS" if score and score >= 90 else "REVISE"

        print(f"\nScore: {score}/100")
        print(f"Status: {status}")

        return {
            'score': score,
            'status': status,
            'assessment': assessment,
            'image_path': str(image_path)
        }

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Test with cover hero image
    image_path = Path(__file__).parent.parent / "assets" / "branding-guide" / "cover_hero_image_1.png"

    if image_path.exists():
        result = validate_image_with_vision(
            image_path,
            "Cover Hero Image",
            "AI-generated imagery for ReimagineED brand guide cover page"
        )

        if result:
            print("\n" + "=" * 80)
            print("FULL ASSESSMENT:")
            print("=" * 80)
            print(result['assessment'])
            print("=" * 80)

            # Save assessment
            output_dir = Path(__file__).parent.parent / "docs" / "assessments"
            output_dir.mkdir(exist_ok=True)

            assessment_file = output_dir / "cover_hero_image_assessment.txt"
            with open(assessment_file, 'w', encoding='utf-8') as f:
                f.write(f"IMAGE: {result['image_path']}\n")
                f.write(f"SCORE: {result['score']}/100\n")
                f.write(f"STATUS: {result['status']}\n\n")
                f.write(result['assessment'])

            print(f"\nAssessment saved to: {assessment_file}")
    else:
        print(f"Image not found: {image_path}")
