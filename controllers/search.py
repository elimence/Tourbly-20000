from security import Root

class Search(Root.Handler):
    def get(self):
        self.render("search.html")