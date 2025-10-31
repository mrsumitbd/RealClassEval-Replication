import json
from ultralytics.utils.checks import check_requirements

class ParkingPtsSelection:
    """
    A class for selecting and managing parking zone points on images using a Tkinter-based UI.

    This class provides functionality to upload an image, select points to define parking zones, and save the
    selected points to a JSON file. It uses Tkinter for the graphical user interface.

    Attributes:
        tk (module): The Tkinter module for GUI operations.
        filedialog (module): Tkinter's filedialog module for file selection operations.
        messagebox (module): Tkinter's messagebox module for displaying message boxes.
        master (tk.Tk): The main Tkinter window.
        canvas (tk.Canvas): The canvas widget for displaying the image and drawing bounding boxes.
        image (PIL.Image.Image): The uploaded image.
        canvas_image (ImageTk.PhotoImage): The image displayed on the canvas.
        rg_data (List[List[Tuple[int, int]]]): List of bounding boxes, each defined by 4 points.
        current_box (List[Tuple[int, int]]): Temporary storage for the points of the current bounding box.
        imgw (int): Original width of the uploaded image.
        imgh (int): Original height of the uploaded image.
        canvas_max_width (int): Maximum width of the canvas.
        canvas_max_height (int): Maximum height of the canvas.

    Methods:
        initialize_properties: Initializes the necessary properties.
        upload_image: Uploads an image, resizes it to fit the canvas, and displays it.
        on_canvas_click: Handles mouse clicks to add points for bounding boxes.
        draw_box: Draws a bounding box on the canvas.
        remove_last_bounding_box: Removes the last bounding box and redraws the canvas.
        redraw_canvas: Redraws the canvas with the image and all bounding boxes.
        save_to_json: Saves the bounding boxes to a JSON file.

    Examples:
        >>> parking_selector = ParkingPtsSelection()
        >>> # Use the GUI to upload an image, select parking zones, and save the data
    """

    def __init__(self):
        """Initializes the ParkingPtsSelection class, setting up UI and properties for parking zone point selection."""
        check_requirements('tkinter')
        import tkinter as tk
        from tkinter import filedialog, messagebox
        self.tk, self.filedialog, self.messagebox = (tk, filedialog, messagebox)
        self.master = self.tk.Tk()
        self.master.title('Ultralytics Parking Zones Points Selector')
        self.master.resizable(False, False)
        self.canvas = self.tk.Canvas(self.master, bg='white')
        self.canvas.pack(side=self.tk.BOTTOM)
        self.image = None
        self.canvas_image = None
        self.canvas_max_width = None
        self.canvas_max_height = None
        self.rg_data = None
        self.current_box = None
        self.imgh = None
        self.imgw = None
        button_frame = self.tk.Frame(self.master)
        button_frame.pack(side=self.tk.TOP)
        for text, cmd in [('Upload Image', self.upload_image), ('Remove Last BBox', self.remove_last_bounding_box), ('Save', self.save_to_json)]:
            self.tk.Button(button_frame, text=text, command=cmd).pack(side=self.tk.LEFT)
        self.initialize_properties()
        self.master.mainloop()

    def initialize_properties(self):
        """Initialize properties for image, canvas, bounding boxes, and dimensions."""
        self.image = self.canvas_image = None
        self.rg_data, self.current_box = ([], [])
        self.imgw = self.imgh = 0
        self.canvas_max_width, self.canvas_max_height = (1280, 720)

    def upload_image(self):
        """Uploads and displays an image on the canvas, resizing it to fit within specified dimensions."""
        from PIL import Image, ImageTk
        self.image = Image.open(self.filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg')]))
        if not self.image:
            return
        self.imgw, self.imgh = self.image.size
        aspect_ratio = self.imgw / self.imgh
        canvas_width = min(self.canvas_max_width, self.imgw) if aspect_ratio > 1 else int(self.canvas_max_height * aspect_ratio)
        canvas_height = min(self.canvas_max_height, self.imgh) if aspect_ratio <= 1 else int(canvas_width / aspect_ratio)
        self.canvas.config(width=canvas_width, height=canvas_height)
        self.canvas_image = ImageTk.PhotoImage(self.image.resize((canvas_width, canvas_height)))
        self.canvas.create_image(0, 0, anchor=self.tk.NW, image=self.canvas_image)
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        (self.rg_data.clear(), self.current_box.clear())

    def on_canvas_click(self, event):
        """Handles mouse clicks to add points for bounding boxes on the canvas."""
        self.current_box.append((event.x, event.y))
        self.canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill='red')
        if len(self.current_box) == 4:
            self.rg_data.append(self.current_box.copy())
            self.draw_box(self.current_box)
            self.current_box.clear()

    def draw_box(self, box):
        """Draws a bounding box on the canvas using the provided coordinates."""
        for i in range(4):
            self.canvas.create_line(box[i], box[(i + 1) % 4], fill='blue', width=2)

    def remove_last_bounding_box(self):
        """Removes the last bounding box from the list and redraws the canvas."""
        if not self.rg_data:
            self.messagebox.showwarning('Warning', 'No bounding boxes to remove.')
            return
        self.rg_data.pop()
        self.redraw_canvas()

    def redraw_canvas(self):
        """Redraws the canvas with the image and all bounding boxes."""
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor=self.tk.NW, image=self.canvas_image)
        for box in self.rg_data:
            self.draw_box(box)

    def save_to_json(self):
        """Saves the selected parking zone points to a JSON file with scaled coordinates."""
        scale_w, scale_h = (self.imgw / self.canvas.winfo_width(), self.imgh / self.canvas.winfo_height())
        data = [{'points': [(int(x * scale_w), int(y * scale_h)) for x, y in box]} for box in self.rg_data]
        from io import StringIO
        write_buffer = StringIO()
        json.dump(data, write_buffer, indent=4)
        with open('bounding_boxes.json', 'w', encoding='utf-8') as f:
            f.write(write_buffer.getvalue())
        self.messagebox.showinfo('Success', 'Bounding boxes saved to bounding_boxes.json')