from security import Root

class Guide(Root.Handler):
    def get(self, name):
        self.render("guide.html")
