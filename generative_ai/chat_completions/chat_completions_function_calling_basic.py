# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# TODO: Delete this file after approval generative_ai/function_calling/chat_function_calling_basic.py


def generate_text(project_id: str, location: str = "us-central1") -> object:
    # [START generativeaionvertexai_gemini_chat_completions_function_calling_basic]
    import vertexai
    import openai

    from google.auth import default, transport

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # location = "us-central1"

    vertexai.init(project=project_id, location=location)

    # Programmatically get an access token
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    auth_request = transport.requests.Request()
    credentials.refresh(auth_request)

    # # OpenAI Client
    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/{location}/endpoints/openapi",
        api_key=credentials.token,
    )

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA or a zip code e.g. 95616",
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    messages = []
    messages.append(
        {
            "role": "system",
            "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.",
        }
    )
    messages.append({"role": "user", "content": "What is the weather in Boston?"})

    response = client.chat.completions.create(
        model="google/gemini-1.5-flash-001",
        messages=messages,
        tools=tools,
    )

    print(response)
    # [END generativeaionvertexai_gemini_chat_completions_function_calling_basic]

    return response
