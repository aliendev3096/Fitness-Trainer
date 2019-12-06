import wx;

class NotesPanel(wx.Panel):
    def __init__(self, parent):
        super(NotesPanel, self).__init__(parent)
        self.text = wx.TextCtrl(self, pos=(0,0), style=wx.TE_MULTILINE, size=(980, 675))
        self.notesViewSizer = wx.BoxSizer(wx.VERTICAL)
        self.notesViewSizer.Add(self.text, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(self.notesViewSizer)


    # Routine Event Handler
    def onPageChangeListener(self, event=None):
        user = self.GetParent().GetParent().active_user.replace("&", "");
        with open('./db/{}-notes.txt'.format(user), 'r') as userNotes:
            self.text.SetValue(userNotes.read())
