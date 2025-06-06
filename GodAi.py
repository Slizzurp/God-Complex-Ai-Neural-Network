# GodAi v1 - Advanced AI Chatbot with Memory and Deep Learning Integration
# Developed by Mirnes
# License: MIT

import tkinter as tk
from tkinter import font
import json
import openai  # If using OpenAI's API for responses
import threading  # To prevent UI freeze during AI processing

# Load Knowledge Base (Q&A Database)
with open('answers.json', 'r') as f:
    answers_db = json.load(f)

# UI Setup
root = tk.Tk()
root.title("GodAi v1")
root.configure(bg='white')

# Set UI Fonts
app_font = font.Font(family="Franklin Gothic", size=11)
root.option_add("*Font", app_font)
root.option_add("*Background", "white")
root.option_add("*Foreground", "black")

# Create UI Elements
chat_display = tk.Text(root, width=80, height=20, bg="white", fg="black", state='disabled')
chat_display.pack(padx=10, pady=10)
user_entry = tk.Entry(root, width=60)
user_entry.pack(side=tk.LEFT, padx=10, pady=5)
send_btn = tk.Button(root, text="Send", command=lambda: threading.Thread(target=send_message).start())
send_btn.pack(side=tk.LEFT, padx=5, pady=5)

# Function to Handle AI Responses
def get_ai_response(query):
    """Check if question exists in knowledge base, otherwise use AI model"""
    for category in answers_db.values():
        if query in category:
            return category[query]  # Return pre-written answer
    
    # If no pre-written answer, use AI model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are GodAi, a morality-based AI assistant."},
                  {"role": "user", "content": query}]
    )
    return response['choices'][0]['message']['content']

# Function to Send User Message
def send_message():
    query = user_entry.get().strip()
    if query:
        chat_display.config(state='normal')
        chat_display.insert(tk.END, "You: " + query + "\n")
        chat_display.config(state='disabled')
        user_entry.delete(0, tk.END)
        
        # Get AI response
        response = get_ai_response(query)
        
        # Display AI response
        chat_display.config(state='normal')
        chat_display.insert(tk.END, "GodAi: " + response + "\n\n")
        chat_display.config(state='disabled')
        chat_display.see(tk.END)

# Run Application
root.mainloop()