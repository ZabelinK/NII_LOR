import logging
import wx

def exception_logger(error):
    logger = logging.getLogger(__name__)
    # Create handlers
    #можно отключить вывод в консоль убрав c_handler
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('../logs/file.log')
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.ERROR)
    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    logger.warning(error)
    logger.error(error, exc_info=True)

def error_message(obj, error):
    # if not hasattr(obj, 'dlg'):
    dlg = wx.MessageDialog(None, str(error), "Error", wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    # else:
    #     dlg = wx.MessageDialog(None, str(error), "Error", wx.OK | wx.ICON_INFORMATION)
    #     dlg.ShowModal()


