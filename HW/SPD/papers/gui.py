import json
import sys
import os

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication as Application, QWidget, QPushButton as Button, QFileDialog, QComboBox
from PyQt5.QtWidgets import QLabel as Label, QGridLayout, QDesktopWidget, QSlider

#import design_lbl
import design

#class ProgramGUI(QtWidgets.QMainWindow, design_lbl.Ui_MainWindow):
class ProgramGUI(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.title = 'SPD papers tests'
        self.setWindowTitle(self.title)
        self.left = 100
        self.top = 100
        self.width = 1600
        self.height = 1000

        self.DEFAULT_TASK_PATH = "tasks"
        self.label_title.setText(f'Тестирующая система.')
        self.BOUNDARY_LENGTH = 70

        self.dict_label_answer = {1: self.label_answer1, 2: self.label_answer2,
                                  3: self.label_answer3, 4: self.label_answer4}

        self.dict_checkbox = {1: self.checkBox_1, 2: self.checkBox_2,
                              3: self.checkBox_3, 4: self.checkBox_4}

        for key, value in self.dict_checkbox.items():
            not_resize = value.sizePolicy()
            not_resize.setRetainSizeWhenHidden(True)
            value.setSizePolicy(not_resize)

        self.filename_list = []
        for file_name in os.listdir(self.DEFAULT_TASK_PATH):
            self.filename_list.append(file_name)
            self.comboBox_task.addItem(file_name.replace(".json", ""))
        self.load_questions(os.path.join(self.DEFAULT_TASK_PATH, self.filename_list[0]))
        self.setup_task()

        self.comboBox.activated.connect(self.change_question)
        self.comboBox_task.activated.connect(self.choose_task)
        self.slider.valueChanged.connect(self.change_question)
        self.button_answer.clicked.connect(self.push_answer_button)
        self.button_finish.clicked.connect(self.push_finish_button)



        #self.gui_change_window_size()

    # def gui_change_window_size(self):
    #     width_cur = self.centralwidget.width()
    #     height_cur = self.centralwidget.height()
    #     if width_cur != 100 and height_cur != 30:
    #         self.centralwidget.setFixedWidth(width_cur - 1)
    #         self.centralwidget.setFixedWidth(width_cur)
    #         self.centralwidget.setFixedHeight(height_cur - 1)
    #         self.centralwidget.setFixedHeight(height_cur)
    #         self.center()

    def choose_task(self):
        load_ind = self.comboBox_task.currentIndex()
        self.load_questions(os.path.join(self.DEFAULT_TASK_PATH, self.filename_list[load_ind]))
        self.setup_task()

    def load_questions(self, load_path):
        with open(load_path, encoding='utf-8') as file:
            data = json.load(file)
            self.task_number = data["task_number"]
            self.questions_all = data['questions_all']
            self.n_questions = len(self.questions_all)

    def setup_task(self):
        self.button_finish.setEnabled(True)

        self.current_ind = 0
        #self.comboBox.setCurrentIndex(0)
        try:
            self.slider.valueChanged.disconnect()
            self.comboBox.activated.disconnect()
        except:
            pass

        self.comboBox.clear()
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.n_questions - 1)

        for i in range(self.n_questions):
            self.comboBox.addItem(f'question {str(i + 1)}')

        self.slider.setValue(0)

        self.comboBox.activated.connect(self.change_question)
        self.slider.valueChanged.connect(self.change_question)

        self.n_answered = 0
        self.is_finish = False
        self.answer_log = {}

        self.answers_true = {}
        self.answers_false = {}
        self.answers_miss = {}
        self.max_true_answers = 0
        self.obtained_true_answers = 0
        self.obtained_false_answers = 0
        self.obtained_miss_answers = 0
        self.real_true_answer = {}

        self.set_question()
        self.set_progress()


    def set_progress(self):
        if self.is_finish:
            self.label_progress.setText(f'Правильных ответов: {str(self.obtained_true_answers)}' +
                                        f'/{str(self.max_true_answers)}' + '\n' +
                                        f'Неправильных ответов: {str(self.obtained_false_answers)}' + '\n' +
                                        f'Пропущенных ответов: {str(self.obtained_miss_answers)}')
        else:
            self.label_progress.setText(f'Ваш прогресс: {str(len(self.answer_log))}/{str(self.n_questions)}')





    def change_question(self):
        combobox_current_index = self.comboBox.currentIndex()
        slider_current_index = self.slider.value()
        if combobox_current_index != self.current_ind:
            current_ind = combobox_current_index
            self.slider.setValue(current_ind)
            self.current_ind = current_ind
            self.set_question()
        elif slider_current_index != self.current_ind:
            current_ind = slider_current_index
            self.comboBox.setCurrentIndex(current_ind)
            self.current_ind = current_ind
            self.set_question()





    def set_text(self, label, text):
        words = text.split()

        cur_len = 0
        for ind, el in enumerate(words):
            cur_len += len(el) + 1
            if cur_len >= self.BOUNDARY_LENGTH:
                words.insert(ind + 1, "\n")
                cur_len = 0

        new_text = " ".join(el for el in words)
        label.setText(new_text)

    def set_question(self):
        ind = self.current_ind
        current_question = self.questions_all[ind]
        #self.label_question.setText(f"Вопрос {str(ind + 1)}. " + current_question['question'])
        self.set_text(self.label_question, f"Вопрос {str(ind + 1)}. " + current_question['question'])
        current_question_count = len(current_question) - 2

        for i, el in enumerate(current_question):
            if i > 1:
                current_answer_label = self.dict_label_answer[i - 1]
                current_checkbox = self.dict_checkbox[i - 1]
                current_answer_json = "answer_" + str(i - 1)
                #current_answer_label.setText(current_question[current_answer_json])
                self.set_text(current_answer_label, current_question[current_answer_json])
                current_checkbox.show()
                if self.answer_log.get(ind):
                    if i - 1 in self.answer_log[ind]:
                        current_checkbox.setChecked(True)
                    else:
                        current_checkbox.setChecked(False)
                else:
                    current_checkbox.setChecked(False)

                current_answer_label.setStyleSheet("background-color: white")
                if self.is_finish:
                    if i - 1 in self.answers_true[ind]:
                        current_answer_label.setStyleSheet("background-color: lightgreen")
                    elif i - 1 in self.answers_false[ind]:
                        current_answer_label.setStyleSheet("background-color: rgb(255, 127,127)")
                    elif i - 1 in self.real_true_answer[ind]:
                        current_answer_label.setStyleSheet("background-color: rgb(255, 255,224)")

        for i in range(current_question_count + 1, 5):
            current_answer_label = self.dict_label_answer[i]
            current_answer_label.setText('')
            current_checkbox = self.dict_checkbox[i]
            #current_checkbox.hide()
            current_checkbox.setVisible(False)
            current_checkbox.setChecked(False)
            current_answer_label.setStyleSheet("background-color: rgb(250, 250, 255)")


    def push_answer_button(self):
        self.answer_log[self.current_ind] = []
        for k in self.dict_checkbox:
            if self.dict_checkbox[k].isChecked():
                self.answer_log[self.current_ind].append(k)

        if len(self.answer_log[self.current_ind]) > 0:
            self.set_progress()

        #print(self.answer_log)
        if len(self.answer_log) == self.n_questions:
            #self.print_results()
            pass
        elif self.current_ind < self.n_questions - 1:
            current_ind = self.current_ind + 1
            self.slider.setValue(current_ind)
        else:
            for i in range(self.n_questions):
                is_answer_i = self.answer_log.get(i)
                if is_answer_i is None:
                    current_ind = i
                    break
            self.slider.setValue(current_ind)


    def print_results(self):
        pass


    def push_finish_button(self):
        self.button_finish.setDisabled(True)
        self.check_true_answers()
        self.is_finish = True
        self.set_progress()
        self.set_question()

    def check_true_answers(self):
        for i in range(self.n_questions):
            self.answers_true[i] = []
            self.answers_false[i] = []
            self.answers_miss[i] = []
            current_question = self.questions_all[i]
            true_answer = current_question["true_answer"]
            current_answer = self.answer_log.get(i)
            self.real_true_answer[i] = true_answer
            self.max_true_answers += len(true_answer)

            for j in range(len(self.questions_all[i]) - 2):
                if not (current_answer is None):
                    if j + 1 in current_answer and j + 1 in true_answer:
                        self.answers_true[i].append(j + 1)
                    elif j + 1 in current_answer and not (j + 1 in true_answer):
                        self.answers_false[i].append(j + 1)
                    elif not (j + 1 in current_answer) and j + 1 in true_answer:
                        self.answers_miss[i].append(j + 1)
                else:
                    if j + 1 in true_answer:
                        self.answers_miss[i].append(j + 1)

            self.obtained_true_answers += len(self.answers_true[i])
            self.obtained_false_answers += len(self.answers_false[i])
            self.obtained_miss_answers += len(self.answers_miss[i])


if __name__ == '__main__':
    app = Application(sys.argv)
    gui = ProgramGUI()

    qr = gui.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    gui.move(qr.topLeft())
    app.processEvents()

    gui.show()

    exit_val = app.exec_()

    # behaviour to trigger on exit
    sys.exit(exit_val)