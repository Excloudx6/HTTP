from get_html import get_html
from xpath import DOM_nav
from gui import GUI

# get html
req = get_html()
req.url = "https://jaredbot.uk"
req.search()
html = req.html

#html = """
#<html>
#    <h1>Heading 1</h1>
#    <h2>Heading 2</h2>
#    <h3>Heading 3</h3>
#    <h4>Heading 4</h4>
#    <h5>Heading 5</h5>
#    <h6>Heading 6</h6>
#    <a href="https://google.com">Link to google</a>
#</html>
#"""

# traverse html
nav = DOM_nav()
gui = GUI()
for elm in nav.traverse_tree(html):
    tag, attr, text = elm
    print(elm)

    # add element to GUI
    gui.process_tag(tag, text, attr)
