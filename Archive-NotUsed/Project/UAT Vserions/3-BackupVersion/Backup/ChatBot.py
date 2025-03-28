import tkinter as tk
from transformers import pipeline

# Load a pre-trained model for text generation (GPT-2, GPT-3 via OpenAI API or GPT-4 could be used for better performance)
chatbot = pipeline("text-generation", model="gpt2")

def chatbot_response(user_input):
    # Accessing the tokenizer and model directly from the pipeline object
    model = chatbot.model
    tokenizer = chatbot.tokenizer

    # Encoding the user input
    input_ids = tokenizer.encode(user_input, return_tensors='pt')

    # Generating a response using the model's generate method with adjusted parameters
    response = model.generate(
        input_ids=input_ids,
        max_length=150,  # Increased max length for more meaningful responses
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,  # Ensuring padding with the EOS token
        temperature=0.7,  # Control randomness of the model's responses (higher is more random)
        top_p=0.9,  # Use nucleus sampling for more diverse responses
        top_k=50,  # Use top-k sampling to restrict to the top 50 words
    )

    # Decode the response and return the generated text
    generated_text = tokenizer.decode(response[0], skip_special_tokens=True)
    
    return generated_text

def on_send_message():
    user_input = entry.get()  # Get the user's input from the entry box
    
    if user_input.lower() == "bye":
        root.quit()  # Close the chat window if the user types 'bye'
    else:
        # Display the user's message
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"You: {user_input}\n")
        
        # Get chatbot response
        response = chatbot_response(user_input)
        
        # Display the chatbot's response
        chat_box.insert(tk.END, f"Chatbot: {response}\n\n")
        
        # Automatically scroll to the bottom
        chat_box.yview(tk.END)
        
        # Clear the entry box after sending the message
        entry.delete(0, tk.END)

# Setting up the Tkinter window
root = tk.Tk()
root.title("Chatbot by Mohamed")

# Create a label
label = tk.Label(root, text="Chat with the Bot!", font=("Arial", 14))
label.pack(pady=10)

# Create a Text widget for displaying the conversation
chat_box = tk.Text(root, font=("Arial", 12), width=60, height=20, wrap=tk.WORD, state=tk.DISABLED)
chat_box.pack(pady=10)

# Create an entry box to type the message
entry = tk.Entry(root, font=("Arial", 12), width=50)
entry.pack(pady=10)

# Create a send button to send the message
send_button = tk.Button(root, text="Send", font=("Arial", 12), command=on_send_message)
send_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
