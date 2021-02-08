import numpy as np
import pandas as pd
import cv2

# Config
main_window_id = "Color Recognition App"

# Files
image_path = "colours.jpg"
colours_csv_path = "colours.csv"

# Text styles
text_position = (50, 50)
text_scale = 0.5
text_thickness = 1
text_family = cv2.FONT_HERSHEY_COMPLEX
text_colours = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
}

csv_columns = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv(colours_csv_path, names=csv_columns, header=None)

def recognize_color(r, g, b):
    def get_row_rgb_values(csv, i):
      return (csv.loc[i, "R"], csv.loc[i, "G"], csv.loc[i, "B"])

    def get_diff(actual_colour, row_colour_string):
        return abs(actual_colour - int(row_colour_string))

    current_lowest_diff = 10000
    colour_name = "Unknown!"

    for i in range(len(csv)):
        row_r, row_g, row_b = get_row_rgb_values(csv, i)

        # Get diffs from image colour to row colour
        r_diff = get_diff(r, row_r)
        g_diff = get_diff(g, row_g)
        b_diff = get_diff(b, row_b)

        row_total_diff = r_diff + g_diff + b_diff
    
        # If this is the lowest row we've seen, use this as the current target row
        if (row_total_diff <= current_lowest_diff):
            current_lowest_diff = row_total_diff
            colour_name = csv.loc[i, "color_name"]

    return colour_name


# This function creates a function which handles the event
# This is so the handler has a reference to img
def get_mouse_click_handler(img):
    def handle_mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            b, g, r = img[y, x]
            display_colour(img, int(r), int(g), int(b))

    # Return the handler
    return handle_mouse_click

def display_colour(img, r, g, b):
    def add_text(img, text, colour):
      cv2.putText(img, text, text_position, text_family, text_scale, colour, text_thickness, cv2.LINE_AA)

    # Background rectangle
    cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

    # Text to display - classification + rgb
    text = f"Classification: {recognize_color(r,g,b)}, R={r} G={g} B={b}"

    def is_bright_colour(r, g, b):
      return r + g + b >= 400

    text_colour = "white"

    if is_bright_colour(r, g, b):
      text_colour = "black"

    add_text(img, text, text_colours[text_colour])

# Draw loop and event handling
def run_gui_loop(img):
    while (1):
        # Show the image - this acts like a render/draw function
        cv2.imshow(main_window_id, img)

        # Break the loop when user hits "esc" key
        if cv2.waitKey(20) & 0xFF == 27:
            break

def main(): 
    cv2.namedWindow(main_window_id)
    img = cv2.imread(image_path)

    # Create and setup event handler
    handle_mouse_click = get_mouse_click_handler(img)
    cv2.setMouseCallback(main_window_id, handle_mouse_click)

    # Run gui loop
    run_gui_loop(img)

    # Quit once gui loop finishes
    cv2.destroyAllWindows()

main()