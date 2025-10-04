# simple_email_agent
# AI Email Agent

An intelligent email assistant that automatically analyzes, classifies, summarizes, and drafts replies to emails using AI.

## Features

- 🔍 Detects urgent emails automatically
- 📊 Classifies emails (Work, Personal, Spam, Other)
- 📝 Creates 2-3 sentence summaries
- ✍️ Drafts professional replies
- 🔔 Real-time notifications for urgent emails

## Installation

1. **Clone or download this project**

2. **Install Python packages:**
```bash
pip install crewai crewai-tools python-dotenv
```

3. **Create `.env` file and add your API key:**
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

## Usage

Run the agent:
```bash
python agent.py
```

## Example

**Input:**
```
Hello,
Urgent meeting tomorrow at 3PM to discuss the project.
Please confirm.
```

**Output:**
```
Summary: Meeting requested for tomorrow at 3PM to discuss project with confirmation needed.

Classification: Work

Draft Reply: Hello, thank you for reaching out. I confirm my availability 
for tomorrow at 3PM. Looking forward to the meeting.

Notification: 🚨 IMPORTANT EMAIL ALERT: Urgent meeting tomorrow
```

## How to Process Your Own Emails

Edit `agent.py` and change the email content:

```python
your_email = """
Your email content here
"""

result = assistant.process_email(your_email)
print(assistant.format_output(result))
```

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection

## Project Structure

```
email-agent/
├── agent.py           # Main code (run this)
├── .env               # Your API key (create this)
├── requirements.txt   # Dependencies
└── README.md         # This file
```

## Cost

Each email costs approximately $0.02-0.05 using GPT-3.5 or $0.10-0.20 using GPT-4.

## Troubleshooting

**Error: "No module named 'crewai'"**
```bash
pip install crewai crewai-tools
```

**Error: "OpenAI API key not found"**
- Make sure you created `.env` file
- Check that it contains: `OPENAI_API_KEY=openai_api_key_here

**Processing takes 20+ seconds**
- This is normal! AI processing takes time

## License

MIT License - feel free to use and modify!

## Support

If you have questions, create an issue on GitHub or contact me.

---

Made with ❤️ using CrewAI
