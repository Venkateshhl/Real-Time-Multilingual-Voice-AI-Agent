import openai
import json
from agent.prompt.prompt import SYSTEM_PROMPT
from agent.tools.tools import call_tool

def process_request(user_text, language, context):
    prompt = SYSTEM_PROMPT.format(
        user_input=user_text,
        language=language,
        context=json.dumps(context)
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=200
        )
        content = response['choices'][0]['message']['content']
        # Try to parse as JSON
        result = json.loads(content)
        # Call the appropriate tool
        tool_response = call_tool(result)
        return tool_response
    except json.JSONDecodeError:
        # If not JSON, return as text response
        return content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"