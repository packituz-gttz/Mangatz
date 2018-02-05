import urllib
from bs4 import BeautifulSoup
import os
from PyQt4.QtCore import (QThread, QDir, QMutex, QWaitCondition, QSettings, QVariant, QStringList)
from PyQt4.QtGui import (QMainWindow, QMessageBox, QImage, QPixmap, QKeySequence, QDialog, QDialogButtonBox, QAction)
import datetime
from Gui import MangaDownloader, Dialog_Settings
from PyQt4.QtCore import pyqtSignal as Signal
import resource
import tempfile
import zipfile
import re

# Elements for waiting user confirmation for overriding file
waitCondition = QWaitCondition()
mutex = QMutex()

class MainWindow(QMainWindow, MangaDownloader.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.mutex = QMutex()
        self.settings_dict = dict(recent=5, save_dir=QDir.homePath(), close_confirmation=True,
                              display_image=True, list_recent=[])
        self.pushbutton_stop.setEnabled(False)
        self.edit_url.setFocus()
        self.image = QImage()
        self.pushbutton_start.clicked.connect(self.startDownload)

        self.action_Quit.setShortcut(QKeySequence.Quit)
        self.action_Quit.triggered.connect(self.close)

        self.actionPreferences.setShortcut(QKeySequence.Preferences)
        self.actionPreferences.triggered.connect(self.open_preferences)
        self.load_settings()

        self.menu_Recent.aboutToShow.connect(self.load_recent_files)

        #self.setWindowIcon(QIcon(":/window_icon.png"))

    def load_recent_files(self):
        self.menu_Recent.clear()
        print "me"
        for fname in self.settings_dict['list_recent']:
            print "mes"
            action = QAction(fname, self)
            # action.triggere.connect()
            self.menu_Recent.addAction(action)

    def add_new_recent_file(self):
        file_downloaded = ' '.join([unicode(self.series_title_label.text()), unicode(self.label_chapter.text())])
        if not self.settings_dict['list_recent'].contains(file_downloaded):
            print "dadasd2"
            self.settings_dict['list_recent'].prepend(file_downloaded)
            print self.settings_dict['list_recent']
        print type(self.settings_dict['list_recent'])
        print self.settings_dict['recent']
        while self.settings_dict['list_recent'].count() > self.settings_dict['recent']:
            self.settings_dict['list_recent'].takeLast()


    def startDownload(self):
        if not self.edit_url.text():
            QMessageBox.warning(self, 'Warning', 'Missing URL')
        else:
            self.download_thread = DownloadThread(self, self.edit_url.text())
            self.download_thread.start()
            self.download_thread.finished.connect(self.completed)
            # Custom signals
            self.download_thread.new_progress.connect(self.update_progressbar)
            self.download_thread.page_init.connect(self.update_init_info)
            self.download_thread.error_terminate.connect(self.terminate_on_error)
            self.download_thread.override_confirmation.connect(self.override_check)
            self.download_thread.success_on_terminate.connect(self.add_new_recent_file)

            self.pushbutton_stop.clicked.connect(self.download_thread.terminate)
            self.pushbutton_start.setEnabled(False)
            self.pushbutton_stop.setEnabled(True)

    def open_preferences(self):
        dialog = SettingsDialog(self.settings_dict, self)
        dialog.exec_()

    def load_settings(self):
        settings = QSettings()
        self.settings_dict['recent'] = settings.value('recent',
                                                      self.settings_dict['recent']).toInt()[0]
        self.settings_dict['save_dir'] = settings.value('save_dir',
                                                        self.settings_dict['save_dir']).toString()
        self.settings_dict['close_confirmation'] = settings.value('close_confirmation',
                                                                  self.settings_dict['close_confirmation']).toBool()
        self.settings_dict['display_image'] = settings.value('display_image',
                                                             self.settings_dict['display_image']).toBool()
        self.settings_dict['list_recent'] = settings.value('list_recent',
                                                           self.settings_dict['list_recent']).toStringList()

    def update_progressbar(self, current_page, max_page):
        if max_page != self.progressbar_download.maximum():
            self.progressbar_download.setMaximum(max_page)
        self.progressbar_download.setValue(current_page)


    def completed(self):
        self.pushbutton_start.setEnabled(True)
        self.pushbutton_stop.setEnabled(False)

    def update_init_info(self, image_location, title, chapter):
        self.series_title_label.setText(title)
        self.label_chapter.setText('Chapter: ' + chapter)
        # print  image_location
        image = QImage(image_location)
        # print image
        if not image.isNull():
            # print "me"
            self.label_image.setPixmap(QPixmap.fromImage(image))

    def terminate_on_error(self):
        print "error"
        self.download_thread.terminate()
        self.pushbutton_start.setEnabled(False)
        self.pushbutton_stop.setEnabled(True)

    def override_check(self):
        print "Override me"
        self.download_thread.result_confirmation = QMessageBox.question(self, 'Confirmation', 'File exists, override?',
                                                   QMessageBox.Ok | QMessageBox.Cancel)
        waitCondition.wakeAll()

    def closeEvent(self, QCloseEvent):
        try:
            if self.download_thread.isRunning():
                result = QMessageBox.question(self, 'Close', 'Close Program?', QMessageBox.Ok | QMessageBox.Cancel)
                if result == QMessageBox.Ok:
                  pass
                else:
                    QCloseEvent.ignore()
        except AttributeError:
            pass
        finally:
            settings = QSettings()
            settings.setValue('recent', QVariant(self.settings_dict['recent']))
            settings.setValue('save_dir', QVariant(self.settings_dict['save_dir']))
            settings.setValue('close_confirmation', QVariant(self.settings_dict['close_confirmation']))
            settings.setValue('display_image', QVariant(self.settings_dict['display_image']))
            settings.setValue('list_recent', QVariant(self.settings_dict['list_recent']))


class SettingsDialog(QDialog, Dialog_Settings.Ui_Dialog):
    def __init__(self, settings, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.settings = settings
        self.set_values()
        print settings

    def set_values(self):
        print self.settings
        self.spinbox_downloads.setValue(self.settings['recent'])
        self.lineedit_path.setText(self.settings['save_dir'])
        self.checkbox_close.setChecked(self.settings['close_confirmation'])
        self.checkbox_image.setChecked(self.settings['display_image'])
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept_check)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.defaults)

    def accept_check(self):
        self.settings['recent'] = self.spinbox_downloads.value()
        self.settings['save_dir'] = self.lineedit_path.text()
        self.settings['close_confirmation'] = self.checkbox_close.isChecked()
        self.settings['display_image'] = self.checkbox_image.isChecked()
        self.accept()

    def defaults(self):
        defaults_settings_dict = dict(recent=5, save_dir=QDir.homePath(), close_confirmation=True,
                                           display_image=True, list_recent=[])
        self.settings['recent'] = defaults_settings_dict['recent']
        self.settings['save_dir'] = defaults_settings_dict['save_dir']
        self.settings['close_confirmation'] = defaults_settings_dict['close_confirmation']
        self.settings['display_image'] = defaults_settings_dict['display_image']
        self.settings['list_recent'] = defaults_settings_dict['list_recent']
        self.set_values()



class DownloadThread(QThread):

    new_progress = Signal(int, int)
    success_on_terminate = Signal()
    page_init = Signal(unicode, unicode, unicode)
    error_terminate = Signal()
    override_confirmation = Signal()

    def __init__(self, parent=None, url=''):
        super(DownloadThread, self).__init__(parent)
        # print url
        self.url = url
        self.temp_file = None
        self.series_title = None
        self.result_confirmation = None
        self.chapter = None

    def run(self):
        #self.sleep(2)
        self.get_data(unicode(self.url))

    def get_data(self, link_page):
        try:
            self.get_series_initial_info()
        except (IOError, AttributeError):
            self.error_terminate.emit()
            return
        while True:
            try:
                # Initialize soup object
                url = link_page
                html_data = urllib.urlopen(url).read()
                soup = BeautifulSoup(html_data, 'lxml')

                data_section = soup.find('form', attrs={'name': 'myform'})
                # Get image link
                self.image = data_section.find('img').get('src')
                # Get values for next image
                #print data_section.find('input', attrs={'name': 'c'}).get('value')
                c_value = data_section.find('input', attrs={'name': 'c'}).get('value')
                #print data_section.find('input', attrs={'name': 'i'}).get('value')
                i_value = data_section.find('input', attrs={'name': 'i'}).get('value')
                #print data_section.find('input', attrs={'name': 'cp'}).get('value')
                cp_value = data_section.find('input', attrs={'name': 'cp'}).get('value')

                # Get next page
                select_sections = soup.find('select', attrs={'class': 'form-control',
                                                             'name': 'cp'})

                # Get last page of chapter
                self.max_page = select_sections.find('option')
                #print ("Max Page: ", max_page.text)

                # Get current page
                self.current_page = select_sections.find('option', attrs={'selected': 'selected'})
                #print ("Current Page: ", current_page.text)

            except (AttributeError, IOError):
                print "DATA"
                self.error_terminate.emit()
                break
            else:
                self.download_image()
                if os.path.exists(os.path.join(unicode(QDir.homePath()),
                                               '.'.join([self.series_title + self.chapter, 'cbz']))) \
                        and self.result_confirmation != QMessageBox.Ok:
                    self.override_confirmation.emit()

                    mutex.lock()
                    waitCondition.wait(mutex)
                    mutex.unlock()

                    if self.result_confirmation == QMessageBox.Ok:
                        if self.current_page.text == self.max_page.text:
                            with zipfile.ZipFile(
                                    os.path.join(unicode(QDir.homePath()), '.'.join([self.series_title + self.chapter,
                                                                                     'cbz'])),
                                    'w') as fzip:
                                for image_file in os.listdir(self.temp_file):
                                    fzip.write(os.path.join(self.temp_file, image_file), os.path.basename(image_file))
                            break
                    else:
                        break

                else:
                    if self.current_page.text == self.max_page.text:
                        try:
                            with zipfile.ZipFile(os.path.join(unicode(QDir.homePath()),
                                                              '.'.join([self.series_title + self.chapter, 'cbz'])),
                                                 'w') as fzip:
                                for image_file in os.listdir(self.temp_file):
                                    fzip.write(os.path.join(self.temp_file ,image_file), os.path.basename(image_file) )
                            self.success_on_terminate.emit()
                            print "messadas"
                            break
                        except (IOError, OSError):
                            self.error_terminate.emit()
                        else:
                            print "MESESES"

                url_c = '='.join(['c', c_value])
                url_i = '='.join(['i', i_value])
                url_cp = '='.join(['cp', cp_value])

                link_page = 'http://mangachameleon.com/?' + '&'.join([url_c, url_i, url_cp])
                #print link_page

    def download_image(self):
        # Download image
        image_extension = str(self.image).rsplit('.', 1)[1]
        current_page_formated = self.current_page.text
        while len(current_page_formated) < 3:
            current_page_formated = '0' + current_page_formated
        print "up"
        image_file = urllib.urlretrieve(self.image, os.path.join(self.temp_file, '.'.join([str(current_page_formated),
                                                                                      str(image_extension)])))
        print "down"
        self.new_progress.emit(int(self.current_page.text), int(self.max_page.text))

    def get_series_initial_info(self):
        url = unicode(self.url)
        html_data = urllib.urlopen(url).read()
        soup = BeautifulSoup(html_data, 'lxml')

        # Get Form
        title_section = soup.find('h2', attrs={'style': 'padding-left:0.5em'})
        title = title_section.find('a')
        # print title.text
        url_init = ''.join(['http://mangachameleon.com/', title_section.find('a').get('href')])
        # print url_init


        html_data = urllib.urlopen(unicode(url_init)).read()
        soup_init = BeautifulSoup(html_data, 'lxml')

        image_cover_main = soup_init.find('img',
                                     attrs={'style': 'max-width: 222px; padding-bottom:2em                                                                            '})
        image_cover = image_cover_main.get('src')
        #print image_cover_main.find('img')

        image_local = urllib.urlretrieve(image_cover, os.path.join(unicode(QDir.tempPath()), 'cover'))
        self.series_title = title.text
        self.temp_file = tempfile.mkdtemp(suffix=title.text, dir=unicode(QDir.tempPath()))


        # Get chapter number
        chapter_section = soup.find('form', attrs={'class': 'col-md-3 col-sm-4 col-xs-12'})
        current_chapter = (chapter_section.find('select')).find('option', attrs={'selected': 'selected'})
        print current_chapter.text
        match = re.search(r'\b[0-9]+(.[0-9]+)?', current_chapter.text)
        self.chapter = match.group()
        print match.group()

        self.page_init.emit(os.path.join(unicode(QDir.tempPath()), 'cover'), title.text, self.chapter)
        # print data_section
        # Get image link
        #self.image = data_section.find('img').get('src')




#print str(image).rsplit('.jpg', 1)[0].rsplit('/', 1)[1]




# form_sections = soup.find_all('form', attrs={'class':'col-md-1 col-sm-2 col-xs-4'})
#
# for form in form_sections:
#     list_forms = form.find_all('input')
#     if len(list_forms) != 4:
#         del list_forms
#
# try:
#     for input_data in list_forms:
#         print input_data
#         if input_data.get('name') == 'c':
#             c_value = input_data.get('value')
#         elif input_data.get('name') == 'i':
#             i_value = input_data.get('value')
#         elif input_data.get('name') == 'cp':
#             cp_value = input_data.get('value')
#
#     print c_value
#     print i_value
#     print cp_value
# except NameError:
#     pass
if __name__ == '__main__':
    print datetime.datetime.now()
    #get_data("http://mangachameleon.com/?c=4e73d7d2c09225616d325c56&i=4e70ea6ac092255ef7006a52")
