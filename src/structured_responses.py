from pydantic import BaseModel
from google.genai import Client
from google.genai.types import (
    GenerateContentConfig, 
    Tool,
    FunctionDeclaration,
    Content,
    Part,
)
from system_prompt import prompt
from pydantic_ai import format_as_xml
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = Client(api_key=api_key)

class GetTemperatureParams(BaseModel):
    city: str
    scale: str  

def get_temperature(city: str, scale: str) -> float:
    return 25.0

def get_humidity(city: str) -> float:
    return 60.0

def get_wind_speed(city: str) -> float:
    return 10.0

tools = [
    Tool(function_declarations=[FunctionDeclaration.from_callable(client=client, callable=get_temperature)]),
    Tool(function_declarations=[FunctionDeclaration.from_callable(client=client, callable=get_humidity)]),
    Tool(function_declarations=[FunctionDeclaration.from_callable(client=client, callable=get_wind_speed)]),
]

# config for the content generation, including the system prompt and tools
config = GenerateContentConfig(
    system_instruction=format_as_xml(prompt),
    tools=tools,
)
# first content is the user query
user_content = Content(
    role="user",
    parts=[Part.from_text(text="¿Cuál es la temperatura en El Salvador, Chile?")],
)

# api call to generate content, passing the config and the user query
response = client.models.generate_content(
    config=config,
    model="gemini-2.5-flash",
    contents=[user_content],
)

function_response_parts = []

for part in response.candidates[0].content.parts:
    if part.function_call:
        print("Function Call name:", part.function_call.name)
        print("Function Call Args:", part.function_call.args)
        result = None

        if part.function_call.name == "get_temperature":
            city = part.function_call.args["city"]
            scale = part.function_call.args["scale"]
            result = get_temperature(city, scale)
        
        if part.function_call.name == "get_humidity":
            city = part.function_call.args["city"]
            result = get_humidity(city)
        
        if part.function_call.name == "get_wind_speed":
            city = part.function_call.args["city"]
            result = get_wind_speed(city)

        # create a new part with the function response 
        function_response_part = Part.from_function_response(
            name=part.function_call.name, 
            response={"result": result}
            )

        # append the function response part to the list of function response parts
        function_response_parts.append(function_response_part)

    else:
        print("Content:", part.text)

# create a new content with the function response part and the original user query, and pass it to the model again to generate a final response
contents = [
    user_content,
    Content(role="model", parts=[part]),
    Content(role="user", parts=[function_response_part]),
]

# api call to generate content, passing the config and the new content with the function response
response2 = client.models.generate_content(
    config=config,
    model="gemini-2.5-flash",
    contents=contents,
)

print("Final Response: ", response2.text)