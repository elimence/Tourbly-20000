from security import Root

class Guide(Root.Handler):
    def get(self):
        self.render("guide.html")