import QtQuick 2.1
import QtWebEngine 1.2

QtObject {
    id: root

    property QtObject defaultProfile: WebEngineProfile {
        storageName: "Default"
    }

    property QtObject otrProfile: WebEngineProfile {
        offTheRecord: true
    }

    property Component browserWindowComponent: BrowserWindow {
        applicationRoot: root
        onClosing: destroy()
    }
    property Component browserDialogComponent: BrowserDialog {
        onClosing: destroy()
    }
    function createWindow(profile) {
        var newWindow = browserWindowComponent.createObject(root)
        newWindow.currentWebView.profile = profile
        profile.downloadRequested.connect(newWindow.onDownloadRequested)
        return newWindow
    }
    function createDialog(profile) {
        var newDialog = browserDialogComponent.createObject(root)
        newDialog.currentWebView.profile = profile
        return newDialog
    }
    function load(url) {
        var browserWindow = createWindow(defaultProfile)
        browserWindow.currentWebView.url = url
    }
}
