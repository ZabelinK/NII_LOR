import os
import wx
import wx.media
import wx.grid

from patient_testing_model import *
from recognition_service import *
from microphone_service import *

from sound_service import *
from constants import *
from docxtpl import DocxTemplate

import wx.lib.scrolledpanel as scrolled

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')



class PatientResultPanel(scrolled.ScrolledPanel):

    def __init__(self, parent, testing_model, test_settings, recognition_service_settings):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.testing_model = testing_model
        self.test_settings = test_settings
        self.recognition_service_settings = recognition_service_settings

        self.SetSize((1200, 600))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def update(self):

        self.SetSize((1200, 600))
        self.grid = wx.GridSizer(self.test_settings.audioFilesNumber, 6, 6, 6)

        self.all_check_box = []
        self.count = 0
        self.btn_to_file = {}
        btn_count = 0
        self.comment_count = 0
        noise_path = None
        if self.test_settings.noiseFile:
            noise_path = self.recognition_service_settings.noises_dir + self.test_settings.noiseFile

        for item in self.testing_model.testingItems:
            self.comment_count = 0
            labelCorrect = wx.StaticText(self, label=item.initialText)
            playOrigBtn = wx.Button(self, id=btn_count, style=wx.SL_INVERSE, label="Play", size=(100, 30))
            playOrigBtn.Bind(wx.EVT_BUTTON, self.playRecord)
            labelRecord = wx.StaticText(self, label=item.resultTest)

            self.btn_to_file[btn_count] = self.recognition_service_settings.words_dir + item.initialAudioFilePath
            btn_count +=1

            playRecBtn = wx.Button(self, id=btn_count, style=wx.SL_INVERSE, label="Play", size=(100, 30))
            playRecBtn.Bind(wx.EVT_BUTTON, self.playRecord)
            
            self.btn_to_file[btn_count] = self.recognition_service_settings.temp_dir + item.resultAudioFilePath
            btn_count +=1

            checkBox = wx.CheckBox(self)
            checkBox.Bind(wx.EVT_CHECKBOX, self.updateCheckBox)

            if item.isCorrect:
                checkBox.SetLabel("Правильно")
                checkBox.SetValue(True)
                self.count += 1
            else:
                checkBox.SetLabel("Неправильно")
                checkBox.SetValue(False)

            textComment = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_WORDWRAP,
                                      value="", name="Комментарий", size=(100, 30))
            textComment.Bind(wx.EVT_TEXT, self.updateCommentText)
            self.comment_count += 1


            self.grid.Add(labelCorrect, 0, wx.EXPAND)
            self.grid.Add(playOrigBtn, 0, wx.EXPAND)
            self.grid.Add(labelRecord, 0, wx.EXPAND)
            self.grid.Add(playRecBtn, 0, wx.EXPAND)
            self.grid.Add(checkBox, 0, wx.EXPAND)
            self.grid.Add(textComment, 0, wx.EXPAND)

            self.all_check_box.append(checkBox)

        self.fioLabel = wx.StaticText(self, label="{} {}".format("ФИО: ", self.testing_model.firstName + " " + self.testing_model.secondName))
        self.birthdayLabel = wx.StaticText(self, label="{} {}".format("Год рождения: ", self.testing_model.birthday))

        self.resultsTestingLabel = wx.StaticText(self, label="Результаты тестирования:")

        self.countLabel = wx.StaticText(self, label="Правильно пройденных тестов {}".format(self.count))

        self.nextBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Начать заново", size=(200, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)

        self.printBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Напечатать результаты", size=(200, 30))
        self.printBtn.Bind(wx.EVT_BUTTON, self.printResults)


        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.fioLabel)
        self.mainSizer.Add(self.birthdayLabel)
        self.mainSizer.Add(self.resultsTestingLabel)
        self.mainSizer.Add(self.grid)
        self.mainSizer.Add(self.countLabel)
        self.mainSizer.Add(self.printBtn)
        self.mainSizer.Add(self.nextBtn)

        self.SetSizer(self.mainSizer)
        self.Layout()


    def updateCheckBox(self, event):
        check_box = event.GetEventObject()
        if check_box.IsChecked():
            check_box.SetLabel("Правильно")
            self.count += 1
        else:
            check_box.SetLabel("Неправильно")
            self.count -= 1
        self.updateCountLabel()

    def updateCountLabel(self):
        self.countLabel.SetLabel("Правильно пройденных тестов {}".format(self.count))

    def layoutControls(self):
        wx.InitAllImageHandlers()

    def playRecord(self, event):
        btn = event.GetEventObject()
        play_file(self.btn_to_file[btn.GetId()])
        
    def nextPanel(self, event):
        self.Hide()
        next_panel = next(self.parent.current_panel)
        next_panel.update()
        next_panel.Show()
        self.Layout()

    def updateCommentText(self, event):
        self.testing_model.testingItems[self.comment_count].commentText = event.GetString()

    def printResults(self, event):
        doc = DocxTemplate(self.recognition_service_settings.template_dir + "ResultTpl.docx")
        patient_name = self.testing_model.firstName + " " + self.testing_model.secondName
        doctor_name = self.testing_model.doctorFirstName + " " + self.testing_model.doctorSecondName
        correct_number = self._getCorrectTests()

        context = {
            'test_date': self.testing_model.testDay,
            'patient_name': patient_name,
            'patient_birthday': self.testing_model.birthday,
            'patient_results': self.testing_model.testingItems,
            'noise': self.test_settings.noiseFile,
            'countOfWords': self.test_settings.audioFilesNumber,
            'correctWords': correct_number,
            'percentOfCorrect': self._getPercentValue(correct_number, self.test_settings.audioFilesNumber),
            'doctor_name': doctor_name,
            'doctor_rank': "Самый главный доктор"
        }
        doc.render(context)
        result_file = self.recognition_service_settings.temp_dir + "generated_doc.docx"
        doc.save(result_file)
        os.system('start ' + result_file)

    def _getPercentValue(self, value, count):
        return str(int(value / count * 100)) + "%" if count > 0 else 0

    def _getCorrectTests(self):
        result = 0
        for item in self.testing_model.testingItems:
            print(" Comment:", item.commentText, "\n")
            if item.isCorrect:
                result += 1
        return result
