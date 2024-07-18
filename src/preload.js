// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  processVideo: (filePath, compression) => ipcRenderer.send('process-video', { filePath, compression }),
  onProcessComplete: (callback) => ipcRenderer.on('process-complete', callback),
});

