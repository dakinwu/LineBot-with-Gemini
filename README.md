# MCP News Search

A powerful news search and analysis tool built with MCP (Machine Conversation Protocol) that combines Google News API and Google's Gemini AI to provide intelligent news insights.

## Features

- 🔍 Smart news search with related keywords generation
- 🤖 AI-powered news analysis using Google's Gemini model
- 🌐 Multi-language support (default: Traditional Chinese)
- 📊 Customizable search parameters (time period, result count)
- 📝 Concise news insights in Traditional Chinese

## Requirements

- Python >= 3.11
- MCP CLI
- Google News API
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mcp-project.git
cd mcp-project
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables:
Create a `.env` file in the `src` directory with your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

Run the MCP server:
```bash
python src/news_server.py
```

The server provides a `search_news` tool with the following parameters:
- `keyword`: Search term (required)
- `language`: Language code (default: "zh-TW")
- `period`: Time period (default: "2d" for 2 days)
- `max_results`: Number of results to return (default: 4)

## How It Works

1. The system first uses Gemini AI to generate related keywords based on the search term
2. It then searches Google News using both the original and related keywords
3. For each news article found, it generates an AI-powered insight in Traditional Chinese
4. Results are returned as a JSON string containing titles, links, publication dates, descriptions, and AI-generated insights

## License

[Your chosen license]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 