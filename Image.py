from PIL import Image, ImageEnhance, ImageFilter


class ImageEditor:
    def __init__(self):

        self.image = None
        self.undo_stack = []
        self.redo_stack = []

    def load_image(self, image_path):

        self.image = Image.open(image_path)

    def save_image(self, output_path):

        if self.image:
            self.image.save(output_path)

    def apply_resize(self, new_size):

        if self.image:
            self._push_to_undo_stack()
            self.image = self.image.resize(new_size)

    def apply_crop(self, crop_box):

        if self.image:
            self._push_to_undo_stack()
            self.image = self.image.crop(crop_box)

    def apply_rotate(self, angle):

        if self.image:
            self._push_to_undo_stack()
            self.image = self.image.rotate(angle)

    def apply_flip(self, flip_mode):

        if self.image:

            self._push_to_undo_stack()
            if flip_mode == 'horizontal':

                self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            elif flip_mode == 'vertical':

                self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

    def adjust_brightness(self, factor):

        if self.image:

            self._push_to_undo_stack()
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(factor)

    def adjust_contrast(self, factor):

        if self.image:

            self._push_to_undo_stack()
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(factor)

    def adjust_saturation(self, factor):

        if self.image:

            self._push_to_undo_stack()
            enhancer = ImageEnhance.Color(self.image)
            self.image = enhancer.enhance(factor)

    def apply_blur(self):

        if self.image:

            self._push_to_undo_stack()
            self.image = self.image.filter(ImageFilter.BLUR)

    def apply_sharpen(self):

        if self.image:

            self._push_to_undo_stack()
            self.image = self.image.filter(ImageFilter.SHARPEN)
    def adjust_temperature(self, adjustment):

        if self.image:

            self._push_to_undo_stack()
            r, g, b = self.image.split()
            r = self._adjust_channel(r, adjustment)
            enhanced_image = Image.merge("RGB", (r, g, b))
            self.image = enhanced_image

    def adjust_exposure(self, adjustment):

        if self.image:

            self._push_to_undo_stack()
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(1.0 + adjustment)

    def _adjust_channel(self, channel, adjustment):

        lut = [(i + int(adjustment * 255)) for i in range(256)]
        channel = channel.point(lut)
        return channel

    def apply_grayscale(self):

        if self.image:

            self._push_to_undo_stack()
            grayscale_image = self.image.convert("L")
            blurred_image = grayscale_image.filter(ImageFilter.BLUR)
            final_image = Image.blend(grayscale_image, blurred_image, alpha=0.2)
            self.image = final_image

    
    def undo(self):

        if len(self.undo_stack) > 0:
            self.redo_stack.append(self.image)
            self.image = self.undo_stack.pop()

    def apply_edge_enhance(self):

        if self.image:
            self._push_to_undo_stack()
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)

    def get_image(self):

        return self.image

    def redo(self):

        if len(self.redo_stack) > 0:
            self.undo_stack.append(self.image)
            self.image = self.redo_stack.pop()

    def _push_to_undo_stack(self):
        
        if self.image:
            self.undo_stack.append(self.image.copy())
            self.redo_stack = []
