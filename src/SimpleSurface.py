"""
Extend the functionality of cairo.ImageSurface to allow for easier and
cleaner vector drawing, text writing, and image manipulation.
"""
import cairo
import numpy

from PIL import Image

from .DrawSurface import DrawSurface
from .TextSurface import TextSurface


class SimpleSurface:
    """Extend the functionality of the cairo.ImageSurface class."""

    def __init__(self, width, height, image_format=cairo.FORMAT_ARGB32):
        """
        Initialize the SimpleSurface object.

        Keyword arguments:
                width (int) -- the width of the image, in pixels.
                height (int) -- the height of the image, in pixels.
                format (cairo.Format) -- the format of the image
                        (default cairo.FORMAT_ARGB32).

        Attributes:
                surface (ImageSurface) -- the Surface where everything is drawn.
                context (Context) -- the Context associated with the Surface.
                text (TextSurface) -- the TextSurface object used to write text.
                draw (DrawSurface) -- the DrawSurface object used to draw things.
        """
        self.surface = cairo.ImageSurface(image_format, width, height)
        self.context = cairo.Context(self.surface)
        self.text = TextSurface(self)
        self.draw = DrawSurface(self)

    def crop(self, x, y, width, height):
        """
        Crop the surface to a given width and height. The (x, y)-coordinates
        mark the top-left corner of the section to be cropped.

        Keyword arguments:
                x (int) -- the left side of the crop.
                y (int) -- the top side of the crop.
                width (int/float) -- the width of the crop.
                height (int/float) -- the height of the crop.
        """
        # Make a new ImageSurface of the width and height given
        cropped_surface = cairo.ImageSurface(self.get_format(), int(width), int(height))

        # Create a Context for the cropped surface
        cropped_context = cairo.Context(cropped_surface)

        # Translate the Context back by the x, y amounts
        cropped_context.translate(-x, -y)

        # Set the source of the Context to be the source surface
        cropped_context.set_source_surface(self.surface)

        # Draw a rectangle of the width and height given, at the coords given
        cropped_context.rectangle(x, y, width, height)

        # Paint it onto the cropped surface
        cropped_context.paint()

        # Delete our old class attributes
        del self.surface
        del self.context
        del self.text
        del self.draw

        # Set the cropped surface as our surface
        self.surface = cropped_surface

        # With the new ImageSurface object, we need to repoint our other
        # attributes at it
        self.context = cairo.Context(self.surface)
        self.text = TextSurface(self)
        self.draw = DrawSurface(self)

        # Delete the cropped surface and its Context
        del cropped_surface
        del cropped_context

    def dot(self, x, y, radius=1, **kwargs):
        """
        Draw a dot of a given radius, centered at (x, y).

        Keyword arguments:
                x (int/str) -- the x-coordinate.
                y (int/str) -- the y-coordinate.
                radius (int) -- the radius of the dot (default 1).
                color (3- or 4-tuple) -- the RGB(A) color of the dot
                        (default (0, 0, 0) (black)).
                fill (bool) -- whether or not to fill the dot with color
                        (default True).
                outline (int) -- the thickness of the dot's outline,
                        in pixels (default 1).
                outline_color (3- or 4-tuple) -- the RGB(A) color of the
                        dot's outline (default 'color').
        """
        self.draw.dot(x, y, radius, **kwargs)

    def ellipse(self, x, y, width, height, **kwargs):
        """
        Draw an ellipse of a given width and height. The (x, y)-coordinates
        correspond to the top-left corner of the bounding box that would
        contain the ellipse.

        Keyword arguments:
                x (int/str) -- the x-coordinate of the ellipse.
                y (int/str) -- the y-coordinate of the ellipse.
                width (int) -- the width of the ellipse.
                height (int) -- the height of the ellipse.
                color (3- or 4-tuple) -- the RGB(A) color of the ellipse
                        (default (0, 0, 0) (black)).
                fill (bool) -- whether or not to fill the ellipse with color
                        (default True).
                outline (int) -- the thickness of the ellipse's outline,
                        in pixels (default 1).
                outline_color (3- or 4-tuple) -- the RGB(A) color of the
                        ellipse's outline (default 'color').
        """
        self.draw.ellipse(x, y, width, height, **kwargs)

    def line(self, x1, y1, x2, y2, **kwargs):
        """
        Draw a line connecting two points at given sets of coordinates.

        Keyword arguments:
                x1 (int/str) -- the x-coordinate of the first point.
                y1 (int/str) -- the y-coordinate of the first point.
                x2 (int/str) -- the x-coordinate of the second point.
                y2 (int/str) -- the y-coordinate of the second point.
                color (3- or 4-tuple) -- the RGB(A) color of the polygon
                        (default (0, 0, 0) (black)).
                line_cap (cairo.LINE_CAP) -- the cap at the end of the line
                        (default cairo.LINE_CAP_SQUARE).
                line_width (int) -- the thickness of the line, in pixels.
        """
        self.draw.line(x1, y1, x2, y2, **kwargs)

    def polygon(self, points, **kwargs):
        """
        Draw a polygon that connects a series of (x, y)-coordinates.

        Keyword arguments:
                points (list) -- a list of xy-coordinates as tuples,
                        indicating the vertices of the polygon.
                color (3- or 4-tuple) -- the RGB(A) color of the polygon
                        (default (0, 0, 0) (black)).
                fill (bool) -- whether or not to fill the polygon with color
                        (default True).
                line_join(cairo.LINE_JOIN) -- the rendering between two
                        joining lines (default cairo.LINE_JOIN_MITER).
                outline (int) -- the thickness of the polygon's outline,
                        in pixels (default 1).
                outline_color (3- or 4-tuple) -- the RGB(A) color of the
                        polygon's outline (default 'color').
        """
        self.draw.polygon(points, **kwargs)

    def rectangle(self, x, y, width, height, **kwargs):
        """
        Draw a rectangle. The (x, y)-coordinates correspond to the
        top-left corner of the rectangle.

        Keyword arguments:
                x (int/str) -- the x-coordinate.
                y (int/str) -- the y-coordinate.
                width (int) -- the width of the rectangle.
                height (int) -- the height of the rectangle.
                color (3- or 4-tuple) -- the RGB(A) color of the rectangle
                        (default (0, 0, 0) (black)).
                fill (bool) -- whether or not to fill the rectangle with color
                        (default True).
                outline (int) -- the thickness of the rectangle's outline,
                        in pixels (default 1).
                outline_color (3- or 4-tuple) -- the RGB(A) color of the
                        rectangle's outline (default 'color').
        """
        self.draw.rectangle(x, y, width, height, **kwargs)

    def rounded_rectangle(self, x, y, width, height, radius, **kwargs):
        """
        Draw a rectangle with rounded corners. The (x, y)-coordinates
        correspond to the top-left corner of the bounding box that would
        contain the rounded rectangle.

        Keyword arguments:
                x (int/str) -- the x-coordinate.
                y (int/str) -- the y-coordinate.
                width (int) -- the width of the rounded rectangle.
                height (int) -- the height of the rounded rectangle.
                radius (int) -- the radius of the rectangle's corners.
                color (3- or 4-tuple) -- the RGB(A) color of the rounded rectangle
                        (default (0, 0, 0) (black)).
                fill (bool) -- whether or not to fill the rounded rectangle with
                        color (default True).
                outline (int) -- the thickness of the rounded rectangle's outline,
                        in pixels (default 1).
                outline_color (3- or 4-tuple) -- the RGB(A) color of the
                        rounded rectangle's outline (default 'color').
        """
        self.draw.rounded_rectangle(x, y, width, height, radius, **kwargs)

    def write(self, text, x, y, font, **kwargs):
        """
        Write text at given coordinates, with given attributes. Return
        the resulting width and height of the bounding box that includes
        the text and padding.

        Keyword arguments:
                text (str) -- the text to be written.
                x (float) -- the x-coordinate of the text.
                y (float) -- the y-coordinate of the text.
                font (str) -- the filename of the font.

        Optional arguments:
                alignment (str) -- the alignment of the text. Can be "left",
                        "center", "right", or "justified" (default "left").
                break_up_lines (bool) -- whether to break text up into multiple
                        lines if it's too long (default True).
                color (3- or 4-tuple) -- the color of the text as an RGB(A)
                        tuple (default (0, 0, 0) (black)).
                font_size (int/str) -- the font size, in pts. If set to "fill",
                        it will be the largest font size it can be (default "fill").
                justify_last_line (bool) -- whether to justify the last line
                        of text , if the text is justified. If set to False, the
                        last line will be left-aligned (default False).
                line_spacing (float) -- the line spacing multiplier (default 1.0).
                max_height (int) -- the maximum vertical space the text and
                        padding will take up. If set to "fill", it will be the
                        largest height needed/allowed (default "fill").
                max_width (int) -- the maximum horizontal space the text and
                        padding will take up. If set to "fill", it will be the
                        largest width needed/allowed (default "fill").
                min_font_size (int) -- the minimum font size, in pts (default 7).
                outline (int) -- the text outline width, in pixels (default 0).
                outline_color (3- or 4-tuple) -- the color of the text outline
                        as an RGB(A) tuple (default (0, 0, 0) (black)).
                padding (dict) -- the padding around the text, in pixels.
                        Any or all of the padding keys can be sent in.
                        (default {"top":0, "right":0, "bottom":0, "left":0}).
        """
        return self.text.write(text, x, y, font, **kwargs)

    def from_pil(self, image, alpha=1.0, image_format=cairo.FORMAT_ARGB32):
        """
        Return a cairo.ImageSurface representation of a given PIL.Image
        object.

        Keyword arguments:
                image (ImageDraw.Draw) -- the Image to convert.
                alpha (float) -- alpha to add to non-alpha images
                        (default 1.0).
                image_format (cairo.FORMAT) -- Pixel image_format for output surface
                        (default cairo.FORMAT_ARGB32).
        """
        # Make sure the format is okay
        assert image_format in (
            cairo.FORMAT_RGB24,
            cairo.FORMAT_ARGB32,
        ), f"Unsupported pixel image_format: '{image_format}'"

        # If there's no alpha channel, add in an opaque one
        if "A" not in image.getbands():
            image.putalpha(int(alpha * 256.0))

        # Convert the PIL.Image object into a bytearray
        arr = bytearray(image.tobytes("raw", "BGRa"))

        # Delete our old class attributes
        del self.surface
        del self.context
        del self.text
        del self.draw

        # Convert the Image bytearray into a new ImageSurface
        self.surface = cairo.ImageSurface.create_for_data(
            arr, image_format, image.width, image.height
        )

        # With the new ImageSurface object, we need to repoint our other
        # attributes at it
        self.context = cairo.Context(self.surface)
        self.text = TextSurface(self)
        self.draw = DrawSurface(self)

    def get_format(self):
        """Return the ImageSurface attribute's format."""
        return self.surface.get_format()

    def get_height(self):
        """Return the ImageSurface attribute's height."""
        return self.surface.get_height()

    def get_width(self):
        """Return the ImageSurface attribute's width."""
        return self.surface.get_width()

    def gridlines(self, color=(0, 0, 0)):
        """
        Outline the surface, and draw vertical and horizontal center lines.

        Keyword arguments:
                color (3- or 4-tuple) -- the color of the gridlines
                        (default (0, 0, 0) (black)).
        """
        self.outline(color=color)
        self.draw.line(
            self.get_width() / 2, 0, self.get_width() / 2, self.get_height(), color=color
        )
        self.draw.line(
            0, self.get_height() / 2, self.get_width(), self.get_height() / 2, color=color
        )

    def outline(self, color=(0, 0, 0), line_width=1):
        """
        Outline the surface.

        Keyword arguments:
                color (3- or 4-tuple) -- the color of the outline
                        (default (0, 0, 0) (black)).
                line_width (int) -- the width of the outline, in pixels
                        (default 1).
        """
        self.draw.rectangle(
            0, 0, self.get_width(), self.get_height(), color=color, outline=line_width, fill=False
        )

    def paste(self, origin, x, y, width=None, height=None, scaling_type="absolute", rotate=0):
        """
        Paste a given cairo.ImageSurface or SimpleSurface object at a
        given (x, y)-coordinate.

        The x, y values specify the top-left corner of where to paste
        the image. These values can also be represented as one of a set
        of strings: "left", "center", or "right" for x, and "top",
        "center", or "bottom" for y.

        If the width/height parameters are left as None, then they
        default to the width/height of the origin Surface.

        The origin Surface is scaled no matter what. If the scaling_type
        parameter is set to "absolute", then the resulting pasted image
        will be exactly the width and height variables (e.g., 600, 800).
        If scaling_type is set to "ratio", then the origin Surface is
        scaled by the ratios set by the width and height variables
        (e.g., 2.0, 1.5).

        The pasted image can also be rotated clockwise in radians (where
        2*pi is one full rotation). The rotation happens about the top-left
        corner (i.e., the (x, y)-coordinate).

        Keyword arguments:
                origin (cairo.ImageSurface/SimpleSurface) -- the
                        surface that's going to be pasted.
                x (float/str) -- the x-coordinate of the image. It can be
                        either a number, or one of "left", "center", or "right".
                y (float/str) -- the y-coordinate of the image. It can be
                        either a number, or one of "top", "center", or "bottom".
                width (float) -- the desired width of the pasted image
                        (default None).
                height (float) -- the desired height of the pasted image
                        (default None).
                scaling_type (str) -- how to scale the pasted image, either
                        "absolute" or "ratio" (default "absolute").
                rotate (float) -- how much to rotate the pasted imaged
                        clockwise, in radians, where 2*pi is one full rotation
                        (default 0).
        """
        # Make sure the parameters follow the proper formatting
        assert scaling_type in ["absolute", "ratio"], (
            f"parameter 'scaling_type' cannot be '{scaling_type}', "
            "must be either 'absolute' or 'ratio'"
        )
        if isinstance(x, str):
            assert x in ["left", "center", "right"], (
                f"parameter 'x' cannot be '{x}', must be either a number "
                "or one of 'left', 'center', or 'right'"
            )
        if isinstance(y, str):
            assert y in ["top", "center", "bottom"], (
                f"parameter 'y' cannot be '{y}', must be either a number "
                "or one of 'top', 'center', or 'bottom'"
            )

        # Save the state of our Context in order to restore it at the end
        self.context.save()

        # If origin is an SimpleSurface object, then we just want to work
        # with its ImageSurface attribute
        if isinstance(origin, SimpleSurface):
            origin = origin.surface

        # Create a SurfacePattern object with which to paste the image
        surface_pattern_origin = cairo.SurfacePattern(origin)

        # Initialize the destination width and height of the image, and the
        # scaling factors
        dest_width = origin.get_width()
        dest_height = origin.get_height()
        scaling_width = 1
        scaling_height = 1

        # Scale it to the width and height, if needed
        if not (width is None and height is None):
            # Leave the width or height if it wasn't sent in
            if width is None:
                width = origin.get_width()
            if height is None:
                height = origin.get_height()

            # Figure out how much to scale by based on the scaling type
            if scaling_type == "absolute":
                scaling_width = width / origin.get_width()
                scaling_height = height / origin.get_height()
            elif scaling_type == "ratio":
                scaling_width = width
                scaling_height = height

            # Recalculate the width and height of the pasted image
            dest_width = scaling_width * origin.get_width()
            dest_height = scaling_height * origin.get_height()

        # Convert the x and y coordinates, if need be
        if x == "left":
            x = 0
        elif x == "center":
            x = (self.get_width() - dest_width) / 2
        elif x == "right":
            x = self.get_width() - dest_width

        if y == "top":
            y = 0
        elif y == "center":
            y = (self.get_height() - dest_height) / 2
        elif y == "bottom":
            y = self.get_height() - dest_height

        # Move to the right place
        self.context.translate(x, y)

        # Rotate the image
        self.context.rotate(rotate)

        # Create a rectangle for the image to be pasted
        self.context.rectangle(0, 0, dest_width, dest_height)

        # Scale the surface to the desired width and height.
        # Scaling is the last thing done because it affects the entire Context.
        if not (dest_width == 0 or dest_height == 0):
            self.context.scale(scaling_width, scaling_height)

        # Set the source of painting to the origin image
        self.context.set_source(surface_pattern_origin)

        # Fill the drawn rectangle with the origin image
        self.context.fill()

        # Restore our Context back to its original state
        self.context.restore()

    def set_background(self, color=(255, 255, 255)):
        """
        Set the surface background to a given color.

        Keyword arguments:
                color (3- or 4-tuple) -- the RGB color of the background
                        (default (255, 255, 255) (white)).
        """
        self.draw.rectangle(0, 0, self.get_width(), self.get_height(), color=color)

    def set_color(self, color):
        """
        Set the color of a Context to an RGB or RGBA tuple (range 0-255).

        Keyword arguments:
                color (3- or 4-tuple) -- the RGB(A) color to set.
        """
        assert len(color) in [3, 4], "parameter 'color' must be a 3- or 4-tuple"

        # Grab the colours and set the alpha to opaque if it's not sent in
        r, g, b, *a = color
        a = a[0] if len(a) > 0 else 255
        self.context.set_source_rgba(r / 255, g / 255, b / 255, a / 255)

    def to_pil(self):
        """
        Return the cairo.ImageSurface object, converted into a PIL.Image
        object.
        """
        # We need to convert the data from RGBA to BGRA manually.
        # If we don't do this, then the colours switch.
        argb_array = numpy.fromstring(bytes(self.surface.get_data()), "c").reshape(-1, 4)
        for el in argb_array:
            el[0:3] = el[0:3][::-1]
        pil_data = argb_array.reshape(-1).tostring()

        # Return the PIL.Image object representing our ImageSurface
        return Image.frombuffer(
            "RGBA",
            (self.surface.get_width(), self.surface.get_height()),
            pil_data,
            "raw",
            "RGBA",
            0,
            1,
        )

    def write_to_pdf(self, target_path, dpi=300):
        """
        Write our Surface to a PDF file.

        Keyword arguments:
                target_path (str) -- the filepath of the PDF file to save to.
                dpi (float) -- the DPI of the image (default 300).
        """
        # Calculate the scale of resolution between our Surface and our PDF
        points_per_inch = 72.0
        pdf_scale = points_per_inch / dpi

        # Create the PDFSurface object at the proper dimensions
        pdf_surface = cairo.PDFSurface(
            target_path,
            self.surface.get_width() * pdf_scale,
            self.surface.get_height() * pdf_scale,
        )
        pdf_context = cairo.Context(pdf_surface)

        # Paint our Surface onto the PDFSurface
        pdf_context.save()
        try:
            pdf_context.identity_matrix()
            pdf_context.scale(pdf_scale, pdf_scale)
            pdf_context.set_source_surface(self.surface)
            pdf_context.paint()
        finally:
            pdf_context.restore()

        # Save the PDF file
        pdf_context.show_page()

    def write_to_png(self, target_path):
        """
        Write our surface object to a PNG file.

        Keyword arguments:
                target_path (str) -- the filepath of the PNG file to save to.
        """
        self.surface.write_to_png(target_path)
