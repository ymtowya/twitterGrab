
import re

class Trend:
    def __init__(self, position, title, views) -> None:
        self.position = position
        self.title = title
        self.views = int(re.findall("\d+", views)[0])
    
    def getPosition(self):
        return self.position
    
    def getViews(self):
        # int(re.findall("\d+",trend.getViews())[0])
        return self.views
    
    def getTitle(self):
        return self.title
