import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import messagebox
from PIL import ImageTk, Image, ImageFilter, ImageEnhance
from Image import ImageEditor
from tkinter.ttk import Combobox
from tkinter import ttk
from ttkthemes import ThemedStyle




class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Editor")
        
        

        self.image_editor = ImageEditor()

        self.style = ThemedStyle(self.root)

        #setting theme for  gui

        self.style.set_theme("aqua")  

        #menu bar
        self.menu_bar = MenuBar(self, self.image_editor) 
        #toolbar

        self.toolbar = ToolBar(self, self.image_editor, width=150)  

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.open_button = tk.Button(self.top_frame, text="Open", command=self.open_image)
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.top_frame, text="Save", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(self.top_frame, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.redo_button = tk.Button(self.top_frame, text="Redo", command=self.redo)
        self.redo_button.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.root.config(menu=self.menu_bar.menu_bar)
        self.root.mainloop()

    def open_image(self):

        file_path = filedialog.askopenfilename()

        if file_path:

            try:
                self.image_editor.load_image(file_path)
                self.display_image()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_image(self):

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("GIF", "*.gif")]
        )
        if file_path:
            try:
                self.image_editor.save_image(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def undo(self):

        try:
            self.image_editor.undo()
            self.display_image()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def redo(self):

        try:
            self.image_editor.redo()
            self.display_image()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_image(self):

        image = self.image_editor.get_image()
        if image:
            
            self.canvas.delete("all")
            image_width, image_height = image.size
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            scale = min(canvas_width / image_width, canvas_height / image_height)
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=tk_image)
            self.canvas.image = tk_image


class MenuBar:
    def __init__(self, gui, image_editor):
        self.gui = gui
        self.image_editor = image_editor
        

        self.menu_bar = tk.Menu(self.gui.root)
        
        self.create_menus()

    def create_menus(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.gui.open_image)
        file_menu.add_command(label="Save", command=self.gui.save_image)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.gui.undo)
        edit_menu.add_command(label="Redo", command=self.gui.redo)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)


class ToolBar:
    def __init__(self, gui, image_editor, width=150):
        self.gui = gui
        self.image_editor = image_editor
        

        self.toolbar = tk.Frame(self.gui.root, width=width)
        self.create_toolbar()

        self.toolbar.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

    def create_toolbar(self):
        brightness_label = tk.Label(self.toolbar, text="Brightness")
        brightness_label.pack()

        brightness_slider = ttk.Scale(self.toolbar, from_=-10, to=10, orient=tk.HORIZONTAL, length=120, command=self.adjust_brightness)
        brightness_slider.set(0)  # Set initial value in the middle
        brightness_slider.pack()

        contrast_label = tk.Label(self.toolbar, text="Contrast")
        contrast_label.pack()

        contrast_slider = ttk.Scale(self.toolbar, from_=-10, to=10, orient=tk.HORIZONTAL, length=120, command=self.adjust_contrast)
        contrast_slider.set(0)  # Set initial value in the middle
        contrast_slider.pack()

        saturation_label = tk.Label(self.toolbar, text="Saturation")
        saturation_label.pack()

        saturation_slider = ttk.Scale(self.toolbar, from_=-10, to=10, orient=tk.HORIZONTAL, length=120, command=self.adjust_saturation)
        saturation_slider.set(0)  # Set initial value in the middle
        saturation_slider.pack()

        temperature_label = tk.Label(self.toolbar, text="Temperature")
        temperature_label.pack()

        temperature_slider = ttk.Scale(self.toolbar, from_=-10, to=10, orient=tk.HORIZONTAL, length=120, command=self.adjust_temperature)
        temperature_slider.set(0)  # Set initial value in the middle
        temperature_slider.pack()

        exposure_label = tk.Label(self.toolbar, text="Exposure")
        exposure_label.pack()

        exposure_slider = ttk.Scale(self.toolbar, from_=-10, to=10, orient=tk.HORIZONTAL, length=120, command=self.adjust_exposure)
        exposure_slider.set(0)  # Set initial value in the middle
        exposure_slider.pack()

        resize_label = tk.Label(self.toolbar, text="Resize")
        resize_label.pack()

        width_label = tk.Label(self.toolbar, text="Width:")
        width_label.pack()
        width_entry = tk.Entry(self.toolbar)
        width_entry.pack()

        height_label = tk.Label(self.toolbar, text="Height:")
        height_label.pack()
        height_entry = tk.Entry(self.toolbar)
        height_entry.pack()

        resize_button = tk.Button(self.toolbar, text="Apply", command=lambda: self.apply_resize(width_entry.get(), height_entry.get()))
        resize_button.pack(pady=5)

        flip_label = tk.Label(self.toolbar, text="Flip")
        flip_label.pack()

        flip_option = ttk.Combobox(self.toolbar, values=["None", "Horizontal", "Vertical"])
        flip_option.pack()

        flip_button = tk.Button(self.toolbar, text="Apply", command=lambda: self.apply_flip(flip_option.get()))
        flip_button.pack(pady=5)

        filter_label = tk.Label(self.toolbar, text="Filter")
        filter_label.pack()

        filter_option = Combobox(self.toolbar, values=["Blur", "Sharpen", "Edge Enhance","GrayScale"])
        filter_option.pack()

        filter_button = tk.Button(self.toolbar, text="Apply", command=lambda: self.apply_filter(filter_option.get()))
        filter_button.pack(pady=5)

    def adjust_brightness(self, value):
        try:
            value = float(value)
            pivot = 0.0  # Midpoint of the scale
            adjustment = (value - pivot) / 10.0  # Scale adjustment relative to the pivot
            self.image_editor.adjust_brightness(1.0 + adjustment)
            self.gui.display_image()
        except ValueError:
            pass

    def adjust_contrast(self, value):
        try:
            value = float(value)
            pivot = 0.0  # Midpoint of the scale
            adjustment = (value - pivot) / 10.0  # Scale adjustment relative to the pivot
            self.image_editor.adjust_contrast(1.0 + adjustment)
            self.gui.display_image()
        except ValueError:
            pass

    def adjust_saturation(self, value):
        try:
            value = float(value)
            pivot = 0.0  # Midpoint of the scale
            adjustment = (value - pivot) / 10.0  # Scale adjustment relative to the pivot
            self.image_editor.adjust_saturation(1.0 + adjustment)
            self.gui.display_image()
        except ValueError:
            pass

    def apply_resize(self, width, height):
        try:
            width = int(width)
            height = int(height)
            self.image_editor.apply_resize((width, height))
            self.gui.display_image()
        except ValueError:
            pass
    
    def apply_flip(self, flip_mode):
        if flip_mode == "Horizontal":
            self.image_editor.apply_flip("horizontal")
        elif flip_mode == "Vertical":
            self.image_editor.apply_flip("vertical")

        self.gui.display_image()

    def apply_filter(self, filter_name):
        if filter_name == "Blur":
            self.image_editor.apply_blur()
        elif filter_name == "Sharpen":
            self.image_editor.apply_sharpen()
        elif filter_name == "Edge Enhance":
            self.image_editor.apply_edge_enhance()
        elif filter_name == "GrayScale":
            self.image_editor.apply_grayscale()  
        

        self.gui.display_image()
    def adjust_temperature(self, value):
        try:
            value = float(value)
            pivot = 0.0  # Midpoint of the scale
            adjustment = (value - pivot) / 10.0  # Scale adjustment relative to the pivot
            self.image_editor.adjust_temperature(adjustment)
            self.gui.display_image()
        except ValueError:
            pass

    def adjust_exposure(self, value):
        try:
            value = float(value)
            pivot = 0.0  # Midpoint of the scale
            adjustment = (value - pivot) / 10.0  # Scale adjustment relative to the pivot
            self.image_editor.adjust_exposure(adjustment)
            self.gui.display_image()
        except ValueError:
            pass


gui = GUI()
