import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def getopenairesponse(all_chunks) :
    content=""
    try:
        # Set your Azure Cognitive Services API key and endpoint
        openai.api_type = os.getenv("AZURE_OPENAI_API_TYPE")
        openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION") 
        openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") # Your Azure OpenAI resource's endpoint value.
        openai.api_key = os.getenv("AZURE_OPENAI_KEY")
        openai_engine=os.getenv("AZURE_OPENAI_DEPLOYMENT")
        bot_message=[]
        # Define your conversation context and query
        context_template = f"""
        You are a chatbot for Fluke.com.
        Don't justify your answers. Don't give information not mentioned in the CONTEXT INFORMATION.
        Answer the QUESTION from the CONTEXT below only and follow the INSTRUCTIONS.

        CONTEXT :
        **************
        
        1. Here is the search context {all_chunks}.
        

        QUESTION : PL NO,INV NO,HSCODE,Date,Address,Tax No,Commodity,QTY,Unit,Unit Price,Total Amount,Commodity,G.W(KG),N.W(KG) from the context

        INSTRUCTIONS :
        1. Always provide response only from the CONTEXT.
        2. Provide the response in csv format.
        3. seperate the values using '|' pipe seperator symbol.
        4. Dont provide the columns provide only values
        """
        system_context = {
                        'role': 'system',
                        'content': context_template
                    }
        bot_message.append(system_context)
        # Make a request to the Conversational Agent
        response = openai.ChatCompletion.create(
            engine=openai_engine, # The deployment name you chose when you deployed the GPT-3.5-Turbo or GPT-4 model.
            messages=bot_message,
            frequency_penalty=0,
            n=1,  # Number of messages
            presence_penalty=0,
            temperature=0.0,
            top_p=1,  # Nucleus Sampling
        )
        print(response)
        # To print only the response content text:
        print(response['choices'][0]['message']['content'])
        content=response['choices'][0]['message']['content']
    except Exception as e:
        print(e)
    return content

def getopenaiarabicresponse(all_chunks) :
    content=""
    try:
        # Set your Azure Cognitive Services API key and endpoint
        openai.api_type = os.getenv("AZURE_OPENAI_API_TYPE")
        openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION") 
        openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") # Your Azure OpenAI resource's endpoint value.
        openai.api_key = os.getenv("AZURE_OPENAI_KEY")
        openai_engine=os.getenv("AZURE_OPENAI_DEPLOYMENT")
        bot_message=[]
        # Define your conversation context and query
        context_template = f"""
        You are a chatbot for Fluke.com.
        Don't justify your answers. Don't give information not mentioned in the CONTEXT INFORMATION.
        Answer the QUESTION from the CONTEXT below only and follow the INSTRUCTIONS.

        CONTEXT :
        **************
        
        1. Here is the search context {all_chunks}.
        

        QUESTION : Customer Tax Number,Customer Name,Payment,Invoice Date,Invoice number,Customer Mobile,Customer Code,City,Country,Item name,Description,Price,Quantity,Net Amount from the context

        INSTRUCTIONS :
        1. Always provide response only from the CONTEXT.
        2. Provide the response in csv format.
        3. seperate the values using '|' pipe seperator symbol.
        4. Dont provide the columns provide only values.
        5. Dont answer outside from the context
        """
        system_context = {
                        'role': 'system',
                        'content': context_template
                    }
        bot_message.append(system_context)
        # Make a request to the Conversational Agent
        response = openai.ChatCompletion.create(
            engine=openai_engine, # The deployment name you chose when you deployed the GPT-3.5-Turbo or GPT-4 model.
            messages=bot_message,
            frequency_penalty=0,
            n=1,  # Number of messages
            presence_penalty=0,
            temperature=0.0,
            top_p=0,  # Nucleus Sampling
        )
        print(response)
        # To print only the response content text:
        print(response['choices'][0]['message']['content'])
        content=response['choices'][0]['message']['content']
    except Exception as e:
        print(e)
    return content


def getopenaiimageresponse(all_chunks) :
    content=""
    try:
        # Set your Azure Cognitive Services API key and endpoint
        openai.api_type = os.getenv("AZURE_OPENAI_API_TYPE")
        openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION") 
        openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") # Your Azure OpenAI resource's endpoint value.
        openai.api_key = os.getenv("AZURE_OPENAI_KEY")
        openai_engine=os.getenv("AZURE_OPENAI_DEPLOYMENT")
        bot_message=[]
        # Define your conversation context and query
        context_template = f"""
        You are a chatbot for Fluke.com.
        Don't justify your answers. Don't give information not mentioned in the CONTEXT INFORMATION.
        Answer the QUESTION from the CONTEXT below only and follow the INSTRUCTIONS.

        CONTEXT :
        **************
        
        1. Here is the search context {all_chunks}.
        

        QUESTION : Receiver Name,Receiver Country, Receiver Location,Description,Country,Order Number,QTY,Gross Weight,Volume from the context

        INSTRUCTIONS :
        1. Always provide response only from the CONTEXT.
        2. Provide the response in csv format.
        3. seperate the values using '|' pipe seperator symbol.
        4. Dont provide the columns provide only values.
        5. Dont answer outside from the context
        """
        system_context = {
                        'role': 'system',
                        'content': context_template
                    }
        bot_message.append(system_context)
        # Make a request to the Conversational Agent
        response = openai.ChatCompletion.create(
            engine=openai_engine, # The deployment name you chose when you deployed the GPT-3.5-Turbo or GPT-4 model.
            messages=bot_message,
            frequency_penalty=0,
            n=1,  # Number of messages
            presence_penalty=0,
            temperature=0.0,
            top_p=0,  # Nucleus Sampling
        )
        print(response)
        # To print only the response content text:
        print(response['choices'][0]['message']['content'])
        content=response['choices'][0]['message']['content']
    except Exception as e:
        print(e)
    return content