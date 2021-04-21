import os
import wx
import wx.media
import wx.lib.buttons as buttons

import sounddevice as sd
import soundfile as sf
import numpy as np
import requests
import json 


dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')
########################################################################
class MediaPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        
        self.frame = parent
        self.currentVolume = 50
        self.layoutControls()
        
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()
        


        # record parameters
        self.fs = 8000
        self.data = np.empty([1, 2])
        self.wav_name = "../workdir/out.wav"
        self.recognize_service = 'https://asr.kube.plintum.dev/recognize?lang=ru'
        self.hideRecordCircle()
        
        
    #----------------------------------------------------------------------

    def layoutControls(self):
        """
        Create and layout the widgets
        """
        
        wx.InitAllImageHandlers()

        try:
            self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
        except NotImplementedError:
            self.Destroy()
            raise

        self.recordBtn = wx.ToggleButton(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Начать запись", size=(120, 30))
        self.recordBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onRecord)

        self.textRes = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP, 
            value="", name="Результаты распознавания", size=(400, 500))

        self.helpLabel = wx.StaticText(self, label="Для того чтобы начать распознавать голос, " \
                                        "нажмите на кнопку 'Начать запись', говорите фразы в микрофон, " \
                                        "а затем нажмите на кнопку еще раз. Распознанный текст выведется " \
                                        "в текстовое поле через 1-10 секунд.", size=(400, 90))

        self.textLabel = wx.StaticText(self, label="Распознанный текст")

        self.redCircle = wx.StaticBitmap(self, bitmap=wx.Bitmap("../libs/scripts/bitmaps/circle.png", wx.BITMAP_TYPE_PNG), size=(32, 32))

        self.recordLabel = wx.StaticText(self, label="Идет запись")

        # Create sizers
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vvSizer = wx.BoxSizer(wx.VERTICAL)

        self.vvSizer.Add(self.recordBtn, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.vvSizer.Add(self.redCircle, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.vvSizer.Add(self.recordLabel, 0, wx.ALL|wx.ALIGN_CENTER, 5)


        self.hSizer.Add(self.vvSizer, 0, wx.ALL, 5)
        self.hSizer.Add(self.helpLabel, 0, wx.ALL, 5)

        # layout widgets
        self.vSizer.Add(self.hSizer, 0, wx.ALL, 5)
        self.vSizer.Add(self.textLabel, 0, wx.ALL, 5)
        self.vSizer.Add(self.textRes, 0, wx.ALL, 5)
        self.mainSizer.Add(self.vSizer)
        
        self.SetSizer(self.mainSizer)
        self.Layout()


    def hideRecordCircle(self):
        self.redCircle.Hide()
        self.recordLabel.Hide()
        self.Layout()

    def showRecordCircle(self):
        self.redCircle.Show()
        self.recordLabel.Show()        
        self.Layout()

    def saveDataToWav(self):
        """
        Save audio data to wav file
        """

        sf.write(self.wav_name, self.data, self.fs)

    def recognizeWav(self):
        """
        Open wav file and send reques to recognizion service to recognize audio data
        """

        with open(self.wav_name, "rb") as binaryfile :
            wav_data = bytearray(binaryfile.read())

        print("Data saved to {}".format(self.wav_name))


        try:
            rsp = requests.post(self.recognize_service, data = wav_data)
            print("Response from recognize service {}".format(str(rsp)))
            return json.loads(rsp.text)["text"]
        except Exception as e:
            print(e)
            return "< ERROR > Ошибка в консоле"

    def startRecord(self):
        """
        Start record from micro
        """
        def callback(indata, frames, time, status):
            self.data = np.append(self.data, indata, axis=0)

        self.data = np.empty([1, 2])
        self.stream = sd.InputStream(samplerate=self.fs, channels=2, callback=callback)
        self.stream.start()
        self.showRecordCircle()
        print("Start recording")
    
    def stopRecord(self):
        """
        Stop Record
        """
        self.stream.stop()
        self.hideRecordCircle()
        print("Stop Recording")
        self.saveDataToWav()
        text = self.recognizeWav()

        print("Result : {}".format(text))

        self.textRes.Clear()
        if text is None:
            self.textRes.write("< Произошла ошибка, подробности в консоли >")
        else:
            self.textRes.write(text)
        


    def onRecord(self, event):
        """
        Start and stop record
        """

        if self.recordBtn.GetValue() == True:
            self.recordBtn.SetLabel("Остановить запись")
            self.startRecord()

        else:
            self.recordBtn.SetLabel("Начать запись")
            self.recordBtn.Disable()
            self.stopRecord()
            self.recordBtn.Enable()

########################################################################
class MediaFrame(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "НИИ ЛОР - Тестирование звука")
        panel = MediaPanel(self)
        
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MediaFrame()
    frame.Show()
    app.MainLoop()