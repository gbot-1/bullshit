from PIL import Image, ImageOps
import random
import os

def load_images_from_folder(folder):
    images = {}
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            img = Image.open(os.path.join(folder, filename)).convert("RGBA")
            if img is not None:
                images[filename] = img
    return images

def load_instructions_and_create_pool(file_path, images):
    pool = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 3:
                filename, count, max_size = parts
                if filename in images:
                    for _ in range(int(count)):
                        pool.append((filename, float(max_size)))
    return pool

def check_overlap(new_rect, existing_rects, tolerance):
    new_x, new_y, new_w, new_h = new_rect
    new_area = new_w * new_h
    for rect in existing_rects:
        ex_x, ex_y, ex_w, ex_h = rect

        # Calculate overlap
        overlap_x = max(0, min(new_x + new_w, ex_x + ex_w) - max(new_x, ex_x))
        overlap_y = max(0, min(new_y + new_h, ex_y + ex_h) - max(new_y, ex_y))
        overlap_area = overlap_x * overlap_y

        if overlap_area / new_area > tolerance:
            return True  # Overlap exceeds tolerance
    return False  # No significant overlap

# Your images folder path and instructions file path
images_folder_path = 'C:/Users/Guillaume/Documents/Codes/bullshit'
instructions_file_path = 'instruction.txt'

# Load images and instructions
images = load_images_from_folder(images_folder_path)
image_pool = load_instructions_and_create_pool(instructions_file_path, images)

# instructions = load_instructions(instructions_file_path)

# Screen dimensions (for example, 1920x1080)
screen_width = 1920*3
screen_height = 1080*3

# Create a new blank image with screen dimensions
canvas = Image.new('RGBA', (screen_width, screen_height), (255, 255, 255))

placed_rects = [] 

random.shuffle(image_pool)   # List to keep track of placed image rectangles

# for filename, details in instructions.items():
#     image = random.choice(images.get(filename))
#     if image:
#         for _ in range(details['count']):
#             for attempt in range(20):  # Try to place the image up to 100 times to avoid infinite loop
#                 # Scale the image according to max_size parameter
#                 scale_factor = random.uniform(0.01, details['max_size'])
#                 new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
#                 resized_image = image.resize(new_size)
                
#                 # Randomly rotate, flip, and position the image
#                 rotated_image = resized_image.rotate(random.randint(0, 360), expand=True)
#                 if random.choice([True, False]):
#                     rotated_image = ImageOps.mirror(rotated_image)
#                 if random.choice([True, False]):
#                     rotated_image = ImageOps.flip(rotated_image)
#                 position_x = random.randint(-rotated_image.width // 2, screen_width - rotated_image.width // 2)
#                 position_y = random.randint(-rotated_image.height // 2, screen_height - rotated_image.height // 2)

#                 # Check for overlap with a tolerance of up to 90%
#                 new_rect = (position_x, position_y, rotated_image.width, rotated_image.height)
#                 if not check_overlap(new_rect, placed_rects, tolerance=0.9):
#                     canvas.paste(rotated_image, (position_x, position_y), rotated_image)
#                     placed_rects.append(new_rect)
#                     break

while image_pool:
    filename, max_size = image_pool.pop()
    image = images[filename]
    
    for attempt in range(20):  # Try to place the image up to 100 times to avoid infinite loop
        # Scale the image according to max_size parameter
        scale_factor = random.uniform(0.05, max_size)
        new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        resized_image = image.resize(new_size)
        
        # Randomly rotate, flip, and position the image
        rotated_image = resized_image.rotate(random.randint(0, 360), expand=True)
        if random.choice([True, False]):
            rotated_image = ImageOps.mirror(rotated_image)
        if random.choice([True, False]):
            rotated_image = ImageOps.flip(rotated_image)
        position_x = random.randint(-rotated_image.width // 2, screen_width - rotated_image.width // 2)
        position_y = random.randint(-rotated_image.height // 2, screen_height - rotated_image.height // 2)

        # Check for overlap with a tolerance of up to 90%
        new_rect = (position_x, position_y, rotated_image.width, rotated_image.height)
        if not check_overlap(new_rect, placed_rects, 0.75):
            canvas.paste(rotated_image, (position_x, position_y), rotated_image)
            placed_rects.append(new_rect)
            break

# Convert the final canvas to remove the alpha channel for saving in formats like JPEG
final_image = Image.new("RGB", canvas.size, (255, 255, 255))
final_image.paste(canvas, mask=canvas.split()[3])  # 3 is the alpha channel of an RGBA image

# Save or show the final image
final_image.save('personalized_wheres_waldo_random_selection.png')

# Save or show the final image
# canvas.save('demise_no_overlap.png')
