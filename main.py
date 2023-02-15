#!/usr/bin/python

import os
import openai

openai.organization = "org-jOA7rNNtj8vYONYLWZ6egAU0"
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)

print (response)
