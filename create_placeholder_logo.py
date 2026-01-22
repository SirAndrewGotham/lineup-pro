from PIL import Image, ImageDraw

# Create a simple 256x256 placeholder image
img = Image.new('RGB', (256, 256), color=(74, 144, 226))
draw = ImageDraw.Draw(img)

# Draw a simple logo
draw.rectangle([50, 50, 206, 206], outline=(255, 255, 255), width=5)
draw.text((128, 128), "LP", fill=(255, 255, 255), anchor="mm", font_size=64)

img.save('assets/images/logo.png')
print("Created placeholder logo at assets/images/logo.png")
