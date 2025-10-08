# Research Agent

A simple AI research assistant built using LangChain and Anthropic's Claude model.  
It can perform web searches, query Wikipedia, and save research summaries to a text file.

## Features

- Search the web via DuckDuckGo.
- Query Wikipedia for quick summaries.
- Save structured research data to a file.
- Outputs structured JSON suitable for further processing.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/JureLovric/research-agent.git
cd research-agent
```
2. Create a virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

```
3. Create a .env file and add your API keys:
```
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

```

## Usage

Enter your research query when prompted, and the agent will:

- Search for information.

- Summarize the findings.

- Save the results to research_output.txt.


## Project Structure

- main.py – Main script to run the agent.

- tools.py – Contains web search, Wikipedia, and save-to-file tools.

- .env – Your API keys (should be ignored by git).

## Notes
- Make sure .env is in your .gitignore.

- Designed for experimentation and learning with LangChain and Claude.

#License
MIT
