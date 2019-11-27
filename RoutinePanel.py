import wx;

class RoutinePanel(wx.Panel):
    def __init__(self, parent):
        super(RoutinePanel, self).__init__(parent)
        self.active_routine = self.GetParent().GetParent().active_routine
        # Binding method listener to set routine when note page has changed
        parent.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onPageChangeListener)

    def onPageChangeListener(self, event=None):
        self.active_routine = self.GetParent().GetParent().active_routine
        print(self.active_routine)