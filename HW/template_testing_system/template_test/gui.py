import json
import argparse
import sys

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication as Application, QWidget, QPushButton as Button, QFileDialog, QComboBox
from PyQt5.QtWidgets import QLabel as Label, QGridLayout, QDesktopWidget, QSlider

import design_lbl

class ProgramGUI(QtWidgets.QMainWindow, design_lbl.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.filename = "task.json"
        self.load_questions()
        self.label_title.setText(f'Тестирующая система. \n Задание {self.task_number}')
        self.current_ind = 0
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.n_questions - 1)
        for i in range(self.n_questions):
            self.comboBox.addItem(f'question {str(i + 1)}')

        self.n_answered = 0
        self.is_finish = False
        self.answer_log = {}
        self.dict_label_answer = {1: self.label_answer1, 2: self.label_answer2,
                                  3: self.label_answer3, 4: self.label_answer4}

        self.dict_checkbox = {1: self.checkBox_1, 2: self.checkBox_2,
                              3: self.checkBox_3, 4: self.checkBox_4}

        self.set_question()
        self.set_progress()

        self.comboBox.activated.connect(self.change_question)
        self.slider.valueChanged.connect(self.change_question)
        self.button_answer.clicked.connect(self.push_answer_button)
        self.button_finish.clicked.connect(self.push_finish_button)

    def set_progress(self):
        if self.is_finish:
            self.label_progress.setText(f'Правильных ответов: {str(self.obtained_true_answers)}' +
                                        f'/{str(self.max_true_answers)}' + '\n' +
                                        f'Неправильных ответов: {str(self.obtained_false_answers)}' + '\n' +
                                        f'Пропущенных ответов: {str(self.obtained_missed_answers)}')
        else:
            self.label_progress.setText(f'Ваш прогресс: {str(len(self.answer_log))}/{str(self.n_questions)}')



    def change_question(self):
        combobox_current_index = self.comboBox.currentIndex()
        slider_current_index = self.slider.value()
        if combobox_current_index != self.current_ind:
            current_ind = combobox_current_index
            self.slider.setValue(current_ind)
        elif slider_current_index != self.current_ind:
            current_ind = slider_current_index
            self.comboBox.setCurrentIndex(current_ind)

        self.current_ind = current_ind
        self.set_question()

    def load_questions(self):
        with open(self.filename, encoding='utf-8') as file:
            data = json.load(file)
            self.task_number = data["task_number"]
            self.questions_all = data['questions_all']
            self.n_questions = len(self.questions_all)

    def set_text(self, label, text):
        words = text.split()

        cur_len = 0
        for ind, el in enumerate(words):
            cur_len += len(el) + 1
            if cur_len >= 60:
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
            current_checkbox.hide()
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
        self.check_true_answers()
        self.is_finish = True
        self.set_progress()
        self.set_question()

    def check_true_answers(self):
        self.answers_true = {}
        self.answers_false = {}
        self.max_true_answers = 0
        self.obtained_true_answers = 0
        self.obtained_false_answers = 0
        self.real_true_answer = {}

        for i in range(self.n_questions):
            self.answers_true[i] = []
            self.answers_false[i] = []
            current_question = self.questions_all[i]
            true_answer = current_question["true_answer"]
            current_answer = self.answer_log.get(i)
            self.real_true_answer[i] = true_answer
            self.max_true_answers += len(true_answer)

            if not (current_answer is None):
                for el in true_answer:
                    if el in current_answer:
                        self.answers_true[i].append(el)

            if not (current_answer is None):
                for el in current_answer:
                    if el in true_answer:
                        self.answers_true[i].append(el)
                    else:
                        self.answers_false[i].append(el)

            self.answers_true[i] = set(self.answers_true[i])
            self.answers_false[i] = set(self.answers_false[i])
            self.obtained_true_answers += len(self.answers_true[i])
            self.obtained_false_answers += len(self.answers_false[i])
            self.obtained_missed_answers = self.max_true_answers - \
                                           self.obtained_true_answers - self.obtained_false_answers


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