certnames = [
    "Best Hopscotch Player Award",
    "Most Creative Painting Award"
]

# box starts from TOP-LEFT
# box ends at BOTTOM-RIGHT

name_box = {
    "start": {
        "x": 158,
        "y": 368
    },
    "end": {
        "x": 680,
        "y": 410
    }
}

# This is maximum font size;
# actual font size may be smaller
# when box is too small to fit
# normal font-sized text
name_font_size = 23
name_font_path = "Fonts/PRAGMBL.ttf"

date_box = {
    "start": {
        "x": 159,
        "y": 424
    },
    "end": {
        "x": 683,
        "y": 450
    }
}   

date_font_size = 30
date_font_path = "Fonts/OpenSans-Bold.ttf"

cert_name_box = {
    "start": {
        "x": 0,
        "y": 313
    },
    "end": {
        "x": 842,
        "y": 342
    }
}

cert_name_font_size = 32
cert_name_font_spacing = 1
cert_name_font_path = "Fonts/PRAGMBL.ttf"

from PIL import Image, ImageDraw, ImageFont
from time import sleep
import re

debug = False
drawer = None

class ObjectInImage:
    def __init__(self, start):
        self.start = {"x", "y"}

        if type(start) is tuple:
            self.start["x"] = start[0]
            self.start["y"] = start[1]
        elif type(start) is dict:
            self.start = start


class DrawInImage(ObjectInImage):
    def __init__(self, start, end):
        ObjectInImage.__init__(self, start)

        self.end = {"x", "y"}

        if type(end) is tuple:
            self.end["x"] = end[0]
            self.end["y"] = end[1]
        elif type(start) is dict:
            self.end = end

        self.size = {"x": self.end["x"] - self.start["x"],
                     "y": self.end["y"] - self.start["y"]}


class PasteImageInImage(ObjectInImage):
    """
    Pasting an image in another image.
    Optionally resize image by passing size dict {x, y}.
    """

    # Here start will be bottom-left pixel as our sign is oriented as such.
    def __init__(self, start, img, paste_img, size = None):
        ObjectInImage.__init__(self, start)
        self.img = img
        self.paste_img = Image.open(paste_img)
        
        if size != None:
            size = (self.paste_img.size[0], self.paste_img.size[1]) * round(min(size["x"]/self.paste_img.size[0], size["y"]/self.paste_img.size[1]))
            print(size)
            self.paste_img.resize(size, Image.LANCZOS)

    def commit_to_image(self):
        self.img.paste(self.paste_img, (self.start["x"], self.start["y"]))


class TextInImage(DrawInImage):
    """For drawing text in an image."""

    def __init__(self, start, end, text_details):
        """start, end are dictionaries with keys: \"x\", \"y\", representing pixel coordinates.
        (Coordinates are from top-left of the image)\n
        text_details has three keys: \"text\", \"path\", \"size\" (size is font size, i.e. int)
        path is font path, and size is desired font size."""
        DrawInImage.__init__(self, start, end)

        self.text = text_details["text"]

        def fontSizeFinder(fnt_path, fnt_size, string, width, height):
            """Finds appropriate font size given maximum width and height."""

            try:
                fnt = ImageFont.truetype(fnt_path, fnt_size)
            except OSError:
                print("Font:", fnt_path, "not found.")
                exit(1)

            # Tuple comparison is strange (reference: https://stackoverflow.com/a/5292332/10147642), so this:
            while any(map((lambda x, y: x >= y), fnt.getsize(string), (width, height))):
                if debug is True:
                    print(fnt.getsize(string), ">=",
                          (width, height), "is True.")  # Debug
                fnt_size = fnt_size - 1
                if fnt_size < 5:
                    print(string, "is not fitting in, terminating")
                    exit(0)
                fnt = ImageFont.truetype(fnt_path, fnt_size)
            if debug is True:
                print(fnt.getsize(string), ">=",
                      (width, height), "is False.")
            return fnt
        self.fnt = fontSizeFinder(text_details["path"], text_details["size"],
                                  text_details["text"], end["x"] - start["x"], end["y"] - start["y"])

        text_size = self.fnt.getsize(self.text)
        self.size = {
            "x": text_size[0],
            "y": text_size[1]
        }

    def center(self):
        """Horizontally centers the text (i.e. in the x dimension) within the constraints."""

        start = (self.start["x"] + self.end["x"] - self.size["x"]) / 2
        end = (self.start["x"] + self.end["x"] + self.size["x"]) / 2

        self.start["x"] = start
        self.end["x"] = end

        if debug:
            print("On center align: ")
            print("Start x: ", self.start["x"], ", End x: ", self.end["x"])
        return self

    def bottom_align(self):
        """Bottom aligns the text within the constraints."""
        self.start["y"] = self.end["y"] - self.size["y"]

        if debug is True:
            print("On bottom align: ")
            print("Start y: ", self.start["y"], ", End y: ", self.end["y"])
        return self

    def commit_to_image(self):
        """Writes text to image."""
        drawer.text((self.start["x"], self.start["y"]),
                    self.text, font=self.fnt, fill=(0, 0, 0))

class SpacedTextInImage(TextInImage):
    def __init__(self, start, end, text_details, spacing):
        TextInImage.__init__(self, start, end, text_details)
        self.spacing = spacing
        # Add more to size to accomodate spacing.
        self.size["x"] += len(self.text) * spacing
        if debug is True:
            print(self.size["x"], "was increased by", len(
                self.text) * spacing, "to accomodate spacing.")

    def commit_to_image(self):
        curr = self.start
        for char in self.text:
            drawer.text((curr["x"], curr["y"]),
                        char, font=self.fnt, fill=(0, 0, 0))
            # Put line spacing
            curr["x"] += self.fnt.getsize(char)[0] + self.spacing
        if debug is True:
            print("Inserted spacing:", curr["x"],
                  "should be equal to:", self.end["x"])


def main():
    img_path = "template.png"
    signatures_path = {
        "President": "Signatures/Signature-1.png",
        "VPEd": "Signatures/Signature-2.png"
    }
    fonts_path = {
        "open-sans": "Fonts/OpenSans-Bold.ttf",
        "pragmbl": "Fonts/PRAGMBL.ttf"
    }

    name = input("Enter recipient name: ")
    date = "On " + str(input("Enter date: "))

    def getcertname():
        for index, name in enumerate(certnames, 1):
            print("{0}: {1}".format(index, name))
        num = int(input("Please enter certificate (number): "))
        try:
            return certnames[num - 1]
        except IndexError:
            print("Invalid input.")
            return getcertname()

    cert_name = getcertname()

    try:
        img = Image.open(img_path)
    except FileNotFoundError:
        print('File not found. Please remember to write full file name.')
        print('Example: \'example.png\' or \'example.jpg\', etc. Exiting now.')
        sleep(2.5)
        exit(1)

    global drawer
    drawer = ImageDraw.Draw(img)

    # Best way to determine coordinates is to go in Paint and draw a box around all the text, then note the coordinates you start, and the point where your cursor stops.
    TextInImage(name_box["start"], name_box["end"], {
        "text": name, "path": name_font_path, "size": name_font_size}).center().bottom_align().commit_to_image()
    TextInImage(date_box["start"], date_box["end"], {
        "text": date, "path": date_font_path, "size": date_font_size}).center().bottom_align().commit_to_image()
    SpacedTextInImage(cert_name_box["start"], cert_name_box["end"], {
        "text": cert_name, "path": cert_name_font_path, "size": cert_name_font_size}, cert_name_font_spacing).center().bottom_align().commit_to_image()

    filename = (name+'_'+cert_name+'_'+date).replace(' ', '_')
    img.save(filename)
    img.show()

main()
