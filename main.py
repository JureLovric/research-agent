from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from typing import List
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str = Field(..., description="Kratka tema istraživanja.")
    summary: str = Field(..., description="Detaljan sažetak svih pronađenih informacija.")
    sources: List[str] = Field(..., description="Lista URL-ova ili referenci korištenih za sažetak.")
    tools_used: List[str] = Field(..., description="Lista imena alata korištenih za prikupljanje podataka (npr., 'wikipedia', 'search_tool').")
    
llm = ChatAnthropic(model="claude-3-haiku-20240307")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools. 
            
            When the user asks to 'save to file', you must first gather the information 
            using the search/wiki tools, and then call the 'save_tool' with the final
            structured JSON output (ResearchResponse Pydantic model) as the argument.
            
            When the task is complete, **you must output the final answer only as a JSON object** that adheres exactly to this Pydantic format. Do not include any other text outside the JSON.
            {format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can i help you research? ")
raw_response = agent_executor.invoke({"query": query})

try:
    output_list = raw_response.get("output")
    
    if not output_list or not isinstance(output_list, list):
        raise ValueError("Konačni izlaz agenta je prazan ili neispravan.")
    
    json_string = output_list[0].get("text")
    
    if not json_string:
        raise ValueError("Pronađen je element u izlazu, ali je ključ 'text' prazan.")
    
    structured_response = parser.parse(json_string) 
    
    print("\n--- Parsed Structured Response ---")
    print(structured_response)
    
except Exception as e:
    print("\n--- Greška prilikom parsiranja konačnog odgovora ---")
    print("Error parsing response:", e) 
    print("Raw Response:", raw_response) 
    if 'json_string' in locals():
        print("Attempted JSON String:", json_string)