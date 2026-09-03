import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from rag import retrieve_context
import json

from tools import (
    search_knowledge,
    get_course_info,
    calculate_fee
)

load_dotenv()

client=Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message:str

@app.get("/")
def home():
    return{
        "message":"AI  Institute Assistant API is running"
    }

@app.post("/chat")
def chat(request: ChatRequest):

    answer = run_agent(
        request.message
    )

    return {
        "reply": answer
    }

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search institute documents for information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Question to search in institute documents"
                    }
                },
                "required": ["question"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_course_info",
            "description": "Get details about an institute course.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_name": {
                        "type": "string"
                    }
                },
                "required": ["course_name"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_fee",
            "description": "Calculate combined fee for two courses.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course1": {
                        "type": "string"
                    },
                    "course2": {
                        "type": "string"
                    }
                },
                "required": ["course1", "course2"]
            }
        }
    }
]

def execute_tool(function_name, arguments):

    if function_name == "search_knowledge":

        return search_knowledge(
            arguments["question"]
        )

    elif function_name == "get_course_info":

        return get_course_info(
            arguments["course_name"]
        )

    elif function_name == "calculate_fee":

        return calculate_fee(
            arguments["course1"],
            arguments["course2"]
        )

    return {
        "error": f"Unknown tool: {function_name}"
    }


def run_agent(user_message):

    messages = [
        {
            "role": "system",
            "content": """
You are SmartLearn Institute's AI Agent.

Your job is to help students with institute-related
questions.

You have access to tools.

Rules:

1. Decide whether a tool is needed.
2. Use tools when accurate institute information is required.
3. You can use multiple tools.
4. After receiving a tool result, decide whether another
   tool is required.
5. Never invent institute information.
6. If information cannot be found, clearly say so.
7. Give a concise and friendly final answer.
"""
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    # Agent loop
    for step in range(5):

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # Agent has finished
        if not assistant_message.tool_calls:

            return assistant_message.content

        # Add agent decision to conversation
        messages.append(
            assistant_message
        )

        # Execute tools
        for tool_call in assistant_message.tool_calls:

            function_name = (
                tool_call.function.name
            )

            arguments = json.loads(
                tool_call.function.arguments
            )

            print(
                f"Agent selected tool: {function_name}"
            )

            print(
                f"Arguments: {arguments}"
            )

            result = execute_tool(
                function_name,
                arguments
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                }
            )

    return "I was unable to complete the request."