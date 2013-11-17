from security import Root


class Places(Root.Handler):
    def get(self):
        places = Destination.Destination.getAllDestination()
        self.render("places.html", places = places)
