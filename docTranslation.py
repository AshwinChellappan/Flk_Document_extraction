import csv
import io
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient
import requests
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

#Method copying files from local to the  
def LocalToBlob(content,filename) :

    DeleteBlobs()

    Filename = filename
    Content = content
    #print(Content)
    #print(Filename)

    # Define the connection string and container name  
    connect_str = "DefaultEndpointsProtocol=https;AccountName=flkdoctransln;AccountKey=JmR0VSuJZenxo6Eg/SW/nQEeboRtbca0YpJASH+FhTmD+k/TOhHqCPJFlMAjyTj+k9fIAhhbJRkS+AStY+75qw==;EndpointSuffix=core.windows.net"  
    container_name = "wrdflklntrlnsource"
    
    # Create a BlobServiceClient object  
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    # Create a container client object  
    container_client = blob_service_client.get_container_client(container_name)
    
    blob_client = container_client.get_blob_client(filename)
    blob_client.upload_blob(content, overwrite=True)

from azure.storage.blob import BlobClient  
import requests  


def Translate(language) :
    #print("inside_doctranslate")

    #endpoint = "https://trrsltrlntr.cognitiveservices.azure.com/"
    endpoint = "https://doctransln.cognitiveservices.azure.com/"
    
    #key = "c2324a985a1741a18f47c83ac8b506c4"
    key = "dbdd2a9122264a48b0edccabf62796ce"
    
    
    #source_container_url = "https://flklntransln.blob.core.windows.net/wrdflklntrlnsource?sp=rcwl&st=2023-09-01T07:14:50Z&se=2024-11-05T15:14:50Z&sv=2022-11-02&sr=c&sig=K%2BS3sTapksT8k%2F0HaK2sd%2FdWF1Y1XI2%2FRB3%2FwIqTB8k%3D"
    # Use HTTPS and HTTP from SAS token
    source_container_url = "https://flkdoctransln.blob.core.windows.net/wrdflklntrlnsource?sp=racwdl&st=2024-02-13T10:14:54Z&se=2025-01-01T18:14:54Z&sv=2022-11-02&sr=c&sig=PPgArrm5Jz%2FRB13Sl0lFgUHVLDbWP%2Fz1qCMemXp4j7I%3D"
    #target_container_url = "https://flklntransln.blob.core.windows.net/wrdflklntrlntarget?sp=rcwl&st=2023-09-01T07:17:14Z&se=2024-10-05T15:17:14Z&sv=2022-11-02&sr=c&sig=YXWiPaMRxGkI5kas3l3qK9LhlLIX1ztAD390GQ%2BM3NI%3D"
    target_container_url = "https://flkdoctransln.blob.core.windows.net/wrdflklntrlntarget?sp=racwdl&st=2024-02-13T10:11:53Z&se=2025-01-01T18:11:53Z&sv=2022-11-02&sr=c&sig=2NadLXAbbekGOD%2B%2FhjwDy4ua%2BVRvBf9uYU6IwqH%2Bt%2BE%3D"

    print("endpoint-----------------",endpoint)
    client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))

    target_languages = language
    print("Language--- : ",target_languages)
    
    poller = client.begin_translation(source_container_url, target_container_url,target_languages)

    result = poller.result()

    print(f"Status: {poller.status()}")

    print(f"Created on: {poller.details.created_on}")

    print(f"Last updated on: {poller.details.last_updated_on}")

    print(f"Total number of translations on documents: {poller.details.documents_total_count}")

    print("\nOf total documents...")

    print(f"{poller.details.documents_failed_count} failed")

    print(f"{poller.details.documents_succeeded_count} succeeded")

    for document in result:

        print(f"Document ID: {document.id}")

        print(f"Document status: {document.status}")

        if document.status == "Succeeded":

            print(f"Source document location: {document.source_document_url}")

            print(f"Translated document location: {document.translated_document_url}")

            print(f"Translated to language: {document.translated_to}\n")

        else:

            print(f"Error Code: {document.error.code}, Message: {document.error.message}\n")

    BlobToLocal()  


def BlobToLocal() :

    print("Initiatng File Download")

    # Define the connection string and container name  
    connect_str = "DefaultEndpointsProtocol=https;AccountName=flkdoctransln;AccountKey=JmR0VSuJZenxo6Eg/SW/nQEeboRtbca0YpJASH+FhTmD+k/TOhHqCPJFlMAjyTj+k9fIAhhbJRkS+AStY+75qw==;EndpointSuffix=core.windows.net"  
    container_name = "wrdflklntrlntarget" 
    
    # Create a BlobServiceClient object  
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)  
    
    # Create a container client object  
    container_client = blob_service_client.get_container_client(container_name)  
    
    # Get a list of all blobs in the container  
    blob_list = container_client.list_blobs()  
    
    print("Files in Target Blob", blob_list)

    # Download each blob to local folder  
    for blob in blob_list:  
         
        #Getting the Target Container
        blob_client = container_client.get_blob_client(blob.name)
        #Getting the list of Blob in Target Container
        download_stream = blob_client.download_blob()
        #Storing the Byte Array to variable Content 
        content = download_stream.readall()
        #Returing the file to BlobToLocal
        return content

def DeleteBlobs() :
    # Define the connection string and container names  
    connect_str = "DefaultEndpointsProtocol=https;AccountName=flkdoctransln;AccountKey=JmR0VSuJZenxo6Eg/SW/nQEeboRtbca0YpJASH+FhTmD+k/TOhHqCPJFlMAjyTj+k9fIAhhbJRkS+AStY+75qw==;EndpointSuffix=core.windows.net"  
    source_container_name = "wrdflklntrlnsource"  
    target_container_name = "wrdflklntrlntarget"  
    
    # Create a BlobServiceClient object  
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)  
    
    # Delete all blobs in source container  
    source_container_client = blob_service_client.get_container_client(source_container_name)  
    source_blob_list = source_container_client.list_blobs()  
    for blob in source_blob_list:  
        source_container_client.delete_blob(blob.name)  
    
    # Delete all blobs in Target container  
    target_container_client = blob_service_client.get_container_client(target_container_name)  
    #Getting the list of all files in the Target Blob
    target_blob_list = target_container_client.list_blobs()  
    for blob in target_blob_list:  
        target_container_client.delete_blob(blob.name)

