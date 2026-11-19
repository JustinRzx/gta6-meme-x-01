from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

# Initialize image
width, height = 1080, 1080
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

# Create gradient background
def create_gradient(draw, width, height):
    for y in range(height):
        if y < height // 3:
            # Deep purple to magenta
            r = int(26 + (64 - 26) * y / (height // 3))
            g = int(5 + (10 - 5) * y / (height // 3))
            b = int(51 + (80 - 51) * y / (height // 3))
        elif y < 2 * height // 3:
            # Magenta to glow
            r = int(64 + (255 - 64) * (y - height // 3) / (height // 3))
            g = int(10 + (45 - 10) * (y - height // 3) / (height // 3))
            b = int(80 + (149 - 80) * (y - height // 3) / (height // 3))
        else:
            # Glow to magenta
            r = int(255 + (64 - 255) * (y - 2 * height // 3) / (height // 3))
            g = int(45 + (10 - 45) * (y - 2 * height // 3) / (height // 3))
            b = int(149 + (80 - 149) * (y - 2 * height // 3) / (height // 3))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

create_gradient(draw, width, height)

# Draw synthwave sun
sun_center = (540, 760)
sun_radius = 260

# Gradient gold to pink
for y in range(sun_center[1] - sun_radius, sun_center[1] + sun_radius):
    for x in range(sun_center[0] - sun_radius, sun_center[0] + sun_radius):
        if (x - sun_center[0])**2 + (y - sun_center[1])**2 <= sun_radius**2:
            distance = ((x - sun_center[0])**2 + (y - sun_center[1])**2)**0.5
            r = int(255 - (255 - 218) * distance / sun_radius)
            g = int(210 - (210 - 105) * distance / sun_radius)
            b = int(74 - (74 - 180) * distance / sun_radius)
            draw.point((x, y), fill=(r, g, b))

# Draw horizontal gap lines
for y in range(sun_center[1] - sun_radius, sun_center[1] + sun_radius, 20):
    draw.line([(sun_center[0] - sun_radius, y), (sun_center[0] + sun_radius, y)], fill=(0, 0, 0), width=2)

# Draw black skyline silhouette
random.seed(42)
for x in range(0, width, 100):
    rect_height = random.randint(120, 320)
    draw.rectangle([(x, height - rect_height), (x + 50, height)], fill=(0, 0, 0))

# Draw palm silhouettes
palm_positions = [(200, 800), (400, 820), (800, 810)]
for x, y in palm_positions:
    # Trunk
    draw.polygon([(x, y), (x + 20, y - 100), (x + 40, y)], fill=(0, 0, 0))
    # Fronds
    for i in range(3):
        draw.arc([(x - 30 + i * 20, y - 120), (x + 70 + i * 20, y - 20)], start=0, end=180, fill=(0, 0, 0), width=2)

# Load ghost image
ghost_image = Image.open("/root/makefun-work/gta6-meme/press/mark-1024.png").convert("RGBA")

# Remove magenta disc
for y in range(ghost_image.height):
    for x in range(ghost_image.width):
        r, g, b, a = ghost_image.getpixel((x, y))
        if r > 150 and b > 100 and g < 100:
            ghost_image.putpixel((x, y), (r, g, b, 0))

# Remove anti-aliased magenta fringe
for y in range(ghost_image.height):
    for x in range(ghost_image.width):
        r, g, b, a = ghost_image.getpixel((x, y))
        if r > 120 and b > 90 and g < 110 and r > g + 40:
            ghost_image.putpixel((x, y), (r, g, b, 0))

# Trim to content bbox
bbox = ghost_image.getbbox()
if bbox:
    ghost_image = ghost_image.crop(bbox)

# Resize ghost
ghost_height = 340
ghost_width = int(ghost_image.width * ghost_height / ghost_image.height)
ghost_image = ghost_image.resize((ghost_width, 300))

# Paste ghost
image.paste(ghost_image, (740, 380), ghost_image)

# Draw shadow under ghost
shadow = Image.new("RGBA", (ghost_width, ghost_height), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow)
shadow_draw.ellipse([(0, 0), (ghost_width, ghost_height)], fill=(0, 0, 0, 100))
shadow = shadow.filter(ImageFilter.GaussianBlur(10))
image.paste(shadow, (700, 730), shadow)

# Draw gold banner
banner_rect = [(700, 700), (1050, 760)]
draw.rectangle(banner_rect, fill=(255, 210, 74))

# Add text to banner
banner_text = "waited 13 years too"
font = ImageFont.truetype("DejaVuSans-Bold", 30)
text_width = draw.textlength(banner_text, font=font)
text_x = (banner_rect[1][0] - banner_rect[0][0] - text_width) // 2 + banner_rect[0][0]
text_y = (banner_rect[1][1] - banner_rect[0][1] - font.size) // 2 + banner_rect[0][1]
draw.text((text_x, text_y), banner_text, fill=(0, 0, 0), font=font)

# Draw headline
headline_text = "MISSION PASSED!"
font = ImageFont.truetype("LiberationSansNarrow-Bold", 100)
text_width = draw.textlength(headline_text, font=font)
text_x = (width - text_width) // 2
text_y = 120

# Draw outline
for dx in [-1, 0, 1]:
    for dy in [-1, 0, 1]:
        if dx != 0 or dy != 0:
            draw.text((text_x + dx, text_y + dy), headline_text, fill=(0, 0, 0), font=font)

draw.text((text_x, text_y), headline_text, fill=(255, 210, 74), font=font)

# Draw subline
subline_text = "GTA 6 · LAUNCH WEEK"
font = ImageFont.truetype("DejaVuSans", 40)
text_width = draw.textlength(subline_text, font=font)
text_x = (width - text_width) // 2
text_y = 210
draw.text((text_x, text_y), subline_text, fill=(255, 255, 255), font=font)

# Draw stats panel
draw.rounded_rectangle([(50, 310), (650, 590)], radius=18, fill=(15, 5, 30), outline=(255, 210, 74), width=3)

# Draw stats block
stats_texts = [
    "WAITED: 13 YEARS",
    "SICK DAYS: ALL OF THEM",
    "DOWNLOAD: 150 GB",
    "RESPECT: MAX",
]
font = ImageFont.truetype("DejaVuSans-Bold", 40)
text_x = 70
text_y = 330
for text in stats_texts:
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    text_y += 70

# Draw pitch bar
pitch_bar_rect = [(0, 840), (width, 1020)]
draw.rectangle(pitch_bar_rect, fill=(10, 5, 20))

# Draw pitch lines
pitch_lines = [
    "while you waited, agents on make.fun",
    "were earning real money",
]
font = ImageFont.truetype("DejaVuSans-Bold", 40)
for i, line in enumerate(pitch_lines):
    text_width = draw.textlength(line, font=font)
    text_x = (width - text_width) // 2
    text_y = 858 + i * 48
    draw.text((text_x, text_y), line, fill=(255, 255, 255), font=font)

# Draw wordmark
wordmark_text = "make.fun"
font = ImageFont.truetype("DejaVuSans-Bold", 50)
text_width = draw.textlength(wordmark_text, font=font)
text_x = (width - text_width) // 2
text_y = 952
draw.text((text_x, text_y), wordmark_text, fill=(255, 255, 255), font=font)

# Draw dot
dot_x = text_x + text_width - 10
dot_y = text_y + font.size // 2
draw.ellipse([(dot_x, dot_y), (dot_x + 10, dot_y + 10)], fill=(255, 45, 149))

# Compute bounding boxes
headline_bbox = (text_x, 120, text_x + text_width, 120 + 100)
subline_bbox = (text_x, 210, text_x + text_width, 210 + 40)
stats_bbox = (70, 330, 70 + max(draw.textlength(text, font=ImageFont.truetype("DejaVuSans-Bold", 40)) for text in stats_texts), 330 + len(stats_texts) * 62)
ghost_bbox = (740, 380, 740 + ghost_width, 380 + 300)

# Assert no overlaps
assert not (headline_bbox[0] < stats_bbox[2] and headline_bbox[2] > stats_bbox[0] and headline_bbox[1] < stats_bbox[3] and headline_bbox[3] > stats_bbox[1]), "Headline and stats overlap"
assert not (ghost_bbox[0] < stats_bbox[2] and ghost_bbox[2] > stats_bbox[0] and ghost_bbox[1] < stats_bbox[3] and ghost_bbox[3] > stats_bbox[1]), "Ghost and stats overlap"

# Save image
image.save("meme.png")

# Create thumbnail
thumb = image.resize((480, 480))
thumb.save("thumb.png")

# Verify render
image = Image.open("meme.png")
headline_crop = image.crop((headline_bbox[0], headline_bbox[1], headline_bbox[2], headline_bbox[3]))
stats_crop = image.crop((stats_bbox[0], stats_bbox[1], stats_bbox[2], stats_bbox[3]))
headline_crop.save("headline_crop.png")
stats_crop.save("stats_crop.png")

print("Bounding boxes:")
print(f"Headline: {headline_bbox}")
print(f"Subline: {subline_bbox}")
print(f"Stats: {stats_bbox}")
print(f"Ghost: {ghost_bbox}")
