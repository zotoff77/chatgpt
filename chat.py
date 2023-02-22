# Program to interface with ChatGPT
from tkinter import *
import customtkinter
import openai
import os
import pickle

#initiate app
root = customtkinter.CTk()
root.title("ChatGPT Bot")
root.geometry ('600x500')
root.iconbitmap('ai_lt.ico')

#Set color shcheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme ('dark-blue')

# Submit to ChatGPT
def speak():
    if chat_entry.get():
        # Post request to the chat window
        my_text.insert(END, f'You:\n {chat_entry.get()}\n\n')
        # Define filename
        filename = 'api_key'
        try:
            if (os.path.isfile(filename)):
                # Open the file
                input_file = open(filename, 'rb')

                # Load Data from the file to a variable
                stuff = pickle.load(input_file)

                # Query ChatGPT
                # Define our API key to ChatGPT
                openai.api_key = stuff

                # Create instance
                openai.Model.list()

                # Define our Query /Response
                response = openai.Completion.create(
                            model = 'text-davinci-003',
                            prompt=chat_entry.get(),
                            temperature=0, # specificity of the response - more higher
                            max_tokens=60, # limit text size of the reply
                            top_p=1.0,
                            frequency_penalty=0.0,
                            presence_penalty=0.0)
                my_text.insert(END, 'ChatGPT:\n')
                my_text.insert(END, (response['choices'][0]['text']).strip())
                my_text.insert(END, '\n\n')

            else:
                # Create the file
                input_file = open(filename, 'wb')

                # Close the file
                input_file.close()

                # Error message - API key is required!
                my_text.insert(END, '\n\n You need to provide an API key !!! \n Get one here:\n https://beta.openai.com/account/api-keys')
            #Resize app
            root.geometry('600x650')
            # Reshow API frame
            api_frame.pack(pady=30)
        except Exception as e:
            my_text.insert(END, f'\n\n There was an error \n\n {e}')

    else:
        my_text.insert(END, '\n\n Request is empty. Type something! :) ')

# Clear the screens
def clear():
    # Clear the main text box
    my_text.delete(1.0, END)

    # Clear the entry widget
    chat_entry.delete (0, END)

# Do API stuff
def key():
    # Define filename
    filename = 'api_key'
    try:
        if (os.path.isfile(filename)):
            # Open the file
            input_file = open(filename, 'rb')

            # Load Data from the file to a variable
            stuff = pickle.load(input_file)

            # Output stuff into the entry box
            api_entry.delete(0, END)
            api_entry.insert(END, stuff)
        else:
            # Create the file
            input_file = open(filename, 'wb')

            # Close the file
            input_file.close()
        #Resize app
        root.geometry('600x650')
        # Reshow API frame
        api_frame.pack(pady=30)
    except Exception as e:
        my_text.insert(END, f'\n\n There was an error \n\n {e}')


# Save the API Key
def save_key():
    # Define the filename
    file_name = 'api_key'

    try:
        # Open file
        output_file = open(file_name, 'wb')

        # reset the file
        output_file.truncate()

        # Add data to the file
        pickle.dump(api_entry.get(), output_file)
        
        
        # Hide API frame
        api_frame.pack_forget()
        # Resize App smaller
        root.geometry('600x500')
    except Exception as e:
        my_text.insert(END, f'\n\n There was an error \n\n {e}')

#Create text frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

#Add text widget for ChatGPT responses
my_text = Text(text_frame,
    bg='#343638',
    width=65,
    bd=1,
    fg='#d6d6d6',
    relief='flat',
    wrap=WORD,
    selectbackground='#1f538d')
my_text.grid(row=0, column=0)

#Create scroll bar for the text widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
    command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky='ns')

#Add scrollbar to the textbox
my_text.configure(yscrollcommand=text_scroll.set)

#Entry widget for typing
chat_entry = customtkinter.CTkEntry(root,
    placeholder_text = 'Type your request',
    width = 535,
    height = 50,
    border_width=1)
chat_entry.pack(pady=10)

# Create button Frame
button_frame = customtkinter.CTkFrame(root, fg_color='#242424')
button_frame.pack(pady=10)

# Create Submit button
submit_button = customtkinter.CTkButton(button_frame,
    text = 'Speak to ChatGPT',
    command=speak)
submit_button.grid(row=0, column=0, padx=25)

# Create Clear button
clear_button = customtkinter.CTkButton(button_frame,
    text = 'Clear Responses',
    command=clear)
clear_button.grid(row=0, column=1, padx=35)

# Create API button
api_button = customtkinter.CTkButton(button_frame,
    text = 'Update API key',
    command=key)
api_button.grid(row=0, column=2, padx=25)


# Add API Key Frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

#Add API Entry Widget
api_entry = customtkinter.CTkEntry(api_frame,
    placeholder_text="Enter Your API Key",
    width=350, 
    height=50,
    border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

# Add API Button
api_save_buton = customtkinter.CTkButton(api_frame,
    text='Save Key',
    command=save_key)
api_save_buton.grid(row=0, column=1, padx=10)

root.mainloop()