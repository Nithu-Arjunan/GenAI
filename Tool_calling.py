import os
import requests
from langchain_groq import ChatGroq
from langchain_core.tools import tool

# Set API keys

os.environ["GROQ_API_KEY"] = "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"  
WEATHER_API_KEY = "014864fc61e34118ac3113709253005" 


# Creat third party tools

@tool
def get_current_weather(location: str) -> dict:
    """Get current weather for a location from WeatherAPI.com."""
    
    url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": WEATHER_API_KEY, "q": location}
    response = requests.get(url, params=params)
    return response.json()

# Step3 : Bind to model

# Bind tool to model
llm = ChatGroq(model="llama3-70b-8192", temperature=0)
model_with_tools = llm.bind_tools([get_current_weather])

# Ask a question
user_input = "What's the weather in Kerala tomorrow?"
response = model_with_tools.invoke(user_input)
print(response)

# Step4 : Tool + LLM call

if hasattr(response, "tool_calls") and response.tool_calls:
    print("\n📥 Tool Call JSON:")
    print(response.tool_calls)

    for call in response.tool_calls:
        tool_name = call["name"]
        args = call["args"]
        
        # Run the tool and return raw JSON
        if tool_name == "get_current_weather":
            tool_result = get_current_weather.invoke(args)
            print("\n🔧 Tool Execution Result (Raw JSON):")
            print(tool_result)
else:
    print("\n💬 No tool was called. Response:")
    print(response.content)