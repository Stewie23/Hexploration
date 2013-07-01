from ocempgui.widgets.components import TextListItem

class mTextListItem(TextListItem):
#custom TextListItemt with return text function
    def get_text (self):
        return self._text