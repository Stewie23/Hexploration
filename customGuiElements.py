from ocempgui.widgets.components import TextListItem

from ocempgui.widgets.Container import Container
import ocempgui.widgets.base as base
from ocempgui.widgets.StyleInformation import StyleInformation
import ocempgui.widgets.BaseWidget as BaseWidget
from ocempgui.widgets.Constants import *


class mTextListItem(TextListItem):
#custom TextListItemt with return text function
    def get_text (self):
        return self._text
    

   
  