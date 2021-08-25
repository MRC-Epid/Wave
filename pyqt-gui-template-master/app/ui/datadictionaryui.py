from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
        QTime)
from PyQt5.QtGui import QStandardItemModel
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
        self.filterSyntaxComboBox.addItem("Regular expression", QRegExp.RegExp)
        self.filterSyntaxComboBox.addItem("Wildcard", QRegExp.Wildcard)
        self.filterSyntaxComboBox.addItem("Fixed string", QRegExp.FixedString)
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

        self.setWindowTitle("Basic Sort/Filter Model")
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

    return model

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = DataDictionaryWindow()
    window.setSourceModel(createDictionaryModel(window))
    window.show()
    sys.exit(app.exec_())