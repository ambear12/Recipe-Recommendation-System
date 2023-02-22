import datetime
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import matplotlib.pyplot as plt
import numpy as np

# Read in dataset
recipes_df = pd.read_csv('recipes_w_search_terms1.csv')


# Exit the application
def exit_app():
    QCoreApplication.exit(0)


# Non-descriptive regression graph that shows meals vs cook times.
def mealsVsCookTime():
    tag_bf = 'breakfast'
    tag_lunch = 'lunch'
    tag_dinner = 'dinner'

    amnt_bf = 0
    amnt_lunch = 0
    amnt_dinner = 0

    for recipe in recipes_df['search_terms']:
        if tag_bf in recipe:
            amnt_bf += 1

        if tag_lunch in recipe:
            amnt_lunch += 1

        if tag_dinner in recipe:
            amnt_dinner += 1

    tag_15 = '15-minutes-or-less'
    tag_30 = '30-minutes-or-less'
    tag_60 = '60-minutes-or-less'

    amt_15 = 0
    amt_30 = 0
    amt_60 = 0

    for recipe in recipes_df['tags']:
        if tag_15 in recipe:
            amt_15 += 1

        if tag_30 in recipe:
            amt_30 += 1

        if tag_60 in recipe:
            amt_60 += 1

    x = np.array([amt_15, amt_30, amt_60])
    y = np.array([amnt_bf, amnt_lunch, amnt_dinner])
    a, b = np.polyfit(x, y, 1)

    my_labels = ["Breakfast", "Lunch", "Dinner"]
    lob = 'Line of best fit(linear regression)'

    plt.scatter(x, y, color='red', label=my_labels)
    plt.plot(x, a * x + b, linewidth=2, label=lob)
    plt.title('Cook Times vs Type of Meals')
    plt.xlabel('Number of Meals')
    plt.ylabel('Meal Time')
    plt.text(84105, 31198, 'Breakfast Recipes')
    plt.text(116312, 45056, 'Lunch Recipes')
    plt.text(154081, 215836, 'Dinner Recipes')

    for key, value in zip(x, y):
        label = f"({key},{value})"

        plt.annotate(label,  # this is the text
                     (key, value),  # these are the coordinates to position the label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center

    plt.legend()
    plt.show()


# Display the amount of servings per recipe and display mean
def servingsGraph():
    recipe_mean = int(recipes_df['servings'].mean())

    recipes_df.plot(x='id', y='servings', kind='scatter', title='Servings per Recipe', label='Number of servings')
    plt.plot(recipe_mean, 'o', color='red', label='Mean number of servings = 7.0')
    plt.legend(loc="upper left")
    plt.show()


# Display breakfast, lunch, dinner recipes in a pie chart.
def mealGraph():
    tag_bf = 'breakfast'
    tag_lunch = 'lunch'
    tag_dinner = 'dinner'
    tag_dessert = 'dessert'

    amnt_bf = 0
    amnt_lunch = 0
    amnt_dinner = 0
    amnt_dessert = 0

    for recipe in recipes_df['search_terms']:
        if tag_bf in recipe:
            amnt_bf += 1

        if tag_lunch in recipe:
            amnt_lunch += 1

        if tag_dinner in recipe:
            amnt_dinner += 1

        if tag_dessert in recipe:
            amnt_dessert += 1

    y = np.array([amnt_bf, amnt_lunch, amnt_dinner, amnt_dessert])
    my_labels = ["Breakfast", "Lunch", "Dinner", "Dessert"]

    plt.pie(y, labels=my_labels)
    plt.legend()
    plt.show()


# Display average cook time in a graph.
def cookGraph():
    tag_15 = '15-minutes-or-less'
    tag_30 = '30-minutes-or-less'
    tag_60 = '60-minutes-or-less'

    amt_15 = 0
    amt_30 = 0
    amt_60 = 0

    for recipe in recipes_df['tags']:
        if tag_15 in recipe:
            amt_15 += 1

        if tag_30 in recipe:
            amt_30 += 1

        if tag_60 in recipe:
            amt_60 += 1

    y = np.array([amt_15, amt_30, amt_60])
    my_labels = ["15 minutes or less", "30 minutes or less", "60 minutes or less"]

    plt.bar(my_labels, y)
    plt.title('Cook Times per Recipe')
    plt.xlabel('Cook Time')
    plt.ylabel('Number of Recipes')
    plt.show()


# This class contains the contents of the recipe recommendation program.
class Ui_RecipeGenerator(object):

    # Recommender system that gets recipe from the dataset and displays in a table.
    def get_recipe(self):
        row_count = 0
        self.recipe_table.clearContents()
        self.recipe_table.setRowCount(0)

        try:
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', None)

            recipe_dict = dict(zip(recipes_df['id'], recipes_df['ingredients']))
            user_ingredients = self.user_input_box.toPlainText()
            user_list = user_ingredients.split(",")

            # Validate user input
            if user_ingredients.strip().isdigit():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Input can only contain letters.')
                msg.setWindowTitle("Error")
                msg.exec_()
                raise TypeError

            if len(user_list) <= 1:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Your list must contain more than one ingredient.')
                msg.setWindowTitle("Error")
                msg.exec_()
                return

            for key, value in recipe_dict.items():
                if all(ingredients in value for ingredients in user_list):
                    value = key
                    r_name = recipes_df.query('id == @value')['name']
                    r_description = recipes_df.query('id == @value')['description']
                    r_ing = recipes_df.query('id == @value')['ingredients_raw_str']
                    r_servings = recipes_df.query('id == @value')['servings']
                    r_steps = recipes_df.query('id == @value')['steps']

                    r_name1 = r_name.to_string()
                    r_description1 = r_description.to_string()
                    r_ing1 = r_ing.to_string()
                    r_servings1 = r_servings.to_string()
                    r_steps1 = r_steps.to_string()

                    row_position = self.recipe_table.rowCount()
                    self.recipe_table.insertRow(row_position)
                    num_cols = self.recipe_table.colorCount()
                    num_rows = self.recipe_table.rowCount()
                    self.recipe_table.setRowCount(num_rows)
                    self.recipe_table.setColumnCount(num_cols)

                    row_count += 1

                    self.recipe_table.setItem(num_rows - 1, 0, QTableWidgetItem(r_name1))
                    self.recipe_table.setItem(num_rows - 1, 1, QTableWidgetItem(r_description1))
                    self.recipe_table.setItem(num_rows - 1, 2, QTableWidgetItem(r_ing1))
                    self.recipe_table.setItem(num_rows - 1, 3, QTableWidgetItem(r_servings1))
                    self.recipe_table.setItem(num_rows - 1, 4, QTableWidgetItem(r_steps1))
                    self.recipe_table.setColumnCount(5)

            if row_count == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText("Couldn't find any recipes.\nTry another query.")
                msg.setWindowTitle("No Recipe Found")
                msg.exec_()

                return
        # Log file used to track invalid input and errors. This monitors and maintains the product.
        except TypeError as e:
            f = open('log.txt', 'w')
            f.write('TypeError exception occurred at: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            f.close()

    # All functions below are used to set up the GUI.
    def setupUi(self, RecipeGenerator):
        RecipeGenerator.setObjectName("RecipeGenerator")
        RecipeGenerator.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(RecipeGenerator)
        self.centralwidget.setObjectName("centralwidget")
        self.welcome_label = QtWidgets.QLabel(self.centralwidget)
        self.welcome_label.setGeometry(QtCore.QRect(230, 0, 361, 101))
        font = QtGui.QFont()
        font.setFamily("Modern")
        font.setPointSize(25)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.welcome_label.setFont(font)
        self.welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        self.welcome_label.setObjectName("welcome_label")

        self.generate_button = QtWidgets.QPushButton(self.centralwidget)
        self.generate_button.setGeometry(QtCore.QRect(620, 100, 93, 28))
        self.generate_button.setObjectName("generate_button")
        self.generate_button.clicked.connect(self.get_recipe)

        self.user_input_box = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.user_input_box.setGeometry(QtCore.QRect(220, 100, 381, 31))
        self.user_input_box.setPlainText("")
        self.user_input_box.setObjectName("user_input_box")

        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(640, 430, 93, 28))
        self.exit_button.setObjectName("exit_button")
        self.exit_button.clicked.connect(exit_app)

        # Data visual buttons
        self.servings_button = QtWidgets.QPushButton(self.centralwidget)
        self.servings_button.setGeometry(QtCore.QRect(500, 430, 93, 28))
        self.servings_button.setObjectName("servings_button")
        self.servings_button.clicked.connect(servingsGraph)

        self.meal_button = QtWidgets.QPushButton(self.centralwidget)
        self.meal_button.setGeometry(QtCore.QRect(400, 430, 93, 28))
        self.meal_button.setObjectName("meal_button")
        self.meal_button.clicked.connect(mealGraph)

        self.time_button = QtWidgets.QPushButton(self.centralwidget)
        self.time_button.setGeometry(QtCore.QRect(300, 430, 98, 28))
        self.time_button.setObjectName("time_button")
        self.time_button.clicked.connect(cookGraph)

        self.regression_button = QtWidgets.QPushButton(self.centralwidget)
        self.regression_button.setGeometry(QtCore.QRect(150, 430, 150, 28))
        self.regression_button.setObjectName("regression_button")
        self.regression_button.clicked.connect(mealsVsCookTime)

        self.instruction_label = QtWidgets.QLabel(self.centralwidget)
        self.instruction_label.setGeometry(QtCore.QRect(20, 440, 121, 31))

        font = QtGui.QFont()
        font.setPointSize(11)
        self.instruction_label.setFont(font)
        self.instruction_label.setObjectName("instruction_label")

        self.step1_label = QtWidgets.QLabel(self.centralwidget)
        self.step1_label.setGeometry(QtCore.QRect(20, 470, 681, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.step1_label.setFont(font)
        self.step1_label.setObjectName("step1_label")

        self.step2_label = QtWidgets.QLabel(self.centralwidget)
        self.step2_label.setGeometry(QtCore.QRect(20, 510, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.step2_label.setFont(font)
        self.step2_label.setObjectName("step2_label")

        self.step3_label = QtWidgets.QLabel(self.centralwidget)
        self.step3_label.setGeometry(QtCore.QRect(20, 530, 331, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.step3_label.setFont(font)
        self.step3_label.setObjectName("step3_label")

        self.recipe_table = QtWidgets.QTableWidget(self.centralwidget)
        self.recipe_table.setGeometry(QtCore.QRect(50, 140, 711, 271))

        font = QtGui.QFont()
        font.setPointSize(10)
        self.recipe_table.setFont(font)
        self.recipe_table.setObjectName("recipe_table")
        self.recipe_table.setColumnCount(5)
        self.recipe_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.recipe_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.recipe_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.recipe_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.recipe_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.recipe_table.setHorizontalHeaderItem(4, item)
        RecipeGenerator.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(RecipeGenerator)
        self.statusbar.setObjectName("statusbar")
        RecipeGenerator.setStatusBar(self.statusbar)

        self.retranslateUi(RecipeGenerator)
        QtCore.QMetaObject.connectSlotsByName(RecipeGenerator)

    def retranslateUi(self, RecipeGenerator):
        _translate = QtCore.QCoreApplication.translate
        RecipeGenerator.setWindowTitle(_translate("RecipeGenerator", "MainWindow"))
        self.welcome_label.setText(_translate("RecipeGenerator", "Let\'s Get Cooking!"))
        self.generate_button.setText(_translate("RecipeGenerator", "Cook!"))
        self.exit_button.setText(_translate("RecipeGenerator", "Exit"))
        self.servings_button.setText(_translate("RecipeGenerator", "Serving Data"))
        self.meal_button.setText(_translate("RecipeGenerator", "Meal Data"))
        self.time_button.setText(_translate("RecipeGenerator", "Cook Time Data"))
        self.regression_button.setText(_translate("RecipeGenerator", "Non-descriptive Data"))

        self.instruction_label.setText(_translate("RecipeGenerator", "Instructions:"))
        self.step1_label.setText(_translate("RecipeGenerator",
                                            "1. Type your ingredients in a comma separated list. No spaces."
                                            " (ex. butter,prawns,shallots)"))
        self.step2_label.setText(_translate("RecipeGenerator", "2. Click the \'cook\' button."))
        self.step3_label.setText(_translate("RecipeGenerator", "3. Wait for results and enjoy!"))
        item = self.recipe_table.horizontalHeaderItem(0)
        item.setText(_translate("RecipeGenerator", "Name"))
        item = self.recipe_table.horizontalHeaderItem(1)
        item.setText(_translate("RecipeGenerator", "Description"))
        item = self.recipe_table.horizontalHeaderItem(2)
        item.setText(_translate("RecipeGenerator", "Ingredients"))
        item = self.recipe_table.horizontalHeaderItem(3)
        item.setText(_translate("RecipeGenerator", "Servings"))
        item = self.recipe_table.horizontalHeaderItem(4)
        item.setText(_translate("RecipeGenerator", "Steps"))


# Shows the recipe GUI.
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    RecipeGenerator = QtWidgets.QMainWindow()
    ui = Ui_RecipeGenerator()
    ui.setupUi(RecipeGenerator)
    RecipeGenerator.show()
    sys.exit(app.exec_())
