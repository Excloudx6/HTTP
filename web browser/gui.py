import tkinter, re
from PIL import ImageTk, Image
from get_html import get_html

# Global Defaults
DEF_FONT = "Arial"
DEF_FONT_SIZE = 16
DEF_FONT_COLOUR = "black"
DEF_FONT_POS = "center"

class GUI():
    def __init__(self):
        self.row_counter = 0
        self.font = "Arial"
        self.font_size = 16
        self.colour = "black"
        self.pos = "center"
        self.canvas = tkinter.Tk()
        self.row_counter = 0
        self.column_counter = 0
        self.button_width = 30
        self.tag_sizes = {
                "h1" : 32,
                "h2" : 24,
                "h3" : 20,
                "h4" : 16,
                "h5" : 12,
                "h6" : 11
        }

    def add_text(self, txt, padding = (0, 0), colour = DEF_FONT_COLOUR,
        pos = DEF_FONT_POS, font = DEF_FONT, size = DEF_FONT_SIZE, href=""):
        title = tkinter.Label(self.canvas, fg=colour, anchor=pos)
        title.config(font=(font, size), text=txt)
        title.grid(row=self.row_counter,
            column=self.column_counter,
            padx=padding[0],
            pady=padding[1],
            sticky=tkinter.W)
        self.row_counter += 1

    def add_button(self, txt, callback, padding = (0, 0)):
        button = tkinter.Button(self.canvas, text=txt, command=callback)
        button.config(width=self.button_width)
        button.grid(row=self.row_counter,
            column=self.column_counter,
            padx=padding[0],
            pady=padding[1],
            sticky=tkinter.W)
        self.row_counter += 1

    def add_image(self, url, padding = (0, 0)):
        img = ImageTk.PhotoImage(Image.open(url))
        im = tkinter.Label(self.canvas, image = img)
        im.image = img
        im.grid(row=self.row_counter,
            column=self.column_counter,
            padx=padding[0],
            pady=padding[1],
            sticky=tkinter.W)
        
        self.row_counter += 1

    def download_image(self, url):
        req = get_html()
        req.url = url
        req.search()

        filename = re.compile(r"https?:/.+/(.+\.\w+)$").findall(url)[0]
        with open(filename, "wb") as file:
            file.write(req.html)

        return filename

    def process_tag(self, tag, text, attributes):
        ''' Adds HTML tag to canvas '''

        # title
        if tag == "title":
            self.canvas.title = text

        # heading 1-6
        elif re.compile("h[1-6]").search(tag) != None:
            self.add_text(text, size=self.tag_sizes[tag])

        # a tag
        elif tag == "a":
            if "href" in attributes.keys():
                self.add_text(text, size=self.font_size, colour="blue", href=attributes["href"])
            else:
                self.add_text(text, size=self.font_size, colour=self.colour)

        #p tag
        elif tag == "p":
            self.add_text(text, size=self.font_size)

        #img tag
        elif tag == "img":
            if "src" in attributes.keys():
                file = self.download_image(attributes["src"])
                self.add_image(url = file)
            

#gui = GUI()
#gui.add_title("Hello World", size=8)
#gui.add_title("Hello World", size=16)
#gui.add_image(url = "http://jaredbot.uk/img/src/web/lion-blur.png")

# title changes the window title
# a tag inserts a link
# img inserts an image
# h1 to h6 headings
