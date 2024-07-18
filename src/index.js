const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('node:path');
const { execFile } = require('child_process');
const fs = require('fs');
const os = require('os');

if (require('electron-squirrel-startup')) {
  app.quit();
}

const createWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      enableRemoteModule: false,
    },
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));
  mainWindow.webContents.openDevTools();
};

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Handle the 'process-video' IPC message
ipcMain.on('process-video', (event, { filePath, compression }) => {
  if (filePath) {
    const outputPath = path.join(os.tmpdir(), 'compressed_video.mp4'); // Use a temp file for output

    execFile('python', [path.join(__dirname, 'compression.py'), filePath, outputPath, compression], (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        event.reply('process-complete', { success: false, message: `Error: ${error.message}` });
        return;
      }
      if (stderr) {
        console.error(`Stderr: ${stderr}`);
        event.reply('process-complete', { success: false, message: `Stderr: ${stderr}` });
        return;
      }
      console.log(`Stdout: ${stdout}`);
      event.reply('process-complete', { success: true, message: 'File processed successfully!', outputPath });
    });
  } else {
    event.reply('process-complete', { success: false, message: 'No file selected.' });
  }
});
