import sys, os
import pandas as pd
import matplotlib.pyplot as plt
from numpy import nan
from matplotlib.backends.backend_pdf import PdfPages
from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QStackedLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QAbstractItemView,
    QDateEdit,
    QCheckBox,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QComboBox,
    QGroupBox,
    QInputDialog,
    QFileDialog,
    QMessageBox
    )
from PySide6.QtCore import (Qt,
                            QDate,
                            Signal,
                            QObject,
                            QModelIndex,
                            QRegularExpression
                            )
from math import ceil

#Close any previously open QApplication
if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()

#DataFrames, dictionaries and lists
data = {"Caso": [],
        "Area": [],
        "Tinción": [],
        "Grosor": [],
        "Fecha": [],
        "Escaneado": [],
        "Ubicación": [],
        'Transferencia': []}

TincionList = ["H&E",
               "BA",
               "PTAU",
               "P_A_SYN",
               "FUS",
               "GFAP",
               "P_TDP43",
               "P62",
               "FastBlue",
               "CD36UV",
               'IBA1',
               'P_TDP4',
               'TMEM119',
               'HLA-DR',
               'CD68',
               'Vimentina',
               'Neurofilamento',
               'NeuN',
               'PrP',
               'BA/IBA1',
               'CD44',
               'SP37',
               'Notch2',
               'Notch3',
               ]

SBBList = [["B1", 3, "Polo frontal"],
           ["B2", 3, 'Giro frontal medio'],
           ["B3", 3, 'Giro frontal superior'],
           ["B4", 3, "Giro frontal inferior"],
           ["B5", 3, 'Superficie orbito-frontal'],
           ["B6", 3, 'Giro temporal superior y medio'],
           ["B7", 3, 'Giro temporal inferior'],
           ["B8", 3, 'Lobulo parietal inferior'],
           ["B9", 3, 'Corteza occipital'],
           ["B10", 2, 'Giro del cíngulo anterior'],
           ["B11", 2, 'Giro del cíngulo posterior'],
           ["B12", 6, 'Hipocampo'],
           ["B12.-1", 1, 'Hipocampo'],
           ["B12.-2", 1, 'Hipocampo'],
           ["B12.-3", 1, 'Hipocampo'],
           ['B13', 3, 'Núcleo amigdaloide'],
           ['B14', 3, "Área motora primaria"],
           ['B15', 3, 'Área sensitiva primaria'],
           ['B16', 3, 'Lóbulo paracentral'],
           ['B17', 3, 'Ínsula'],
           ['B18', 3, 'Precuneus'],
           ['B19', 3, 'Giro fusiforme'],
           ['B20.1', 1, "Tálamo-hipotálamo (Comisura anterior)"],
           ['B20.2', 1, "Tálamo-hipotálamo (Cuerpos Mamilares)"],
           ['B20.3', 1, "Tálamo-hipotálamo (CGL)"],
           ["B21", 1, "Glándula pineal"],
           ["B22", 1, "Hipófisis"],
           ["B23", 3, "Núcleo caudado"],
           ["B24", 3, 'Núcleo lenticular'],
           ["B25", 1, 'Cuerpo calloso'],
           ["B26", 1, "Fórnix"],
           ["B27", 3, "Sustancia blanca frontal"],
           ["B28", 1, 'Centros semiovales' ],
           ["B29", 1, 'Corona radiada'],
           ["B30", 1, 'Cápsula interna'],
           ["B31", 1, "Nervio óptico"],
           ["B32", 1, 'Nervio olfatorio'],
           ["B33", 1, "Duramadre"],
           ["B34", 1, 'Leptomeninges'],
           ["B35", 1, "Plexos coroideos"],
           ["B36", 1, "Arteria cerebral media"],
           ["B37", 1, "Arteria cerebral anterior"],
           ["B38", 1, 'Arteria cerebral posterior'],
           ["B39", 1, "Arteria lenticuloestriadas"],
           ["B40", 1, "Arteria carótida interna"],
           ["B41", 1, "Arteria basilar"],
           ["B42", 1, "Cerebelo"],
           ["B43.1", 1, "Cerebelo vermis"],
           ["B43.2", 1, "Paravermis"],
           ["B43.3", 1, "Hemisferio cerebeloso"],
           ["B43.4", 1, "Flóculo"],
           ["B44", 1, "Pedúnculo cerebeloso superior"],
           ["B45", 1, "Pedúnculo cerebeloso medio"],
           ["B46", 1, "Pedúnculo cerebeloso inferior"],
           ["B47", 3, "Mesencéfalo"],
           ["B47.M", 1, "Mesencefalo medio"],
           ["B47.I", 1, "Mesencefalo inferior"],
           ["B48", 2, "Puente"],
           ["B48.M", 1, "Puente medio"],
           ["B48.I", 1, "Puente inferior"],
           ["B49.S", 1, "Bulbo raquídeo superior"],
           ["B49.M", 1, "Bulbo raquídeo medio"],
           ["B49.I", 1, "Bulbo raquídeo inferior"],
           ["B50", 5, 'Médula espinal cérvical'],
           ["B51", 1, "Nervio facial"],
           ["B52", 1, "Nervio trigémino"],
           ["B53", 1, "Nervio raquídeo"]
    ]

ABBList = [["AB1", 1, "Núcleo subtalámico de Luys"],
           ["AB2", 1, "Núcleo accumbens septi"],
           ["AB3", 1, "Sustancia innominada"],
           ["AB4", 1, "Cuerpos mamilares"],
           ["AB5", 1, "Area premotora"],
           ["AB6", 1, "Arteria vertebral"],
           ["AB7", 1, "Otras arterias"],
           ["AB8", 1, "Nervio vestíbulo-coclear"],
           ["AB9", 1, "Nervio vago"],
           ["AB10.III", 1, "Nervio motor ocular común"],
           ["AB10.IV", 1, "Nervio troclear"],
           ["AB10.IX", 1, "Nervio glosofaríngeo"],
           ["AB10.XI", 1, "Nervio espinal"],
           ["AB10.XII", 1, "Nervio hipogloso"],
           ["AB11T", 2, "Médula torácica"],
           ["AB11L", 2, "Médula lumbar"],
           ["AB11S", 2, "Médula sacra"],
           ["AB12", 1, "Cauda equina"],
           ["AB13", 1, "Nervios periféricos"]
    ]

OBBList = [["AB14.1", 1, "Mucosa olfatoria"],
           ["AB14.2", 1, "Músculo"],
           ["AB14.3", 1, "Piel"],
           ["AB14.4", 1, "Corazón"],
           ["AB14.5", 1, "Arteria"],
           ["AB14.6", 1, "Pulmón"],
           ["AB14.7", 1, "Páncreas"],
           ["AB14.8", 1, "Riñón"],
           ["AB14.9", 1, "Bazo"],
           ["AB14.10", 1, "Hígado"],
           ["AB14.12", 1, "Glándula suprarrenal"],
           ["AB14.13", 1, "Hueso del cráneo"],
           ["AB14.14", 1, "Hueso (Otro)"],
           ["AB14.15", 1, "Tumor cerebral"],
           ["AB14.16", 1, "Tumor (Otro)"],
           ["AB14.17", 1, "Hematoma dural"],
           ["AB14.18", 1, "Abceso"],
           ["AB14.19", 1, "Tejido en estudio"],
           ["AB14.20", 1, "Estomafo"],
           ["AB14.21", 1, "Tiroides"],
           ["AB14.22", 1, "Intestino delgado"],
           ["AB14.23", 1, "Amígdala"],
           ["AB14.24", 1, "Vena"],
           ["AB14.25", 1, "Testículo"],
           ["AB14.26", 1, "Oído interno"],
           ["AB14.27", 1, "Ovario"],
           ["AB14.28", 1, "Ganglio linfático"],
           ["AB14.29", 1, "Diafragma"],
           ["AB14.30", 1, "Intestino grueso"],
           ["AB14.31", 1, "Tejido mamario"]
    ]

BBDict = dict()

def listToDict(List):

    for x in List:
        
        key = x[0]
        value = x[2]
        BBDict[f"{key}.*"] = value

listToDict(SBBList)
listToDict(ABBList)
listToDict(OBBList)



#Load dataframe or create new ones
if os.path.exists('DF1.csv'):
    DF1 = pd.read_csv('DF1.csv', index_col=False)
    DF1 = DF1.drop('Unnamed: 0', axis=1)
else:
    DF1 = pd.DataFrame(data)

#Custom signals
class updateSignal(QObject):
    updated = Signal()

class filterSignal(QObject):
    filtrar = Signal()

#Table model to visualize pandas dataframes
class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
    
    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])
            
    #Enable the removal of rows
    def removeRows(self, rows):
        self.beginRemoveRows(QtCore.QModelIndex(), rows[0], rows[-1])
        self._data.drop(self._data.index[rows[0]:rows[-1]+1], inplace=True)
        self.endRemoveRows()
    
    #Enable the sorting of rows
    def sort(self, column, order):
        if order == Qt.DescendingOrder:
            self._data.sort_values(by=self._data.columns[column], ascending=False, inplace=True)
        else:
            self._data.sort_values(by=self._data.columns[column], ascending=True, inplace=True)
        self.layoutChanged.emit()

#-----------------Classes used for the filter functions------------------------


class FilterButton(QPushButton):
    def __init__(self, key, *args, **kwargs):
        self.FilterKey = key
        super().__init__(*args, **kwargs)
        #It was necessary to create a new class to pass the value and filter parameters
        

class Filtrar(QWidget):
    def __init__(self):
        super().__init__()
        
        self.fSignal = filterSignal()
        
        self.filters = {}
        
        #Main layout
        layout1 = QVBoxLayout()
        
        #Group box settings where the filter values buttons will be
        self.groupBox = QGroupBox("Filtros")
        self.groupBoxLayout = QHBoxLayout()
        self.groupBoxLayout.setAlignment(Qt.AlignLeft)
        self.groupBox.setLayout(self.groupBoxLayout)
        
        #Filter criteria combo box settings and creation
        self.comboLayout = QHBoxLayout()
        
        self.CasoSelect = QComboBox()
        self.CasoSelect.addItems(DF1["Caso"].sort_values().unique().astype(str))
        
        self.AreaSelect = QComboBox()
        self.AreaSelect.addItems(DF1["Area"].sort_values().unique())
        
        self.TincionSelect = QComboBox()
        self.TincionSelect.addItems(DF1["Tinción"].unique())
        
        self.GrosorSelect = QComboBox()
        self.GrosorSelect.addItems(DF1["Grosor"].unique().astype(str))
        
        self.FechaSelect = QComboBox()
        self.FechaSelect.addItems(DF1["Fecha"].unique())
        
        #Filter criteria check boxes creation
        self.EscaneadoSelect = QCheckBox()
        self.EscaneadoSelect.setTristate()
        self.EscaneadoSelect.stateChanged.connect(self.emitFilter)
        
        self.UbicacionSelect = QComboBox()
        self.UbicacionSelect.addItems(DF1["Ubicación"].unique())
        
        self.TransferenciaSelect = QCheckBox()
        self.TransferenciaSelect.setTristate()
        self.TransferenciaSelect.stateChanged.connect(self.emitFilter)
        
        self.comboBoxes = {
            "Caso": self.CasoSelect,
            "Area": self.AreaSelect,
            "Tinción": self.TincionSelect,
            "Grosor": self.GrosorSelect,
            "Fecha": self.FechaSelect,
            "Ubicación": self.UbicacionSelect,
            }
        
        for label, comboBox in self.comboBoxes.items():
            comboBox.setPlaceholderText("Seleccionar")
            comboBox.setCurrentIndex(-1)
            comboBox.setEditable(True)
            comboBox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            comboBox.currentIndexChanged.connect(self.addFilter)
            
        for x in range(len(self.comboBoxes)):
            label = list(self.comboBoxes.keys())[x]
            box = self.comboBoxes[label]
            #Label Widget with the filter criteria
            LabelW = QLabel(label)
            LabelW.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            VLayout = QVBoxLayout()
            VLayout.setAlignment(Qt.AlignLeft)
            VLayout.addWidget(LabelW)
            VLayout.addWidget(box)
            self.comboLayout.addLayout(VLayout)
        
        VLayout = QVBoxLayout()
        VLayout.setAlignment(Qt.AlignLeft)
        VLayout.addWidget(QLabel("Escaneado"))
        VLayout.addWidget(self.EscaneadoSelect)
        self.comboLayout.addLayout(VLayout)
        
        VLayout = QVBoxLayout()
        VLayout.setAlignment(Qt.AlignLeft)
        VLayout.addWidget(QLabel("Transferencia"))
        VLayout.addWidget(self.TransferenciaSelect)
        self.comboLayout.addLayout(VLayout)
        
        layout1.addLayout(self.comboLayout)
        layout1.addWidget(self.groupBox)
        self.setLayout(layout1)

    #add filter runs when the combo box index is changed            
    def addFilter(self, index):
        sender = self.sender()
        filter_name = next(filter_name for filter_name, comboBox in self.comboBoxes.items() if comboBox is sender)
        filter_value = sender.currentText()

        if filter_name not in self.filters:
            self.filters[filter_name] = []
        if filter_value not in self.filters[filter_name]:
            self.filters[filter_name].append(filter_value)
            self.updateFilterButtons()
    
    #removeFilter runs when filter value button is pressed
    def removeFilter(self, filter_name, value):
        self.filters[filter_name].remove(value)
        if not self.filters[filter_name]:
            del self.filters[filter_name]
        self.updateFilterButtons()

    def updateFilterButtons(self):
        #Removing all items from the GroupBox layout
        for i in reversed(range(self.groupBoxLayout.count())):
            self.groupBoxLayout.itemAt(i).widget().setParent(None)
        
        #Add each value in the filter criteria to the GroupBox
        for filter_name, filter_values in self.filters.copy().items():
            for value in filter_values:
                button = FilterButton(f"{filter_name}", f"{value}")
                button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
                #It has to be a lambda funtion, otherwise wont work
                button.clicked.connect(lambda filter_name=filter_name, value=value: self.removeFilter(filter_name, value))
                self.groupBoxLayout.addWidget(button)
        
        self.fSignal.filtrar.emit()

    def emitFilter(self):
        self.fSignal.filtrar.emit()

#-------Classes used to add new stains----------------------------------------
class DatosGenerales(QWidget):
    def __init__(self):
        super().__init__()
        
        layout1 = QVBoxLayout()
        
        CasoHBox = QHBoxLayout()
        CasoLabel = QLabel("Número de caso:")
        CasoLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        CasoHBox.addWidget(CasoLabel)
        CasoText = QLineEdit()
        CasoText.setInputMask("00000;_")
        CasoHBox.addWidget(CasoText)
        layout1.addLayout(CasoHBox)
        
        TincionHBox = QHBoxLayout()
        TincionLabel = QLabel("Tinción:")
        TincionLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        TincionHBox.addWidget(TincionLabel)
        TincionListW = QListWidget()
        TincionListW.addItems(TincionList)
        TincionListW.setSelectionMode(QAbstractItemView.MultiSelection)
        TincionHBox.addWidget(TincionListW)
        layout1.addLayout(TincionHBox)
        
        GrosorHBox = QHBoxLayout()
        GrosorLabel = QLabel("Grosor de corte (en μ):")
        GrosorLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        GrosorHBox.addWidget(GrosorLabel)
        GrosorText = QLineEdit()
        GrosorText.setMaxLength(4)
        GrosorText.setInputMask("0000;_")
        GrosorText.setText("5")
        GrosorHBox.addWidget(GrosorText)
        layout1.addLayout(GrosorHBox)
        
        FechaHBox = QHBoxLayout()
        FechaLabel = QLabel("Fecha:")
        FechaLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        FechaHBox.addWidget(FechaLabel)
        self.NoFechaBox = QCheckBox("Desconocida")
        self.NoFechaBox.stateChanged.connect(self.NoFecha)
        FechaHBox.addWidget(self.NoFechaBox)
        self.FechaEdit = QDateEdit()
        self.FechaEdit.setCalendarPopup(True)
        self.FechaEdit.setDate(QDate.currentDate())
        self.FechaEdit.setDisplayFormat("dd/MMM/yyyy")
        FechaHBox.addWidget(self.FechaEdit)
        layout1.addLayout(FechaHBox)
        
        EscaneadoHBox = QHBoxLayout()
        EscaneadoLabel = QLabel("Escaneado:")
        EscaneadoLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        EscaneadoHBox.addWidget(EscaneadoLabel)
        EscaneadoCheck = QCheckBox()
        EscaneadoHBox.addWidget(EscaneadoCheck)
        layout1.addLayout(EscaneadoHBox)
        
        TransferenciaHBox = QHBoxLayout()
        TransferenciaLabel = QLabel("Transferencia:")
        TransferenciaLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        TransferenciaHBox.addWidget(TransferenciaLabel)
        TransferenciaCheck = QCheckBox()
        TransferenciaHBox.addWidget(TransferenciaCheck)
        layout1.addLayout(TransferenciaHBox)
        
        self.setLayout(layout1)
    
    def NoFecha(self):
        self.FechaEdit.setDisabled(self.NoFechaBox.isChecked())

class SbbWidget(QWidget):
    def __init__(self, code, area):
        super().__init__()
        
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        layout1 = QHBoxLayout()
        
        dfCheckBox = QCheckBox()
        dfCheckBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        Mod = QLineEdit()
        Mod.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        
        Cantidad = QSpinBox()
        Cantidad.setMinimum(1)
        Cantidad.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        layout1.addWidget(dfCheckBox)
        layout1.addWidget(QLabel(code), 15)
        layout1.addWidget(Mod,5)
        layout1.addWidget(QLabel(area), 70)
        layout1.addWidget(Cantidad)
        
        self.setLayout(layout1)
        
class BloquesEstandar(QWidget):
    def __init__(self, lista):
        super().__init__()
         
        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignLeft)

        self.searchBar = QLineEdit()
        self.searchBar.setClearButtonEnabled(True)
        self.searchBar.setPlaceholderText("Busqueda")
        self.searchBar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.searchBar.textChanged.connect(self.search)
        layout1.addWidget(self.searchBar)
        
        titlesHBox = QHBoxLayout()
        
        self.AddChekbox = QCheckBox("Bloques")
        self.AddChekbox.stateChanged.connect(self.CheckUncheckAll)
        titlesHBox.addWidget(self.AddChekbox, 25)
        
        titlesHBox.addWidget(QLabel("Área"), 55)
        titlesHBox.addWidget(QLabel("Cantidad"), 20)
        layout1.addLayout(titlesHBox)
        
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollWidget = QWidget()
        scrollLayout = QVBoxLayout()
        scrollLayout.setAlignment(Qt.AlignTop)
        
        for item in lista:
            for y in range(item[1]):
                
                if item[1] == 1:
                    codeLabel = item[0]
                else:
                    codeLabel = item[0] + f'.{str(y+1)}'
                
                areaLabel = item[2]
                
                scrollLayout.addWidget(SbbWidget(codeLabel, areaLabel))
        
        scrollWidget.setLayout(scrollLayout)
        scrollArea.setWidget(scrollWidget)
        layout1.addWidget(scrollArea)
        
        self.setLayout(layout1)
        
    def search(self, text):
        SbbWidgets = self.findChildren(SbbWidget)
        for widget in SbbWidgets:
           labels = widget.findChildren(QLabel)
           found = any(text.lower() in label.text().lower() for label in labels)
           widget.setVisible(found)
    
    def CheckUncheckAll(self, state):
        CheckBoxes = self.findChildren(QCheckBox)
        for checkBox in CheckBoxes:
            checkBox.setChecked(state)
            
class AddCase(QWidget):
    def __init__(self):
        super().__init__()
        
        self.uSignal = updateSignal()
        
        pageLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        self.stackLayout = QStackedLayout()
        
        AddButton = QPushButton("Añadir caso")
        AddButton.pressed.connect(self.addLaminas)
        
        pageLayout.addLayout(buttonLayout)
        pageLayout.addLayout(self.stackLayout)
        pageLayout.addWidget(AddButton)
        
        etiqueta = "Datos Generales"
        DataButton = QPushButton(etiqueta)
        DataButton.pressed.connect(self.activateDataTab)
        buttonLayout.addWidget(DataButton)
        self.stackLayout.addWidget(DatosGenerales())
        
        etiqueta = "Bloques Estándar"
        EstandarButton = QPushButton(etiqueta)
        EstandarButton.pressed.connect(self.activateEstandar)
        buttonLayout.addWidget(EstandarButton)
        self.stackLayout.addWidget(BloquesEstandar(SBBList))
        
        etiqueta = "Bloques Adicionales"
        AdicionalButton = QPushButton(etiqueta)
        AdicionalButton.pressed.connect(self.activateAdicional)
        buttonLayout.addWidget(AdicionalButton)
        self.stackLayout.addWidget(BloquesEstandar(ABBList))
       
        etiqueta = "Otros Tejidos"
        OtrosButton = QPushButton(etiqueta)
        OtrosButton.pressed.connect(self.activateOtros)
        buttonLayout.addWidget(OtrosButton)
        self.stackLayout.addWidget(BloquesEstandar(OBBList))
       
        self.setLayout(pageLayout)
        
    def activateDataTab(self):
        self.stackLayout.setCurrentIndex(0)
    
    def activateEstandar(self):
        self.stackLayout.setCurrentIndex(1)
    
    def activateAdicional(self):
        self.stackLayout.setCurrentIndex(2)
        
    def activateOtros(self):
        self.stackLayout.setCurrentIndex(3)
    
    def addLaminas(self):
        
        areaList = list()
        
        for tab in self.findChildren(BloquesEstandar):
            for sbb in tab.findChildren(SbbWidget):
                checkbox = sbb.findChildren(QCheckBox)[0]
                if checkbox.isChecked() == True:
                    mod = sbb.findChildren(QLineEdit)[0].text()
                    if mod:
                        label = f"{sbb.findChildren(QLabel)[0].text()}{mod}"
                    else:
                        label = sbb.findChildren(QLabel)[0].text()
                    times = sbb.findChildren(QSpinBox)[0].value()
                    for x in range(times):
                        areaList.append(label)
        
        newDF = pd.DataFrame(data)
        newDF["Area"] = areaList
        
        DG = self.findChildren(DatosGenerales)[0]
        newDF["Caso"] = int(DG.findChildren(QLineEdit)[0].text())
        newDF["Grosor"] = int(DG.findChildren(QLineEdit)[1].text())
        FechaUnknown = DG.findChildren(QCheckBox)[0].isChecked()
        if FechaUnknown == True:
            newDF["Fecha"] = nan
        else:
            newDF["Fecha"] = DG.findChildren(QDateEdit)[0].date().toString("dd/MMM/yyyy")
        newDF["Escaneado"] = DG.findChildren(QCheckBox)[1].isChecked()
        newDF["Transferencia"] = DG.findChildren(QCheckBox)[2].isChecked()
        
        tinciones = DG.findChildren(QListWidget)[0].selectedItems()
        
        duplicatedDF = newDF.copy()
        
        for x in range(len(tinciones)):
            if x == 0:
                newDF["Tinción"] = tinciones[x].text()
            else:
                duplicatedDF["Tinción"] = tinciones[x].text()
                newDF = pd.concat([newDF, duplicatedDF], ignore_index=True)
        
        global DF1
        
        DF1 = pd.concat([DF1, newDF], ignore_index=True)
        
        AddDoneBox = QMessageBox()
        AddDoneBox.setText("Las láminas se han añadido")
        AddDoneBox.exec()
        
        self.uSignal.updated.emit()

#---------------------Export to PDF classes-----------------------------------

class ExportPDF(QPushButton):
    def __init__(self):
        super().__init__()

        self.pressed.connect(self.exportar)

    
    def exportar (self):
        i, ok = QInputDialog.getInt(self, "Escribir información",
                                "Número de caso:"
                                )
        if ok:
            caso = i
            savePath = QFileDialog.getSaveFileName(self, "Save File",f"Informe{caso}", "PDFs (*.pdf)")[0]
            self.DFpdf = DF1[DF1["Caso"] == caso].copy()
            pages = ceil(len(self.DFpdf) / 45)
            self.DFpdf = self.DFpdf.drop(["Caso", "Escaneado", "Ubicación", "Transferencia"], axis=1)
            self.DFpdf["Area"] = self.DFpdf["Area"].replace(BBDict, regex=True)
            self.DFpdf = self.DFpdf.reset_index(drop=True)
            self.dataframe_to_pdf(self.DFpdf, f"{savePath}", numpages=(pages))
            ExpDoneBox = QMessageBox()
            ExpDoneBox.setText("El caso ha sido exportado a PDF")
            ExpDoneBox.exec()
        
    def _draw_as_table(self, df, pagesize):
        alternating_colors = [['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
        alternating_colors = alternating_colors[:len(df)]
        fig, ax = plt.subplots(figsize=pagesize)
        ax.axis('tight')
        ax.axis('off')
        the_table = ax.table(cellText=df.values,
                            cellLoc="left",
                            colWidths=[0.5, 0.25, 0.1, 0.15],
                            rowLabels=df.index + 1,
                            colLabels=df.columns,
                            rowColours=['lightblue']*len(df),
                            colColours=['lightblue']*len(df.columns),
                            cellColours=alternating_colors,
                            edges="vertical",
                            loc="center")
        return fig
      
    
    def dataframe_to_pdf(self, df, filename, numpages, pagesize=(8.5, 11)):
      with PdfPages(filename) as pdf:
        nh= numpages
        rows_per_page = 45
        for i in range(numpages):
            page = df.iloc[(i*rows_per_page):min((i+1)*rows_per_page, len(df))]
            fig = self._draw_as_table(page, pagesize)
            if nh > 1:
                # Add a part/page number at bottom-center of page
                fig.text(0.5, 0.5/pagesize[0],
                         f"Parte-{i+1} de {nh}",
                         ha='center', fontsize=8)
            pdf.savefig(fig, bbox_inches='tight')
            
            plt.close()
    

#---------------------Main Window class---------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        

        
        self.table = QTableView()


        #self.table.verticalHeader().hide()
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.table.horizontalHeader().sortIndicatorChanged.connect(self.changeOrder)
        
        self.model = TableModel(DF1)
        
        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)
        
        self.setWindowTitle('MyApp')
        
        self.addCase = AddCase()
        self.addCase.uSignal.updated.connect(self.actualizar)
        
        deleteRowsButton = QPushButton("Eliminar láminas seleccionadas")
        deleteRowsButton.clicked.connect(self.deleteSelectedRows)

        button = QPushButton("Guardar")
        button.pressed.connect(self.guardar)
        
        self.exportButton = ExportPDF()
        self.exportButton.setText("Exportar a PDF")

        layout1 = QHBoxLayout()
        
        layout1_1 = QVBoxLayout()
        
        self.filtrarWidget = Filtrar()
        self.filtrarWidget.fSignal.filtrar.connect(self.filtrar)
        layout1_1.addWidget(self.filtrarWidget)
        
        lamCant = len(DF1.index)
        self.lamLayout = QHBoxLayout()
        self.lamLayout.setAlignment(Qt.AlignLeft)
        self.lamLayout.addWidget(QLabel("Cantidad de láminas:"))
        self.cantWidget = QLabel(str(lamCant))
        self.lamLayout.addWidget(self.cantWidget)
        layout1_1.addLayout(self.lamLayout)
        
        layout1_1.addWidget(deleteRowsButton)
        layout1_1.addWidget(self.table)
        
        SaveButtonsLayout = QHBoxLayout()
        SaveButtonsLayout.addWidget(button)
        SaveButtonsLayout.addWidget(self.exportButton)
        layout1_1.addLayout(SaveButtonsLayout)
        layout1.addLayout(layout1_1, 70)
        
        layout1.addWidget(self.addCase, 30)
        
        
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)
        
        self.showMaximized()
        
    def actualizar(self):
        self.model = TableModel(DF1)
        self.table.setModel(self.model)
        
        self.filtrarWidget.CasoSelect.clear()
        self.filtrarWidget.CasoSelect.addItems(DF1["Caso"].sort_values().unique().astype(str))
        self.filtrarWidget.AreaSelect.clear()
        self.filtrarWidget.AreaSelect.addItems(DF1["Area"].sort_values().unique())
        self.filtrarWidget.TincionSelect.clear()
        self.filtrarWidget.TincionSelect.addItems(DF1["Tinción"].unique())
        self.filtrarWidget.GrosorSelect.clear()
        self.filtrarWidget.GrosorSelect.addItems(DF1["Grosor"].unique().astype(str))
        self.filtrarWidget.FechaSelect.clear()
        self.filtrarWidget.FechaSelect.addItems(DF1["Fecha"].unique())
        
    
    def filtrar(self):
        filtered_data = DF1.copy()
        
        if self.filtrarWidget.filters:
        
            for key, value in self.filtrarWidget.filters.items():
                if key in ["Caso", "Grosor"]:
                    if value:
                        value = pd.Series(value).astype("int64")
                        filtered_data = filtered_data[filtered_data[key].isin(value)]
                        
                else:
                    if value:
                        filtered_data = filtered_data[filtered_data[key].isin(value)]
            
            EscanState = self.filtrarWidget.EscaneadoSelect.checkState()
            TransState = self.filtrarWidget.TransferenciaSelect.checkState()
            
            if EscanState != Qt.Unchecked:
                if EscanState == Qt.PartiallyChecked:
                    filtered_data = filtered_data[filtered_data["Escaneado"] == False]
                else:
                    filtered_data = filtered_data[filtered_data["Escaneado"] == True]
                    
            if TransState != Qt.Unchecked:
                if TransState == Qt.PartiallyChecked:
                    filtered_data = filtered_data[filtered_data["Transferencia"] == False]
                else:
                    filtered_data = filtered_data[filtered_data["Transferencia"] == True]
    
            indexes = filtered_data.index
            
            print(filtered_data)
            
            self.cantWidget.setText(str(len(indexes)))
            
            self.model = TableModel(filtered_data)
            self.table.setModel(self.model)
        
        else:
            self.cantWidget.setText(str(len(DF1)))
            self.model = TableModel(DF1)
            self.table.setModel(self.model)

    def guardar(self):
        DF1.to_csv("DF1.csv")
        GDoneBox = QMessageBox()
        GDoneBox.setText("El archivo se ha guardado")
        GDoneBox.exec()
   
    def deleteSelectedRows(self):
        DF1.reindex(self.model._data.index)
        selectionModel = self.table.selectionModel()
        selectedRows = [index.row() for index in selectionModel.selectedRows()]
        selectedIndex = self.model._data.iloc[selectedRows].index
        self.model.removeRows(selectedRows)
        print(selectedIndex)
        if not self.model._data.equals(DF1):
            DF1.drop(selectedIndex, axis=0, inplace=True )
        self.cantWidget.setText(str(len(self.model._data)))

        DelDoneBox = QMessageBox()
        DelDoneBox.setText("Las láminas se han borrado")
        DelDoneBox.exec()
    
    def changeOrder(self, logicalIndex, order):
        self.table.sortByColumn(logicalIndex, order)
        DF1.reindex(self.model._data.index)


window = MainWindow()
window.show()

app.exec()
