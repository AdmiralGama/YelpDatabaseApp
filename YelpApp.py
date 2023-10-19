import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "YelpApp.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.StateBox.currentTextChanged.connect(self.stateChanged)
        self.ui.CityBox.itemSelectionChanged.connect(self.cityChanged)
        self.ui.ZipBox.itemSelectionChanged.connect(self.zipChanged)
        self.ui.CategoryBox.itemSelectionChanged.connect(self.categoryChanged)

    def executeQuery(self, query):
        try:
            conn = psycopg2.connect("dbname='YelpDB' user='postgres' host='localhost' password='POTestPass123!'")
        except:
            print("Unable to connect")
        
        cur = conn.cursor()
        cur.execute(query)
        #cur.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.StateBox.clear()

        sql_str = "SELECT distinct state FROM business ORDER BY state;"

        try:
            state_list = self.executeQuery(sql_str)
            
            for row in state_list:
                self.ui.StateBox.addItem(row[0])
        except:
            print("Failed to add states")

        self.stateChanged()
    
    def stateChanged(self):
        self.ui.CityBox.clear()

        state = self.ui.StateBox.currentText()
        sql_str = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER BY city;"

        try:
            city_list = self.executeQuery(sql_str)
            
            for row in city_list:
                self.ui.CityBox.addItem(row[0])
        except:
            print("Failed to add cities")

        self.ui.BusinessBox.clear()
        
        sql_str = "SELECT name, address, city, stars, review_count, reviewRating, num_checkins FROM business WHERE state = '" + state + "' ORDER BY name;"

        try:
            business_table = self.executeQuery(sql_str)

            self.ui.BusinessBox.setColumnCount(len(business_table[0]))
            self.ui.BusinessBox.setRowCount(len(business_table))

            self.ui.BusinessBox.setHorizontalHeaderLabels(['Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', '# of Checkins'])

            self.ui.BusinessBox.setColumnWidth(0, 150)
            self.ui.BusinessBox.setColumnWidth(1, 75)
            self.ui.BusinessBox.setColumnWidth(2, 50)

            currRow = 0
            
            for row in business_table:
                for column in range(len(business_table[0])):
                    self.ui.BusinessBox.setItem(currRow, column, QTableWidgetItem(str(row[column])))
                
                currRow += 1
        except:
            print("Failed to add businesses")
    
    def cityChanged(self):
        self.ui.ZipBox.clear()

        #state = self.ui.StateBox.currentText()
        city = self.ui.CityBox.selectedItems()[0].text()
        sql_str = "SELECT distinct zipcode FROM business WHERE city = '" + city + "' ORDER BY zipcode;"

        try:
            zip_list = self.executeQuery(sql_str)
            
            for row in zip_list:
                self.ui.ZipBox.addItem(row[0])
        except:
            print("Failed to add zip codes")

        self.ui.BusinessBox.clear()
        
        sql_str = "SELECT name, address, city, stars, review_count, reviewRating, num_checkins FROM business WHERE city = '" + city + "' ORDER BY name;"

        try:
            business_table = self.executeQuery(sql_str)

            self.ui.BusinessBox.setColumnCount(len(business_table[0]))
            self.ui.BusinessBox.setRowCount(len(business_table))

            self.ui.BusinessBox.setHorizontalHeaderLabels(['Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', '# of Checkins'])

            self.ui.BusinessBox.setColumnWidth(0, 150)
            self.ui.BusinessBox.setColumnWidth(1, 75)
            self.ui.BusinessBox.setColumnWidth(2, 50)

            currRow = 0
            
            for row in business_table:
                for column in range(len(business_table[0])):
                    self.ui.BusinessBox.setItem(currRow, column, QTableWidgetItem(str(row[column])))
                
                currRow += 1
        except:
            print("Failed to add businesses")

    def zipChanged(self):
        if (len(self.ui.ZipBox.selectedItems()) == 0):
            return
        
        self.ui.BusinessBox.clear()

        city = self.ui.CityBox.selectedItems()[0].text()
        zipcode = self.ui.ZipBox.selectedItems()[0].text()
        sql_str = "SELECT name, address, city, stars, review_count, reviewRating, num_checkins FROM business WHERE zipcode = '" + zipcode + "' AND city = '" + city + "' ORDER BY name;"

        try:
            business_table = self.executeQuery(sql_str)

            self.ui.BusinessBox.setColumnCount(len(business_table[0]))
            self.ui.BusinessBox.setRowCount(len(business_table))

            self.ui.BusinessBox.setHorizontalHeaderLabels(['Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', '# of Checkins'])

            self.ui.BusinessBox.setColumnWidth(0, 150)
            self.ui.BusinessBox.setColumnWidth(1, 75)
            self.ui.BusinessBox.setColumnWidth(2, 50)

            currRow = 0
            
            for row in business_table:
                for column in range(len(business_table[0])):
                    self.ui.BusinessBox.setItem(currRow, column, QTableWidgetItem(str(row[column])))
                
                currRow += 1
        except:
            print("Failed to add businesses")

        # Update categories
        self.ui.CategoryBox.clear()

        sql_str = "SELECT DISTINCT category_name FROM business NATURAL JOIN category WHERE zipcode = '" + zipcode + "' ORDER BY category_name;"
        categories = self.executeQuery(sql_str)

        for category in categories:
            self.ui.CategoryBox.addItem(category[0])
        
        # Update stats
        sql_str = "SELECT COUNT(name) FROM business WHERE zipcode = '" + zipcode + "' GROUP BY zipcode;"
        numBusinesses = self.executeQuery(sql_str)[0][0]
        self.ui.BusinessesText.setText(str(numBusinesses))

        sql_str = "SELECT population FROM zipcodedata WHERE zipcode = '" + zipcode + "';"
        population = self.executeQuery(sql_str)[0][0]
        self.ui.PopulationText.setText(str(population))
        
        sql_str = "SELECT meanIncome FROM zipcodedata WHERE zipcode = '" + zipcode + "';"
        meanIncome = self.executeQuery(sql_str)[0][0]
        self.ui.IncomeText.setText(str(meanIncome))

        self.UpdatePopularAndSuccessful()

    def UpdatePopularAndSuccessful(self):
        self.ui.PopularBox.clear()
        self.ui.SuccessfulBox.clear()

        city = self.ui.CityBox.selectedItems()[0].text()
        zipcode = self.ui.ZipBox.selectedItems()[0].text()

        #sql_str = "SELECT name, city, state FROM business WHERE zipcode = '" + zipcode + "' AND city = '" + city + "' ORDER BY name;"

        sql_str = "SELECT name, stars, reviewRating, review_count FROM business WHERE zipcode = '" + zipcode + "' AND city = '" + city + "' AND reviewrating * review_count > 240 ORDER BY name;"

        try:
            popular_table = self.executeQuery(sql_str)

            self.ui.PopularBox.setColumnCount(len(popular_table[0]))
            self.ui.PopularBox.setRowCount(len(popular_table))

            self.ui.PopularBox.setHorizontalHeaderLabels(['Name', 'Stars', 'Review Rating', '# of Reviews'])

            self.ui.PopularBox.setColumnWidth(0, 150)
            self.ui.PopularBox.setColumnWidth(1, 75)
            self.ui.PopularBox.setColumnWidth(2, 50)

            currRow = 0
            
            for row in popular_table:
                for column in range(len(popular_table[0])):
                    self.ui.PopularBox.setItem(currRow, column, QTableWidgetItem(str(row[column])))
                
                currRow += 1
        except:
            print("Failed to add popular businesses")

        sql_str = "SELECT name, review_count, num_checkins FROM business WHERE zipcode = '" + zipcode + "' AND city = '" + city + "' AND review_count + num_checkins > 320 ORDER BY name;"

        try:
            successful_table = self.executeQuery(sql_str)

            self.ui.SuccessfulBox.setColumnCount(len(successful_table[0]))
            self.ui.SuccessfulBox.setRowCount(len(successful_table))

            self.ui.SuccessfulBox.setHorizontalHeaderLabels(['Name', '# of Reviews', '# of Checkins'])

            self.ui.SuccessfulBox.setColumnWidth(0, 150)
            self.ui.SuccessfulBox.setColumnWidth(1, 75)
            self.ui.SuccessfulBox.setColumnWidth(2, 50)

            currRow = 0
            
            for row in successful_table:
                for column in range(len(successful_table[0])):
                    self.ui.SuccessfulBox.setItem(currRow, column, QTableWidgetItem(str(row[column])))
                
                currRow += 1
        except:
            print("Failed to add successful businesses")



    def categoryChanged(self):
        if (len(self.ui.CategoryBox.selectedItems()) == 0):
            return
        
        self.ui.BusinessBox.clear()

        city = self.ui.CityBox.selectedItems()[0].text()
        zipcode = self.ui.ZipBox.selectedItems()[0].text()
        category = self.ui.CategoryBox.selectedItems()[0].text()
        sql_str = "SELECT name, address, city, stars, review_count, reviewRating, num_checkins FROM business NATURAL JOIN category WHERE zipcode = '" + zipcode + "' AND city = '" + city + "' AND category_name = '" + category + "' ORDER BY name;"

        try:
            business_table = self.executeQuery(sql_str)

            self.ui.BusinessBox.setColumnCount(len(business_table[0]))
            self.ui.BusinessBox.setRowCount(len(business_table))

            self.ui.BusinessBox.setHorizontalHeaderLabels(['Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', '# of Checkins'])

            self.ui.BusinessBox.setColumnWidth(0, 150)
            self.ui.BusinessBox.setColumnWidth(1, 75)
            self.ui.BusinessBox.setColumnWidth(2, 50)

            currRow = 0
            
            for row in business_table:
                for column in range(len(business_table[0])):
                    self.ui.BusinessBox.setItem(currRow, column, QTableWidgetItem(str(row[column])))
                
                currRow += 1
        except:
            print("Failed to add category businesses")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec())