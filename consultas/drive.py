"""
Integración con Google Drive usando cuenta de servicio.
"""
from django.conf import settings


def get_drive_service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_DRIVE_CREDENTIALS_FILE, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)


def get_or_create_folder(service, nombre, parent_id=None):
    """Busca carpeta por nombre (y padre), la crea si no existe."""
    query = f"name='{nombre}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    resultados = service.files().list(q=query, fields='files(id, name)').execute()
    archivos = resultados.get('files', [])

    if archivos:
        return archivos[0]['id']

    metadata = {
        'name': nombre,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    if parent_id:
        metadata['parents'] = [parent_id]

    carpeta = service.files().create(body=metadata, fields='id').execute()
    return carpeta['id']


def subir_archivo_drive(archivo, consulta):
    """
    Sube un archivo a Drive con la estructura:
    📁 Consultorio / 📁 [cedula - nombre] / 📁 [fecha - Consulta] / archivo
    """
    from googleapiclient.http import MediaIoBaseUpload
    import io

    service = get_drive_service()

    paciente = consulta.paciente
    fecha_str = consulta.fecha.strftime('%Y-%m-%d')

    # Crear jerarquía de carpetas
    root_id = get_or_create_folder(service, settings.GOOGLE_DRIVE_ROOT_FOLDER_NAME)
    paciente_folder_name = f'{paciente.cedula} - {paciente.nombre_completo}'
    paciente_id = get_or_create_folder(service, paciente_folder_name, root_id)
    consulta_folder_name = f'{fecha_str} - Consulta'
    consulta_id = get_or_create_folder(service, consulta_folder_name, paciente_id)

    # Subir archivo
    contenido = archivo.read()
    media = MediaIoBaseUpload(
        io.BytesIO(contenido),
        mimetype=archivo.content_type,
        resumable=True,
    )
    metadata = {
        'name': archivo.name,
        'parents': [consulta_id],
    }
    archivo_drive = service.files().create(
        body=metadata,
        media_body=media,
        fields='id',
    ).execute()

    return {
        'file_id': archivo_drive['id'],
        'folder_id': consulta_id,
    }
