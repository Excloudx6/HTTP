from bs4 import BeautifulSoup
import requests

# example xpath
#document.querySelectorAll('div[id="main-body"] div[id="add-bot"] div[class="add-bot-div"] h4')[0]

class DOM_nav():
    def __init__(self):
        self.tree = []
    
    def xpath(self, path):
        elms = filter(None, path.split(" "))
        element = soup
        for elm in elms:
            if "[" in elm and "]" in elm:
                # get attributes
                raw = [i.split("]")[0] for i in elm.split("[")]
                tag_name, attributes = raw[0], raw[1:]

                current_elms = []
                for attribute in attributes:
                    attribute_name, attribute_value = attribute.split("=")
                    attribute_value = attribute_value.replace("'",'').replace('"',"")
                    
                    if attribute_name == "id":
                        element = element.find(tag_name, id=attribute_value)
                        if element:
                            current_elms.append(element)

                    elif attribute_name == "class":
                        element = element.find(tag_name, class_=attribute_value)
                        if element:
                            current_elms.append(element)

                # compare attributes of current element
                # check if the attributes refer to the same element
                if len(set([i.contents[0] for i in current_elms])) != 1:
                    return "Failed to find xpath!"
            else:
                element = element.find(elm)     

        return element

    def get_xpath(self, html, query):
        soup = BeautifulSoup(html, 'lxml')
        elm = xpath(query)
        return elm

    def traverse_tree(self, html):
        ''' creates generator '''
        soup = BeautifulSoup(html, 'lxml')
        self.traverse(soup)
        return self.tree

    def traverse(self, soup):
        ''' Traverse through the DOM'''
        if hasattr(soup, "children"):
            for kid in soup.children:
                if kid.name != None:
                    self.tree.append([kid.name, kid.attrs, kid.text])
                self.traverse(kid)


# generator - soup.children
# a[0].name - gets name of first child
# a[0].attrs - gets attributes

