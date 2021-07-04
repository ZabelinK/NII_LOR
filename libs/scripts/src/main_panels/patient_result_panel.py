import os
import wx
import wx.media
import wx.grid
import wx.lib.scrolledpanel as scrolled
from docxtpl import DocxTemplate

from services.sound_service import *

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, '../../bitmaps')


class PatientResultPanel(scrolled.ScrolledPanel):

    def __init__(self, parent, testing_model, test_settings, recognition_service_settings):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.testing_model = testing_model
        self.test_settings = test_settings
        self.recognition_service_settings = recognition_service_settings

        self.SetSize((900, 600))
        self.layoutControls()
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()

    def update(self):
        self.prev_size = self.parent.GetSize()
        self.parent.SetSize(self.GetSize())
        self.grid = wx.GridSizer(self.test_settings.audioFilesNumber, 7, 6, 6)

        self.all_check_box = {}
        self.count = 0
        self.btn_to_file = {}
        btn_count = 0
        self.comment_count = 0
        noise_path = None
        if self.test_settings.noiseFile:
            noise_path = self.recognition_service_settings.noises_dir + self.test_settings.noiseFile

        index = 0
        for item in self.testing_model.testingItems:
            self.comment_count = 0
            index += 1
            labelIndex = wx.StaticText(self, label="  "+str(index)+" аудиозапись: ")
            labelCorrect = wx.StaticText(self, label=item.initialText)
            playOrigBtn = wx.Button(self, id=btn_count, style=wx.SL_INVERSE, label="Play", size=(100, 30))
            playOrigBtn.Bind(wx.EVT_BUTTON, self.playOrigRecord)
            labelRecord = wx.StaticText(self, label=item.resultTest)

            self.btn_to_file[btn_count] = self.recognition_service_settings.words_dir + item.initialAudioFilePath
            btn_count += 1

            playRecBtn = wx.Button(self, id=btn_count, style=wx.SL_INVERSE, label="Play", size=(100, 30))
            playRecBtn.Bind(wx.EVT_BUTTON, self.playCustomerRecord)
            
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

            self.grid.Add(labelIndex, 0, wx.EXPAND)
            self.grid.Add(labelCorrect, 0, wx.EXPAND)
            self.grid.Add(playOrigBtn, 0, wx.EXPAND)
            self.grid.Add(labelRecord, 0, wx.EXPAND)
            self.grid.Add(playRecBtn, 0, wx.EXPAND)
            self.grid.Add(checkBox, 0, wx.EXPAND)
            self.grid.Add(textComment, 0, wx.EXPAND)

            self.all_check_box[checkBox] = item

        self.title = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_title = wx.StaticText(self, -1, "Шаг 5. Результаты тестирования")
        self.fioLabel = wx.StaticText(self, label="{} {}".format("ФИО: ", self.testing_model.firstName + " " + self.testing_model.middleName + " " + self.testing_model.secondName))
        self.birthdayLabel = wx.StaticText(self, label="{} {}".format("Год рождения: ", self.testing_model.birthday))

        self.resultsTestingLabel = wx.StaticText(self, label="Результаты тестирования:")

        self.countLabel = wx.StaticText(self, label="Правильно пройденных тестов {}".format(self.count))

        self.nextBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Начать заново", size=(200, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextPanel)
        self.nextBtn.Hide()

        self.printBtn = wx.Button(self, style=wx.SL_VERTICAL|wx.SL_INVERSE, label="Напечатать результаты", size=(150, 30))
        self.printBtn.Bind(wx.EVT_BUTTON, self.printResults)

        self.graphBtn = wx.Button(self, style=wx.SL_VERTICAL | wx.SL_INVERSE, label="Построить график",
                                  size=(150, 30))
        self.graphBtn.Bind(wx.EVT_BUTTON, self.graphPanel)

        self.printAndGraphSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.printAndGraphSizer.Add(self.printBtn, 0, wx.ALL, 5)
        self.printAndGraphSizer.Add(self.graphBtn, 0, wx.ALL, 5)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.title.Add(self.panel_title, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.mainSizer.Add(self.title)
        self.mainSizer.Add(self.fioLabel)
        self.mainSizer.Add(self.birthdayLabel)
        self.mainSizer.Add(self.resultsTestingLabel)
        self.mainSizer.Add(self.grid)
        self.mainSizer.Add(self.countLabel)
        self.mainSizer.Add(self.printAndGraphSizer)
        self.mainSizer.Add(self.nextBtn)

        self.SetSizer(self.mainSizer)
        self.Layout()


    def updateCheckBox(self, event):
        check_box = event.GetEventObject()
        test_item = self.all_check_box[check_box]
        if check_box.IsChecked():
            check_box.SetLabel("Правильно")
            self.count += 1
            test_item.isCorrect = True
        else:
            check_box.SetLabel("Неправильно")
            self.count -= 1
            test_item.isCorrect = False

        self.updateCountLabel()

    def updateCountLabel(self):
        self.countLabel.SetLabel("Правильно пройденных тестов {}".format(self.count))

    def layoutControls(self):
        wx.InitAllImageHandlers()

    def playOrigRecord(self, event):
        btn = event.GetEventObject()
        noise_file = self.recognition_service_settings.noises_dir + self.test_settings.noiseFile \
                if self.test_settings.noiseFile != '' \
                else None
        play_file(self.btn_to_file[btn.GetId()],self.test_settings.volumeLevelNoice, noise_file)
        
    def playCustomerRecord(self, event):
        btn = event.GetEventObject()
        play_file(self.btn_to_file[btn.GetId()])

    def nextPanel(self, event):
        self.parent.SetSize(self.prev_size)
        self.Hide()
        next_panel = next(self.parent.current_panel)
        next_panel.update()
        next_panel.Show()
        self.Layout()

    def updateCommentText(self, event):
        self.testing_model.testingItems[self.comment_count].commentText = event.GetString()

    def printResults(self, event):
        test_methods = ["AS", "AD", "Бинаурально"]
        play_methods = ["Свободное звуковое поле", "Наушники"]
        device_types = ["-", "Слуховой аппарат", "Кохлеарный имплантат"]
        voice_types = ["Мужчина", "Женщина"]

        doc = DocxTemplate(self.recognition_service_settings.template_dir + "ResultTpl.docx")
        patient_name = self.testing_model.firstName + " " + self.testing_model.secondName
        doctor_name = self.testing_model.doctorFirstName + " " + self.testing_model.doctorSecondName

        context = {
            'test_date': self.testing_model.testDay,
            'patient_name': patient_name,
            'patient_birthday': self.testing_model.birthday,
            'patient_results': self.testing_model.testingItems,
            'patient_diagnosis': self.testing_model.diagnosis,
            'patient_oper': self.testing_model.operation,
            'test_method': test_methods[self.test_settings.analysisMethod],
            'test_sound': play_methods[self.test_settings.soundTool],
            'noise': self.test_settings.noiseFile,
            'noise_prc': str(self.test_settings.volumeLevelNoice) + " Дб",
            'voice': voice_types[self.test_settings.voice],
            'device_info': device_types[self.test_settings.leftTool] + "/" + device_types[self.test_settings.rightTool],
            'device_model': self.test_settings.hearingAidType,
            'countOfWords': self.test_settings.audioFilesNumber,
            'correctWords': self.count,
            'percentOfCorrect': self._getPercentValue(self.count, self.test_settings.audioFilesNumber),
            'doctor_name': doctor_name,
            'doctor_rank': self.testing_model.doctorPosition
        }
        doc.render(context)
        result_file = self.recognition_service_settings.temp_dir + "generated_doc.docx"
        doc.save(result_file)
        os.system('start ' + result_file)

    def _getPercentValue(self, value, count):
        return str(int(value / count * 100)) + "%" if count > 0 else 0

    def graphPanel(self, event):
        self.Hide()
        self.parent.current_panel = self.parent.intensity_graph_panel
        next_panel = self.parent.current_panel
        next_panel.Show()
        self.Layout()