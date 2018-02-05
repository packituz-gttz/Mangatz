from PyQt4.QtGui import QApplication
import download_manga

def main():
    app = QApplication(['Mangatz'])
    app.setOrganizationName('Gatituz PK')
    app.setOrganizationDomain('http://gatituzmes-server.duckdns.org/')
    app.setApplicationName('Mangatz')
    window = download_manga.MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()