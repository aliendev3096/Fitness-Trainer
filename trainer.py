# Author: Jeff Vang
# https://exrx.net/Lists/Directory
from classes import Workout, DailyRoutine, WeeklyRoutine
import MainWindow;
import wx;

def main():
    # Create a GUI?
    # Initialize Application
    app = wx.App();
    frame = MainWindow.MainWindow(None, "PyExFitness");
    app.MainLoop();


main();