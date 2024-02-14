from PIL import Image, ImageOps
import random

# Load the original image
original_image1 = Image.open('simon.png')
original_image2 = Image.open('guigui.png')
original_image3 = Image.open('massaux.png')

# Screen dimensions (for example, 1920x1080)
screen_width = 3840
screen_height = 2160

# Create a new blank image with screen dimensions
canvas = Image.new('RGB', (screen_width, screen_height), (255, 255, 255))

# Maximum allowed overlap percentage
max_overlap = 0.75

# List to store image positions and sizes for overlap checking
# placed_images = []

# def check_overlap(new_image_rect, existing_images):
#     new_x, new_y, new_w, new_h = new_image_rect
#     for ex in existing_images:
#         ex_x, ex_y, ex_w, ex_h = ex

#         # Calculate overlap
#         overlap_x = max(0, min(new_x+new_w, ex_x+ex_w) - max(new_x, ex_x))
#         overlap_y = max(0, min(new_y+new_h, ex_y+ex_h) - max(new_y, ex_y))
#         overlap_area = overlap_x * overlap_y

#         # Calculate the maximum allowed overlap area
#         new_area = new_w * new_h
#         if overlap_area / new_area > max_overlap:
#             return False
#     return True

# Decide how many times you want to paste the original image
number_of_instances = 350


for _ in range(number_of_instances):
    # Randomly scale the original image (50% to 150% of the original size)
    original_image = random.choice([original_image1, original_image2, original_image3])

    scale_factor = random.uniform(0.01, 0.65)
    new_size = (int(original_image.width * scale_factor), int(original_image.height * scale_factor))
    resized_image = original_image.resize(new_size)

    # Randomly rotate the image (0 to 360 degrees)
    rotated_image = resized_image.rotate(random.randint(0, 360), expand=True)

    # Randomly flip the image horizontally or vertically
    if random.choice([True, False]):
        rotated_image = ImageOps.mirror(rotated_image)
    if random.choice([True, False]):
        rotated_image = ImageOps.flip(rotated_image)

    # Allow images to be partially out of bounds by adjusting the position range
    position_x = random.randint(-rotated_image.width // 2, screen_width - rotated_image.width // 2)
    position_y = random.randint(-rotated_image.height // 2, screen_height - rotated_image.height // 2)

    # Paste the randomly manipulated image onto the canvas
    canvas.paste(rotated_image, (position_x, position_y), rotated_image)

# Save or show the final image
canvas.save('filled_screen.png')
# or display it in a Jupyter notebook
# display(canvas)
