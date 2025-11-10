"""
Validate complete cover page with GPT-5 Vision
"""
from pathlib import Path
from validate_with_gpt_vision import validate_image_with_vision

if __name__ == "__main__":
    print("=" * 80)
    print("VALIDATING COMPLETE COVER PAGE")
    print("=" * 80)

    cover_page_path = Path(__file__).parent.parent / "assets" / "branding-guide" / "cover_page_final.png"

    if cover_page_path.exists():
        result = validate_image_with_vision(
            cover_page_path,
            "Cover Page (Complete Design)",
            "Full cover page with logo, tagline, mission statement, brand pillars, and tech elements layered on hero image"
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

            assessment_file = output_dir / "cover_page_final_assessment.txt"
            with open(assessment_file, 'w', encoding='utf-8') as f:
                f.write(f"IMAGE: {result['image_path']}\n")
                f.write(f"SCORE: {result['score']}/100\n")
                f.write(f"STATUS: {result['status']}\n\n")
                f.write(result['assessment'])

            print(f"\nAssessment saved to: {assessment_file}")

            # Decision
            if result['status'] == 'PASS':
                print("\n" + "=" * 80)
                print("PASS! Cover page meets Madison Avenue standards (>=90%).")
                print("Ready to proceed to page 2.")
                print("=" * 80)
            else:
                print("\n" + "=" * 80)
                print("REVISE NEEDED. Score below 90%.")
                print("Will iterate based on feedback.")
                print("=" * 80)
    else:
        print(f"Cover page not found: {cover_page_path}")
