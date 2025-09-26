// Serviço de integração com Google Drive
class GoogleDriveService {
  constructor() {
    this.isInitialized = false;
    this.isSignedIn = false;
    this.fileName = 'financial-control-backup.json';
    this.folderId = null;
  }

  // Inicializa Google Drive API
  async initialize() {
    return new Promise((resolve, reject) => {
      if (this.isInitialized) {
        resolve(true);
        return;
      }

      // Carrega a API do Google
      if (!window.gapi) {
        const script = document.createElement('script');
        script.src = 'https://apis.google.com/js/api.js';
        script.onload = () => this.loadGoogleAPI(resolve, reject);
        script.onerror = () => reject(new Error('Falha ao carregar Google API'));
        document.head.appendChild(script);
      } else {
        this.loadGoogleAPI(resolve, reject);
      }
    });
  }

  // Carrega e configura Google API
  loadGoogleAPI(resolve, reject) {
    window.gapi.load('auth2:client', async () => {
      try {
        await window.gapi.client.init({
          apiKey: 'YOUR_API_KEY', // Será configurado pelo usuário
          clientId: 'YOUR_CLIENT_ID', // Será configurado pelo usuário
          discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'],
          scope: 'https://www.googleapis.com/auth/drive.file'
        });

        this.authInstance = window.gapi.auth2.getAuthInstance();
        this.isInitialized = true;
        this.isSignedIn = this.authInstance.isSignedIn.get();
        resolve(true);
      } catch (error) {
        reject(error);
      }
    });
  }

  // Faz login no Google
  async signIn() {
    if (!this.isInitialized) {
      throw new Error('Google Drive não inicializado');
    }

    try {
      if (!this.isSignedIn) {
        await this.authInstance.signIn();
        this.isSignedIn = true;
      }
      return true;
    } catch (error) {
      throw new Error('Falha no login do Google: ' + error.message);
    }
  }

  // Faz logout do Google
  async signOut() {
    if (this.authInstance && this.isSignedIn) {
      await this.authInstance.signOut();
      this.isSignedIn = false;
    }
  }

  // Verifica se está logado
  isAuthenticated() {
    return this.isSignedIn;
  }

  // Cria pasta no Google Drive se não existir
  async ensureFolder() {
    if (this.folderId) return this.folderId;

    try {
      // Procura pasta existente
      const response = await window.gapi.client.drive.files.list({
        q: "name='Financial Control' and mimeType='application/vnd.google-apps.folder'",
        spaces: 'drive'
      });

      if (response.result.files.length > 0) {
        this.folderId = response.result.files[0].id;
      } else {
        // Cria nova pasta
        const folderResponse = await window.gapi.client.drive.files.create({
          resource: {
            name: 'Financial Control',
            mimeType: 'application/vnd.google-apps.folder'
          }
        });
        this.folderId = folderResponse.result.id;
      }

      return this.folderId;
    } catch (error) {
      throw new Error('Erro ao criar/encontrar pasta: ' + error.message);
    }
  }

  // Salva dados no Google Drive
  async saveToGoogleDrive(data) {
    if (!this.isSignedIn) {
      await this.signIn();
    }

    try {
      const folderId = await this.ensureFolder();
      const content = JSON.stringify(data, null, 2);
      
      // Verifica se arquivo já existe
      const existingFiles = await window.gapi.client.drive.files.list({
        q: `name='${this.fileName}' and parents='${folderId}'`,
        spaces: 'drive'
      });

      const metadata = {
        name: this.fileName,
        parents: [folderId]
      };

      const form = new FormData();
      form.append('metadata', new Blob([JSON.stringify(metadata)], {type: 'application/json'}));
      form.append('file', new Blob([content], {type: 'application/json'}));

      let response;
      if (existingFiles.result.files.length > 0) {
        // Atualiza arquivo existente
        response = await fetch(`https://www.googleapis.com/upload/drive/v3/files/${existingFiles.result.files[0].id}?uploadType=multipart`, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${window.gapi.auth2.getAuthInstance().currentUser.get().getAuthResponse().access_token}`
          },
          body: form
        });
      } else {
        // Cria novo arquivo
        response = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${window.gapi.auth2.getAuthInstance().currentUser.get().getAuthResponse().access_token}`
          },
          body: form
        });
      }

      if (response.ok) {
        return await response.json();
      } else {
        throw new Error('Falha ao salvar no Google Drive');
      }
    } catch (error) {
      throw new Error('Erro ao salvar no Google Drive: ' + error.message);
    }
  }

  // Carrega dados do Google Drive
  async loadFromGoogleDrive() {
    if (!this.isSignedIn) {
      await this.signIn();
    }

    try {
      const folderId = await this.ensureFolder();
      
      // Procura arquivo de backup
      const response = await window.gapi.client.drive.files.list({
        q: `name='${this.fileName}' and parents='${folderId}'`,
        spaces: 'drive'
      });

      if (response.result.files.length === 0) {
        throw new Error('Nenhum backup encontrado no Google Drive');
      }

      const fileId = response.result.files[0].id;
      const fileResponse = await window.gapi.client.drive.files.get({
        fileId: fileId,
        alt: 'media'
      });

      return JSON.parse(fileResponse.body);
    } catch (error) {
      throw new Error('Erro ao carregar do Google Drive: ' + error.message);
    }
  }

  // Lista backups disponíveis
  async listBackups() {
    if (!this.isSignedIn) {
      await this.signIn();
    }

    try {
      const folderId = await this.ensureFolder();
      
      const response = await window.gapi.client.drive.files.list({
        q: `parents='${folderId}' and name contains 'financial'`,
        spaces: 'drive',
        fields: 'files(id,name,modifiedTime,size)'
      });

      return response.result.files.map(file => ({
        id: file.id,
        name: file.name,
        lastModified: new Date(file.modifiedTime),
        size: file.size
      }));
    } catch (error) {
      throw new Error('Erro ao listar backups: ' + error.message);
    }
  }

  // Configura credenciais da API
  setCredentials(apiKey, clientId) {
    this.apiKey = apiKey;
    this.clientId = clientId;
  }

  // Verifica se as credenciais estão configuradas
  hasCredentials() {
    return !!(this.apiKey && this.clientId);
  }
}

// Instância singleton
const googleDriveService = new GoogleDriveService();
export default googleDriveService;
