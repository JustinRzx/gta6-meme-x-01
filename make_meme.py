
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Load the ghost image
ghost_image = Image.open("/root/makefun-work/gta6-meme/press/mark-1024.png").convert("RGBA")

# Create a new image with a white background
width, height = 1080, 1080
image = Image.new("RGBA", (width, height), (255, 255, 255))

# Draw the GTA-style mission passed screen
draw = ImageDraw.Draw(image)

# Draw the mission passed text
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_size = 60
font = ImageFont.truetype(font_path, font_size)
draw.text((width // 2, height // 2 - 100), "MISSION PASSED: GTA 6", fill=(0, 0, 0), font=font, anchor="mm")

# Draw the 13-year wait text
font_size = 40
font = ImageFont.truetype(font_path, font_size)
draw.text((width // 2, height // 2), "make.fun ghost waited 13 years too", fill=(0, 0, 0), font=font, anchor="mm")

# Draw the make.fun text
font_size = 30
font = ImageFont.truetype(font_path, font_size)
draw.text((width // 2, height // 2 + 100), "make.fun: where people and AI agents earn real money", fill=(0, 0, 0), font=font, anchor="mm")

# Resize the ghost image
ghost_size = (200, 200)
ghost_image = ghost_image.resize(ghost_size, Image.LANCZOS)

# Paste the ghost image onto the main image
image.paste(ghost_image, (width // 2 - ghost_size[0] // 2, height // 2 - ghost_size[1] // 2 - 50), ghost_image)

# Save the image
image.save("meme.png")

# Create a thumbnail for verification
thumb_size = (480, 480)
thumb = image.resize(thumb_size, Image.LANCZOS)
thumb.save("thumb.png")
