"""
Generate simple colored placeholder images using pure Python
"""
import os

def create_simple_placeholder(output_path, color=(200, 200, 200), width=400, height=300):
    """Create a simple colored placeholder image"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create a simple PPM image (no external dependencies needed)
    with open(output_path, 'w') as f:
        # PPM header
        f.write(f"P3\n{width} {height}\n255\n")

        # Fill with solid color
        for _ in range(height):
            row = []
            for _ in range(width):
                row.extend([str(color[0]), str(color[1]), str(color[2])])
            f.write(" ".join(row) + "\n")

    print(f"Created: {output_path} (PPM format)")

def generate_all_simple_assets():
    """Generate all simple placeholder images"""
    assets = [
        ("assets/images/dishes/big_hit.ppm", (200, 150, 100)),      # Brown
        ("assets/images/dishes/quarter_pounder.ppm", (180, 120, 80)), # Darker brown
        ("assets/images/dishes/chicken_sandwich.ppm", (220, 180, 140)), # Light brown
        ("assets/images/dishes/french_fries.ppm", (255, 200, 0)),    # Yellow
        ("assets/images/dishes/apple_pie.ppm", (200, 100, 50)),      # Orange-brown
    ]

    for output_path, color in assets:
        create_simple_placeholder(output_path, color)

    print("\nAll placeholder images generated in PPM format!")
    print("Note: Kivy supports PPM format. You can replace with PNG later.")

if __name__ == '__main__':
    generate_all_simple_assets()