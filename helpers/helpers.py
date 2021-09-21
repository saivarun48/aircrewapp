import logging
import uuid
from datetime import datetime, timedelta

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, BlobSasPermissions

from config.config import AZURE_STORAGE_CONNECTION_STRING, AZURE_STORAGE_ACCOUNT_NAME, AZURE_STORAGE_ACCOUNT_KEY

# [English] Create pre-signed URL on Azure Blob Storage 
# [Portuguese] Cria URL autenticada no Azure Blob Storage
def create_presigned_url(container_name, azure_blob):

    try:
        sas_blob = generate_blob_sas(account_name=AZURE_STORAGE_ACCOUNT_NAME, 
                                    container_name= container_name,
                                    blob_name=azure_blob,
                                    account_key= AZURE_STORAGE_ACCOUNT_KEY,
                                    #For writing back to the Azure Blob set write and create to True 
                                    permission=BlobSasPermissions(read=True, write= False, create= False),
                                    #This URL will be valid for 1 hour
                                    expiry=datetime.utcnow() + timedelta(hours=1))
        
        response = 'https://'+AZURE_STORAGE_ACCOUNT_NAME+'.blob.core.windows.net/'+ container_name +'/'+ azure_blob +'?'+ sas_blob
        return response
    except Exception as e:
        logging.error(e)
        print(e)
        return False

# [English] Upload file to Azure Blob Storage 
# [Portuguese] Faz upload de arquivo para o Azure Blob Storage
def upload_file(file_name, container_name, final_file_name):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=final_file_name)
    try:
        with open(file_name, "rb") as data:
            blob_client.upload_blob(data)
    except Exception as e:
        logging.error(e)
        print(e)
        return False
    return True

# [English] Generate unique file name 
# [Portuguese] Gerar nome de arquivo dinâmico
def generate_unique_filename(name,surname):
    name = name.split()[0].lower()
    surname = surname.split()[-1].lower()
    unique_id = str(uuid.uuid4())

    file_name = unique_id + "_" + name + "_" + surname + ".pdf"

    return file_name

# [English] Allowed file extensions.
# [Portuguese] Extensões permitidas de arquivos.
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS