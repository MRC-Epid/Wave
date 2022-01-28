from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
        QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
        QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
        QWidget)


VARIABLE, EXAMPLE, DESCRIPTION = range(3)
ERROR = 'Code'

# Work around the fact that QSortFilterProxyModel always filters datetime
# values in QtCore.Qt.ISODate format, but the tree views display using
# QtCore.Qt.DefaultLocaleShortDate format.
class SortFilterProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, sourceRow, sourceParent):
        # Do we filter for the date column?
        if self.filterKeyColumn() == ERROR:
            # Fetch datetime value.
            index = self.sourceModel().index(sourceRow, DESCRIPTION, sourceParent)
            data = self.sourceModel().data(index)

            # Return, if regExp match in displayed format.
            return (self.filterRegExp().indexIn(data.toString(Qt.DefaultLocaleShortDate)) >= 0)

        # Not our business.
        return super(SortFilterProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)


class DataDictionaryWindow(QWidget):
    def __init__(self):
        super(DataDictionaryWindow, self).__init__()

        self.proxyModel = SortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)

        self.sourceGroupBox = QGroupBox("Data Dictionary")
        self.proxyGroupBox = QGroupBox("Sorted/Filtered Data Dictionary")

        self.sourceView = QTreeView()
        self.sourceView.setRootIsDecorated(False)
        self.sourceView.setAlternatingRowColors(True)

        self.proxyView = QTreeView()
        self.proxyView.setRootIsDecorated(False)
        self.proxyView.setAlternatingRowColors(True)
        self.proxyView.setModel(self.proxyModel)
        self.proxyView.setSortingEnabled(True)

        self.sortCaseSensitivityCheckBox = QCheckBox("Case sensitive sorting")
        self.filterCaseSensitivityCheckBox = QCheckBox("Case sensitive filter")

        self.filterPatternLineEdit = QLineEdit()
        self.filterPatternLabel = QLabel("&Filter pattern:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)

        self.filterSyntaxComboBox = QComboBox()
        self.filterSyntaxComboBox.addItem("Fixed string", QRegExp.FixedString)
        self.filterSyntaxComboBox.addItem("Regular expression", QRegExp.RegExp)
        self.filterSyntaxComboBox.addItem("Wildcard", QRegExp.Wildcard)
        self.filterSyntaxLabel = QLabel("Filter &syntax:")
        self.filterSyntaxLabel.setBuddy(self.filterSyntaxComboBox)

        self.filterColumnComboBox = QComboBox()
        self.filterColumnComboBox.addItem("Variable")
        self.filterColumnComboBox.addItem("Example")
        self.filterColumnComboBox.addItem("Description")
        self.filterColumnLabel = QLabel("Filter &column:")
        self.filterColumnLabel.setBuddy(self.filterColumnComboBox)

        self.filterPatternLineEdit.textChanged.connect(self.filterRegExpChanged)
        self.filterSyntaxComboBox.currentIndexChanged.connect(self.filterRegExpChanged)
        self.filterColumnComboBox.currentIndexChanged.connect(self.filterColumnChanged)
        self.filterCaseSensitivityCheckBox.toggled.connect(self.filterRegExpChanged)
        self.sortCaseSensitivityCheckBox.toggled.connect(self.sortChanged)

        sourceLayout = QHBoxLayout()
        sourceLayout.addWidget(self.sourceView)
        self.sourceGroupBox.setLayout(sourceLayout)

        proxyLayout = QGridLayout()
        proxyLayout.addWidget(self.proxyView, 0, 0, 1, 3)
        proxyLayout.addWidget(self.filterPatternLabel, 1, 0)
        proxyLayout.addWidget(self.filterPatternLineEdit, 1, 1, 1, 2)
        proxyLayout.addWidget(self.filterSyntaxLabel, 2, 0)
        proxyLayout.addWidget(self.filterSyntaxComboBox, 2, 1, 1, 2)
        proxyLayout.addWidget(self.filterColumnLabel, 3, 0)
        proxyLayout.addWidget(self.filterColumnComboBox, 3, 1, 1, 2)
        proxyLayout.addWidget(self.filterCaseSensitivityCheckBox, 4, 0, 1, 2)
        proxyLayout.addWidget(self.sortCaseSensitivityCheckBox, 4, 2)
        self.proxyGroupBox.setLayout(proxyLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.sourceGroupBox)
        mainLayout.addWidget(self.proxyGroupBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Data Dictionary")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Logo.svg"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.resize(500, 450)

        self.proxyView.sortByColumn(VARIABLE, Qt.AscendingOrder)
        self.filterColumnComboBox.setCurrentIndex(VARIABLE)

        self.filterPatternLineEdit.setText("")
        self.filterCaseSensitivityCheckBox.setChecked(True)
        self.sortCaseSensitivityCheckBox.setChecked(True)

    def setSourceModel(self, model):
        self.proxyModel.setSourceModel(model)
        self.sourceView.setModel(model)

    def filterRegExpChanged(self):
        syntax_nr = self.filterSyntaxComboBox.itemData(self.filterSyntaxComboBox.currentIndex())
        syntax = QRegExp.PatternSyntax(syntax_nr)

        if self.filterCaseSensitivityCheckBox.isChecked():
            caseSensitivity = Qt.CaseSensitive
        else:
            caseSensitivity = Qt.CaseInsensitive

        regExp = QRegExp(self.filterPatternLineEdit.text(),
                caseSensitivity, syntax)
        self.proxyModel.setFilterRegExp(regExp)

    def filterColumnChanged(self):
        self.proxyModel.setFilterKeyColumn(self.filterColumnComboBox.currentIndex())

    def sortChanged(self):
        if self.sortCaseSensitivityCheckBox.isChecked():
            caseSensitivity = Qt.CaseSensitive
        else:
            caseSensitivity = Qt.CaseInsensitive

        self.proxyModel.setSortCaseSensitivity(caseSensitivity)


def addDictionary(model, variable, example, description):
    model.insertRow(0)
    model.setData(model.index(0, VARIABLE), variable)
    model.setData(model.index(0, EXAMPLE), example)
    model.setData(model.index(0, DESCRIPTION), description)


def createDictionaryModel(parent):
    model = QStandardItemModel(0, 3, parent)

    model.setHeaderData(VARIABLE, Qt.Horizontal, "Variable")
    model.setHeaderData(EXAMPLE, Qt.Horizontal, "Example")
    model.setHeaderData(DESCRIPTION, Qt.Horizontal, "Description")

    addDictionary(model, "id", "247290", "Unique file identifier (from job file)")
    addDictionary(model, "device", "43726", "Device serial number")
    addDictionary(model, "file_duration", "1206282.33468627", "Length of file recording including non-wear time (seconds) ")
    addDictionary(model, "file_filename", "43726_0000247290.cwa", "Filename from metadata")
    addDictionary(model, "file_header_size", "1024", "Size of header (bytes)")
    addDictionary(model, "file_mean_rate", "98.6830666230049", "Mean sampling frequency across file (Hz)")
    addDictionary(model, "file_num_samples", "119039640", "Number of samples in raw file")
    addDictionary(model, "file_num_sectors", "991997", "Number of sectors")
    addDictionary(model, "file_samples_per_sector", "120", "Expected number of samples per sector")
    addDictionary(model, "file_sector_size", "512", "Size of sector (bytes)")
    addDictionary(model, "file_size", "507903488", "Size of file (byte)")
    addDictionary(model, "firmware_revision", "45", "Firmware revision number")
    addDictionary(model, "first_battery", "175", "First recorded battery level (unformatted)")
    addDictionary(model, "first_light", "218", "First light reading in file (unformatted)")
    addDictionary(model, "first_sample_count", "120", "Number of samples in first sector of data")
    addDictionary(model, "first_samples_per_sector", "120", "Number of samples expected in first sector of data")
    addDictionary(model, "first_sequence_id", "0", "Recording session ID from first sector")
    addDictionary(model, "first_session_id", "247290", "First sector number (starting at 0)")
    addDictionary(model, "first_temperature", "233", "First temperature reading in file (unformatted)")
    addDictionary(model, "first_timestamp", "1527152406.07196", "First date timestamp recorded (unformatted)")
    addDictionary(model, "first_timestamp_offset", "125", "First timestamp offset allowing for fractions of a second")
    addDictionary(model, "first_timestamp_time", "24/05/2018 10:00:06:071",
            "First date timestamp formatted and adjusted for time offset")
    addDictionary(model, "last_battery", "118", "Last recorded battery level (unformatted)")
    addDictionary(model, "last_change", "1527076553",
            "Last change time when monitor had a change within software (unformatted)")
    addDictionary(model, "last_change_time", "23/05/2018 12:55:53:000",
            "Last change date timestamp when monitor had a change within software")
    addDictionary(model, "last_light", "216", "Last light reading in file (unformatted)")
    addDictionary(model, "last_sample_count", "120", "Number of samples in last sector of data")
    addDictionary(model, "last_samples_per_sector", "120", "Number of samples expected in last sector of data")
    addDictionary(model, "last_sequence_id", "991996", "Recording session ID from last sector")
    addDictionary(model, "last_session_id", "247290", "Last sector number")
    addDictionary(model, "last_temperature", "248", "Last temperature reading in file (unformatted)")
    addDictionary(model, "last_timestamp", "1528358688.40664", "Last date timestamp recorded (unformatted)")
    addDictionary(model, "last_timestamp_offset", "130", "Last timestamp offset allowing for fractions of a second")
    addDictionary(model, "last_timestamp_time", "07/06/2018 09:04:48:406",
            "Last date timestamp formatted and adjusted for time offset")
    addDictionary(model, "num_pages", "991997", "Number of pages of data")
    addDictionary(model, "packet_length", "1020", "Size of the header block minus header identifier (bytes)")
    addDictionary(model, "QC_anomaly_A", "0", "Number of anomaly A's within file")
    addDictionary(model, "QC_anomaly_B", "0", "Number of anomaly B's within file")
    addDictionary(model, "QC_anomaly_C", "0", "Number of anomaly C's within file")
    addDictionary(model, "QC_anomaly_D", "0", "Number of anomaly D's within file")
    addDictionary(model, "QC_anomaly_E", "0", "Number of anomaly E's within file")
    addDictionary(model, "QC_anomaly_F", "0", "Number of anomaly F's within file")
    addDictionary(model, "QC_anomaly_G", "0", "Number of anomaly G's within file")
    addDictionary(model, "QC_first_battery_pct", "82.86", "QC first battery percentage")
    addDictionary(model, "QC_last_battery_pct", "56.19", "QC last battery percentage")
    addDictionary(model, "analysis_resolutions", "['1m', '1h']", "List of the time resolutions of the generated results")
    addDictionary(model, "approximate_frequency", "96.31127805065969",
            "Approximate sampling frequency of the file derived from the difference between the first and last timestamps (Hz)")
    addDictionary(model, "budget", "1000", "The number of regression iterations performed to derive the calibration factors ")
    addDictionary(model, "calibration_method", "offset and scale", "Calibration method applied to file")
    addDictionary(model, "end_error", "4.11175191788165", "Error post-calibration (mg)")
    addDictionary(model, "generic_first_timestamp", "14/10/2016 13:00:04:656250", "First date timestamp of raw data")
    addDictionary(model, "generic_last_timestamp", "24/10/2016 13:29:33:028223", "Last date timestamp of raw data")
    addDictionary(model, "generic_loading_time_seconds", "504.458782", "Time taken to load the file (seconds)")
    addDictionary(model, "generic_num_channels", "7", "Number of data channels generated during the data loading process")
    addDictionary(model, "generic_num_samples", "83384280", "Number of samples of x,y,z in the file")
    addDictionary(model, "generic_processing_timestamp", "12/09/2019 17:16:49:098841", "Date timestamp when file was loaded")
    addDictionary(model, "noise_cutoff_mg", "13", "Threshold set for still bout detection (mg)")
    addDictionary(model, "num_final_bouts", "864", "The number of bouts where the data is deemed both reasonable and still")
    addDictionary(model, "num_final_seconds", "434850", "The number of seconds contained in the final bouts")
    addDictionary(model, "num_reasonable_bouts", "231", "Total number of bouts where the monitor was still")
    addDictionary(model, "num_reasonable_seconds", "861750", "Total number of seconds when the monitor was still")
    addDictionary(model, "num_samples", "83384280", "Number of samples of x,y,z in the file")
    addDictionary(model, "num_still_bouts", "864", "Total number of bouts considered reasonable (VM between 0.5 and 1.5g)")
    addDictionary(model, "num_still_seconds", "434850",
            "Total number of seconds within reasonable bouts (VM between 0.5 and 1.5g)")
    addDictionary(model, "processed_file", "43726_0000247290.cwa", "Filename of processed file")
    addDictionary(model, "processing_epoch", "5", "Processing epoch (seconds)")
    addDictionary(model, "processing_script", "WAP_one_step_process v.1.0 16/09/2019",
            "Version of script used for processing")
    addDictionary(model, "QC_anomalies_total", "0", "Total number of anomalies in the raw file")
    addDictionary(model, "start_error", "10.6469242556552", "Error pre-calibration (mg)")
    addDictionary(model, "x_offset", ".0282087606637703", "Offset correction factor of x-axis from calibration process (mg)")
    addDictionary(model, "x_scale", ".99261599824194", "Scale factor of x-axis from calibration process (mg)")
    addDictionary(model, "x_temp_offset", "0",
            "Temperature-scaled offset correction factor of x-axis from calibration process (mg)")
    addDictionary(model, "y_offset", ".0559210951949475", "Offset correction factor of y-axis from calibration process (mg)")
    addDictionary(model, "y_scale", "1.0063328761166", "Scale factor of y-axis from calibration process (mg)")
    addDictionary(model, "y_temp_offset", "0",
            "Temperature-scaled offset correction factor of y-axis from calibration process (mg)")
    addDictionary(model, "z_offset", ".0735302496095458", "Offset correction factor of z-axis from calibration process (mg)")
    addDictionary(model, "z_scale", "1.01978705208691", "Scale factor of z-axis from calibration process (mg)")
    addDictionary(model, "z_temp_offset", "0",
            "Temperature-scaled offset correction factor of z-axis from calibration process (mg)")
    addDictionary(model, "body_location", "left wrist", "Location of device on the body during wear (-1 = missing)")
    addDictionary(model, "end_time", "-1", "End time (if NOT delayed start)")
    addDictionary(model, "exercise_code", "fl", "Exercise type entered during initialisation (-1 = missing)")
    addDictionary(model, "frequency", "100", "Recording frequency selected entered during initialisation (Hz)")
    addDictionary(model, "handedness", "right", "Handedness of participant entered during initialisation (-1 = missing)")
    addDictionary(model, "height", "156",
            "Height of participant (unit dependent on input during initialisation) (-1 = missing)")
    addDictionary(model, "investigator", "SB", "Study investigator entered during initialisation (-1 = missing)")
    addDictionary(model, "logging_end", "1528362000", "Date timestamp of preset end time (unformatted) (-1 = missing)")
    addDictionary(model, "logging_end_time", "07/06/2018 10:00:00:000", "Date timestamp of preset end time (-1 = missing)")
    addDictionary(model, "logging_start", "1527152400", "Date timestamp of preset start time (unformatted) (-1 = missing)")
    addDictionary(model, "logging_start_time", "24/05/2018 10:00:00:000",
            "Date timestamp of preset start time (-1 = missing)")
    addDictionary(model, "sample_range", "8", "Sampling range selected during initialisation (g)")
    addDictionary(model, "session_id", "247290", "Recording session ID entered during initialisation")
    addDictionary(model, "setup_operator", "lmg48", "Operator ID entered during initialisation (-1 = missing)")
    addDictionary(model, "sex", "female", "Sex of participant entered during initialisation (-1 = missing)")
    addDictionary(model, "start_time", "-1", "Start time (if NOT delayed start) (-1 = missing)")
    addDictionary(model, "study_centre", "MRC", "Study centre entered during initialisation (-1 = missing)")
    addDictionary(model, "study_code", "Study1", "Study code entered during initialisation (-1 = missing)")
    addDictionary(model, "study_notes", "Study-specific notes",
            "Notes about the study made during initialisation (-1 = missing)")
    addDictionary(model, "subject_code", "247290", "Participant ID entered during initialisation (-1 = missing)")
    addDictionary(model, "subject_notes", "Subject-specific notes",
            "Notes about the subject made during initialisation (-1 = missing)")
    addDictionary(model, "weight", "48",
            "Weight of participant (unit dependent on input during initialisation) (-1 = missing)")
    addDictionary(model, "std_temperature", "2.48165361343083", "Standard Deviation of temperature values (specific to AX3)")
    addDictionary(model, "max_temperature", "38.6756519191327", "Maximum temperature value  (specific to AX3)")
    addDictionary(model, "mean_temperature", "33.8320733881855", "Mean temperature value  (specific to AX3)")
    addDictionary(model, "min_temperature", "24.3187811309698", "Minimum temperature value  (specific to AX3)")
    addDictionary(model, "timestamp", "07/06/2019 16:00:00:000000",
                  "Timestamp of data point (DD/MM/YYYY HH:MM:SS.ssssss)")
    addDictionary(model, "ENMO_mean", "30.7476212451816", "Mean ENMO for the given timeframe (mg)")
    addDictionary(model, "ENMO_n", "720",
                  "Epoch level count of how many ENMO data points are present within the given timeframe")
    addDictionary(model, "ENMO_missing", "0",
                  "Epoch level count of how many ENMO data points include non-wear within the given timeframe")
    addDictionary(model, "ENMO_sum", "22138.2872965307", "Total amount of ENMO/HPFVM for that given timeframe (mg)")
    addDictionary(model, "ENMO_0_99999", "719",
                  "Count of number of epochs above ENMO 0mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_1_99999", "505",
                  "Count of number of epochs above ENMO 1mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_2_99999", "495",
                  "Count of number of epochs above ENMO 2mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_3_99999", "486",
                  "Count of number of epochs above ENMO 3mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_4_99999", "477",
                  "Count of number of epochs above ENMO 4mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_5_99999", "474",
                  "Count of number of epochs above ENMO 5mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_10_99999", "434",
                  "Count of number of epochs above ENMO 10mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_15_99999", "368",
                  "Count of number of epochs above ENMO 15mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_20_99999", "306",
                  "Count of number of epochs above ENMO 20mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_25_99999", "236",
                  "Count of number of epochs above ENMO 25mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_30_99999", "195",
                  "Count of number of epochs above ENMO 30mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_35_99999", "163",
                  "Count of number of epochs above ENMO 35mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_40_99999", "146",
                  "Count of number of epochs above ENMO 40mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_45_99999", "123",
                  "Count of number of epochs above ENMO 45mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_50_99999", "110",
                  "Count of number of epochs above ENMO 50mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_55_99999", "104",
                  "Count of number of epochs above ENMO 55mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_60_99999", "101",
                  "Count of number of epochs above ENMO 60mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_65_99999", "99",
                  "Count of number of epochs above ENMO 65mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_70_99999", "93",
                  "Count of number of epochs above ENMO 70mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_75_99999", "86",
                  "Count of number of epochs above ENMO 75mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_80_99999", "83",
                  "Count of number of epochs above ENMO 80mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_85_99999", "80",
                  "Count of number of epochs above ENMO 85mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_90_99999", "76",
                  "Count of number of epochs above ENMO 90mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_95_99999", "73",
                  "Count of number of epochs above ENMO 95mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_100_99999", "71",
                  "Count of number of epochs above ENMO 100mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_105_99999", "65",
                  "Count of number of epochs above ENMO 105mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_110_99999", "64",
                  "Count of number of epochs above ENMO 110mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_115_99999", "59",
                  "Count of number of epochs above ENMO 115mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_120_99999", "58",
                  "Count of number of epochs above ENMO 120mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_125_99999", "57",
                  "Count of number of epochs above ENMO 125mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_130_99999", "53",
                  "Count of number of epochs above ENMO 130mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_135_99999", "48",
                  "Count of number of epochs above ENMO 135mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_140_99999", "42",
                  "Count of number of epochs above ENMO 140mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_145_99999", "37",
                  "Count of number of epochs above ENMO 145mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_150_99999", "30",
                  "Count of number of epochs above ENMO 150mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_160_99999", "23",
                  "Count of number of epochs above ENMO 160mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_170_99999", "18",
                  "Count of number of epochs above ENMO 170mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_180_99999", "16",
                  "Count of number of epochs above ENMO 180mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_190_99999", "9",
                  "Count of number of epochs above ENMO 190mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_200_99999", "7",
                  "Count of number of epochs above ENMO 200mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_210_99999", "7",
                  "Count of number of epochs above ENMO 210mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_220_99999", "6",
                  "Count of number of epochs above ENMO 220mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_230_99999", "5",
                  "Count of number of epochs above ENMO 230mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_240_99999", "5",
                  "Count of number of epochs above ENMO 240mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_250_99999", "5",
                  "Count of number of epochs above ENMO 250mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_260_99999", "5",
                  "Count of number of epochs above ENMO 260mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_270_99999", "4",
                  "Count of number of epochs above ENMO 270mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_280_99999", "3",
                  "Count of number of epochs above ENMO 280mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_290_99999", "2",
                  "Count of number of epochs above ENMO 290mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_300_99999", "2",
                  "Count of number of epochs above ENMO 300mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_400_99999", "0",
                  "Count of number of epochs above ENMO 400mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_500_99999", "0",
                  "Count of number of epochs above ENMO 500mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_600_99999", "0",
                  "Count of number of epochs above ENMO 600mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_700_99999", "0",
                  "Count of number of epochs above ENMO 700mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_800_99999", "0",
                  "Count of number of epochs above ENMO 800mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_900_99999", "0",
                  "Count of number of epochs above ENMO 900mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_1000_99999", "0",
                  "Count of number of epochs above ENMO 1000mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_2000_99999", "0",
                  "Count of number of epochs above ENMO 2000mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_3000_99999", "0",
                  "Count of number of epochs above ENMO 3000mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "ENMO_4000_99999", "0",
                  "Count of number of epochs above ENMO 4000mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "PITCH_mean", "-49.925857862556", "Mean Pitch angle for the given timeframe (degrees)")
    addDictionary(model, "PITCH_std", "17.5874609971943",
                  "Standard deviation of the Pitch angle for the given timeframe")
    addDictionary(model, "PITCH_min", "-78.4456147209238",
                  "Minimum Pitch angle seen within the given timeframe (degrees)")
    addDictionary(model, "PITCH_max", "-1", "Maximum Pitch angle seen within the given timeframe (degrees)")
    addDictionary(model, "PITCH_-90_-85", "0", "Count of number of epochs between the Pitch angles -90 to -85")
    addDictionary(model, "PITCH_-85_-80", "0", "Count of number of epochs between the Pitch angles -85 to -80")
    addDictionary(model, "PITCH_-80_-75", "21", "Count of number of epochs between the Pitch angles -80 to -75")
    addDictionary(model, "PITCH_-75_-70", "10", "Count of number of epochs between the Pitch angles -75 to -70")
    addDictionary(model, "PITCH_-70_-65", "11", "Count of number of epochs between the Pitch angles -70 to -65")
    addDictionary(model, "PITCH_-65_-60", "37", "Count of number of epochs between the Pitch angles -65 to -60")
    addDictionary(model, "PITCH_-60_-55", "216", "Count of number of epochs between the Pitch angles -60 to -55")
    addDictionary(model, "PITCH_-55_-50", "297", "Count of number of epochs between the Pitch angles -55 to -50")
    addDictionary(model, "PITCH_-50_-45", "31", "Count of number of epochs between the Pitch angles -50 to -45")
    addDictionary(model, "PITCH_-45_-40", "7", "Count of number of epochs between the Pitch angles -45 to -40")
    addDictionary(model, "PITCH_-40_-35", "2", "Count of number of epochs between the Pitch angles -40 to -35")
    addDictionary(model, "PITCH_-35_-30", "1", "Count of number of epochs between the Pitch angles -35 to -30")
    addDictionary(model, "PITCH_-30_-25", "2", "Count of number of epochs between the Pitch angles -30 to -25")
    addDictionary(model, "PITCH_-25_-20", "2", "Count of number of epochs between the Pitch angles -25 to -20")
    addDictionary(model, "PITCH_-20_-15", "2", "Count of number of epochs between the Pitch angles -20 to -15")
    addDictionary(model, "PITCH_-15_-10", "2", "Count of number of epochs between the Pitch angles -15 to -10")
    addDictionary(model, "PITCH_-10_-5", "48", "Count of number of epochs between the Pitch angles -10 to -5")
    addDictionary(model, "PITCH_-5_0", "31", "Count of number of epochs between the Pitch angles -5 to 0")
    addDictionary(model, "PITCH_0_5", "0", "Count of number of epochs between the Pitch angles 0 to 5")
    addDictionary(model, "PITCH_5_10", "0", "Count of number of epochs between the Pitch angles 5 to 10")
    addDictionary(model, "PITCH_10_15", "0", "Count of number of epochs between the Pitch angles 10 to 15")
    addDictionary(model, "PITCH_15_20", "0", "Count of number of epochs between the Pitch angles 15 to 20")
    addDictionary(model, "PITCH_20_25", "0", "Count of number of epochs between the Pitch angles 20 to 25")
    addDictionary(model, "PITCH_25_30", "0", "Count of number of epochs between the Pitch angles 25 to 30")
    addDictionary(model, "PITCH_30_35", "0", "Count of number of epochs between the Pitch angles 30 to 35")
    addDictionary(model, "PITCH_35_40", "0", "Count of number of epochs between the Pitch angles 35 to 40")
    addDictionary(model, "PITCH_40_45", "0", "Count of number of epochs between the Pitch angles 40 to 45")
    addDictionary(model, "PITCH_45_50", "0", "Count of number of epochs between the Pitch angles 45 to 50")
    addDictionary(model, "PITCH_50_55", "0", "Count of number of epochs between the Pitch angles 50 to 55")
    addDictionary(model, "PITCH_55_60", "0", "Count of number of epochs between the Pitch angles 55 to 60")
    addDictionary(model, "PITCH_60_65", "0", "Count of number of epochs between the Pitch angles 60 to 65")
    addDictionary(model, "PITCH_65_70", "0", "Count of number of epochs between the Pitch angles 65 to 70")
    addDictionary(model, "PITCH_70_75", "0", "Count of number of epochs between the Pitch angles 70 to 75")
    addDictionary(model, "PITCH_75_80", "0", "Count of number of epochs between the Pitch angles 75 to 80")
    addDictionary(model, "PITCH_80_85", "0", "Count of number of epochs between the Pitch angles 80 to 85")
    addDictionary(model, "PITCH_85_90", "0", "Count of number of epochs between the Pitch angles 85 to 90")
    addDictionary(model, "ROLL_mean", "12.080063753547", "Mean Roll angle for the given timeframe (degrees)")
    addDictionary(model, "ROLL_std", "9.43803718146542", "Standard deviation of the Roll angle for the given timeframe")
    addDictionary(model, "ROLL_min", "-17.5177136735001",
                  "Minimum Roll angle seen within the given timeframe (degrees)")
    addDictionary(model, "ROLL_max", "39.6050390363596", "Maximum Roll angle seen within the given timeframe (degrees)")
    addDictionary(model, "ROLL_-90_-85", "0", "Count of number of epochs between the Roll angles -90 to -85")
    addDictionary(model, "ROLL_-85_-80", "0", "Count of number of epochs between the Roll angles -85 to -80")
    addDictionary(model, "ROLL_-80_-75", "0", "Count of number of epochs between the Roll angles -80 to -75")
    addDictionary(model, "ROLL_-75_-70", "0", "Count of number of epochs between the Roll angles -75 to -70")
    addDictionary(model, "ROLL_-70_-65", "0", "Count of number of epochs between the Roll angles -70 to -65")
    addDictionary(model, "ROLL_-65_-60", "0", "Count of number of epochs between the Roll angles -65 to -60")
    addDictionary(model, "ROLL_-60_-55", "0", "Count of number of epochs between the Roll angles -60 to -55")
    addDictionary(model, "ROLL_-55_-50", "0", "Count of number of epochs between the Roll angles -55 to -50")
    addDictionary(model, "ROLL_-50_-45", "0", "Count of number of epochs between the Roll angles -50 to -45")
    addDictionary(model, "ROLL_-45_-40", "0", "Count of number of epochs between the Roll angles -45 to -40")
    addDictionary(model, "ROLL_-40_-35", "0", "Count of number of epochs between the Roll angles -40 to -35")
    addDictionary(model, "ROLL_-35_-30", "0", "Count of number of epochs between the Roll angles -35 to -30")
    addDictionary(model, "ROLL_-30_-25", "0", "Count of number of epochs between the Roll angles -30 to -25")
    addDictionary(model, "ROLL_-25_-20", "0", "Count of number of epochs between the Roll angles -25 to -20")
    addDictionary(model, "ROLL_-20_-15", "1", "Count of number of epochs between the Roll angles -20 to -15")
    addDictionary(model, "ROLL_-15_-10", "49", "Count of number of epochs between the Roll angles -15 to -10")
    addDictionary(model, "ROLL_-10_-5", "33", "Count of number of epochs between the Roll angles -10 to -5")
    addDictionary(model, "ROLL_-5_0", "5", "Count of number of epochs between the Roll angles -5 to 0")
    addDictionary(model, "ROLL_0_5", "11", "Count of number of epochs between the Roll angles 0 to 5")
    addDictionary(model, "ROLL_5_10", "53", "Count of number of epochs between the Roll angles 5 to 10")
    addDictionary(model, "ROLL_10_15", "248", "Count of number of epochs between the Roll angles 10 to 15")
    addDictionary(model, "ROLL_15_20", "268", "Count of number of epochs between the Roll angles 15 to 20")
    addDictionary(model, "ROLL_20_25", "40", "Count of number of epochs between the Roll angles 20 to 25")
    addDictionary(model, "ROLL_25_30", "9", "Count of number of epochs between the Roll angles 25 to 30")
    addDictionary(model, "ROLL_30_35", "1", "Count of number of epochs between the Roll angles 30 to 35")
    addDictionary(model, "ROLL_35_40", "2", "Count of number of epochs between the Roll angles 35 to 40")
    addDictionary(model, "ROLL_40_45", "0", "Count of number of epochs between the Roll angles 40 to 45")
    addDictionary(model, "ROLL_45_50", "0", "Count of number of epochs between the Roll angles 45 to 50")
    addDictionary(model, "ROLL_50_55", "0", "Count of number of epochs between the Roll angles 50 to 55")
    addDictionary(model, "ROLL_55_60", "0", "Count of number of epochs between the Roll angles 55 to 60")
    addDictionary(model, "ROLL_60_65", "0", "Count of number of epochs between the Roll angles 60 to 65")
    addDictionary(model, "ROLL_65_70", "0", "Count of number of epochs between the Roll angles 65 to 70")
    addDictionary(model, "ROLL_70_75", "0", "Count of number of epochs between the Roll angles 70 to 75")
    addDictionary(model, "ROLL_75_80", "0", "Count of number of epochs between the Roll angles 75 to 80")
    addDictionary(model, "ROLL_80_85", "0", "Count of number of epochs between the Roll angles 80 to 85")
    addDictionary(model, "ROLL_85_90", "0", "Count of number of epochs between the Roll angles 85 to 90")
    addDictionary(model, "Temperature_mean", "23.6185242588329", "Mean Temperature for the given timeframe (°C)")
    addDictionary(model, "Integrity_sum", "0",
                  "Each data point in the timeseries is assigned an integrity sum value, -1 is applied where there is missing data, 0 for data that has passed integrity checks and 1 where the data has failed integrity checks")
    addDictionary(model, "HPFVM_mean", "67.1083768345898", "Mean HPFVM for the given timeframe (mg)")
    addDictionary(model, "HPFVM_n", "720",
                  "Epoch level count of how many HPFVM data points are present within the given timeframe")
    addDictionary(model, "HPFVM_missing", "0",
                  "Epoch level count of how many HPFVM data points include non-wear within the given timeframe")
    addDictionary(model, "HPFVM_sum", "48318.0313209046", "Total amount of HPFVM for that given timeframe (mg)")
    addDictionary(model, "HPFVM_0_99999", "719",
                  "Count of number of epochs above HPFVM 0mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_1_99999", "689",
                  "Count of number of epochs above HPFVM 1mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_2_99999", "624",
                  "Count of number of epochs above HPFVM 2mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_3_99999", "582",
                  "Count of number of epochs above HPFVM 3mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_4_99999", "544",
                  "Count of number of epochs above HPFVM 4mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_5_99999", "539",
                  "Count of number of epochs above HPFVM 5mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_10_99999", "522",
                  "Count of number of epochs above HPFVM 10mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_15_99999", "486",
                  "Count of number of epochs above HPFVM 15mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_20_99999", "473",
                  "Count of number of epochs above HPFVM 20mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_25_99999", "453",
                  "Count of number of epochs above HPFVM 25mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_30_99999", "435",
                  "Count of number of epochs above HPFVM 30mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_35_99999", "398",
                  "Count of number of epochs above HPFVM 35mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_40_99999", "374",
                  "Count of number of epochs above HPFVM 40mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_45_99999", "333",
                  "Count of number of epochs above HPFVM 45mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_50_99999", "297",
                  "Count of number of epochs above HPFVM 50mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_55_99999", "263",
                  "Count of number of epochs above HPFVM 55mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_60_99999", "227",
                  "Count of number of epochs above HPFVM 60mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_65_99999", "204",
                  "Count of number of epochs above HPFVM 65mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_70_99999", "189",
                  "Count of number of epochs above HPFVM 70mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_75_99999", "176",
                  "Count of number of epochs above HPFVM 75mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_80_99999", "161",
                  "Count of number of epochs above HPFVM 80mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_85_99999", "146",
                  "Count of number of epochs above HPFVM 85mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_90_99999", "139",
                  "Count of number of epochs above HPFVM 90mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_95_99999", "124",
                  "Count of number of epochs above HPFVM 95mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_100_99999", "120",
                  "Count of number of epochs above HPFVM 100mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_105_99999", "112",
                  "Count of number of epochs above HPFVM 105mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_110_99999", "105",
                  "Count of number of epochs above HPFVM 110mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_115_99999", "102",
                  "Count of number of epochs above HPFVM 115mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_120_99999", "100",
                  "Count of number of epochs above HPFVM 120mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_125_99999", "98",
                  "Count of number of epochs above HPFVM 125mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_130_99999", "97",
                  "Count of number of epochs above HPFVM 130mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_135_99999", "95",
                  "Count of number of epochs above HPFVM 135mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_140_99999", "93",
                  "Count of number of epochs above HPFVM 140mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_145_99999", "92",
                  "Count of number of epochs above HPFVM 145mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_150_99999", "86",
                  "Count of number of epochs above HPFVM 150mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_160_99999", "84",
                  "Count of number of epochs above HPFVM 160mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_170_99999", "80",
                  "Count of number of epochs above HPFVM 170mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_180_99999", "78",
                  "Count of number of epochs above HPFVM 180mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_190_99999", "72",
                  "Count of number of epochs above HPFVM 190mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_200_99999", "68",
                  "Count of number of epochs above HPFVM 200mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_210_99999", "64",
                  "Count of number of epochs above HPFVM 210mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_220_99999", "62",
                  "Count of number of epochs above HPFVM 220mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_230_99999", "62",
                  "Count of number of epochs above HPFVM 230mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_240_99999", "58",
                  "Count of number of epochs above HPFVM 240mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_250_99999", "55",
                  "Count of number of epochs above HPFVM 250mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_260_99999", "53",
                  "Count of number of epochs above HPFVM 260mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_270_99999", "51",
                  "Count of number of epochs above HPFVM 270mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_280_99999", "48",
                  "Count of number of epochs above HPFVM 280mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_290_99999", "39",
                  "Count of number of epochs above HPFVM 290mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_300_99999", "33",
                  "Count of number of epochs above HPFVM 300mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_400_99999", "7",
                  "Count of number of epochs above HPFVM 400mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_500_99999", "4",
                  "Count of number of epochs above HPFVM 500mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_600_99999", "0",
                  "Count of number of epochs above HPFVM 600mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_700_99999", "0",
                  "Count of number of epochs above HPFVM 700mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_800_99999", "0",
                  "Count of number of epochs above HPFVM 800mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_900_99999", "0",
                  "Count of number of epochs above HPFVM 900mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_1000_99999", "0",
                  "Count of number of epochs above HPFVM 1000mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_2000_99999", "0",
                  "Count of number of epochs above HPFVM 2000mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_3000_99999", "0",
                  "Count of number of epochs above HPFVM 3000mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "HPFVM_4000_99999", "0",
                  "Count of number of epochs above HPFVM 4000mg. To convert to minutes use equation: Variable/(60/processing epoch)")
    addDictionary(model, "Battery_mean", "197.732170598663", "Mean Battery for the given timeframe")

    return model

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = DataDictionaryWindow()
    window.setSourceModel(createDictionaryModel(window))
    window.show()
    sys.exit(app.exec_())