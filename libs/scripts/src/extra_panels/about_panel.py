import wx.media

from libs.scripts.src.application import *


class AboutPanel(wx.Panel):

    def __init__(self, parent, message):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.message = message
        self.SetSize((200, 200))
        self.layoutControls()

    def update(self):
        pass

    def layoutControls(self):
        self.errorLabel = wx.StaticText(self, label=self.message, size=(200, 90))
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizer.Add(self.errorLabel, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.Layout()
