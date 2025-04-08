// O arquivo main.js é o ponto de entrada do seu aplicativo Electron. 
// Ele cria uma janela e carrega o conteúdo HTML.

const { app, BrowserWindow } = require('electron');

function createWindow() {
    // Cria uma janela do navegador
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true, // Permite o uso do Node.js no front-end
            contextIsolation: false
        }
    });

    // Carrega o arquivo HTML
    win.loadFile('index.html');

    // Abre o DevTools (ferramentas de desenvolvedor)
    // win.webContents.openDevTools();
}

// Quando o aplicativo estiver pronto, cria a janela
app.whenReady().then(createWindow);

// Fecha o aplicativo quando todas as janelas estiverem fechadas
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});