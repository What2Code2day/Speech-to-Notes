import time
import openai
import os
import math

openai.api_key = "Enter OpenAI token"
try:
    os.remove("final.txt")
    os.remove("notes.md")
except:
    pass
with open("audio.txt", "r") as file:
    script = file.read()
length_output = len(script) 
print(length_output)

new_script = []
final_prompt = []
final_before = ""
list_output = script.split()
how_many_run = math.ceil(len(list_output)/750)
if len(list_output) > 500:
    for i in range(how_many_run):
        new_string = ' '.join(list_output[0:751])
        del list_output[0:751]
        print(str(round(((i+1)/how_many_run)*100))+ "%")
        print('-----------------------------------------------------------------------')
        if i == 0:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Please fix the errors and write a 300 word summary. It should be easy to understand and extract important points from. input: {new_string}",
                temperature=0.7,
                max_tokens=800,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
        else:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Add the most important points of this text into a new piece of text. This new piece of text should have the same amount of detail as the previous but should be only around 500 words: {final_before}",
                temperature=0.7,
                max_tokens=800,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
        ai_output = response.choices[0].text
        
        final_prompt.append(ai_output)
        with open("final.txt", "w") as file:
            file.write(ai_output+"\n")
        with open('final.txt', "r") as file:
            final_before = file.read()

        time.sleep(3)
if len(final_before.split()) >= 900:
    response = openai.Completion.create(
            model="text-curi-003",
            prompt=f"Please fix the errors and write a 700 word summary keeping the most important facts like statistics, etc, it should be easy to understand and extract important points from. input: {final_before}",
            temperature=0.7,
            max_tokens=800,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
    )
    ai_output = response.choices[0].text 
    final_prompt.append(ai_output)
    with open("final.txt", "w") as file:
        file.write(ai_output+"\n")

print('Starting...')
print('-----------------------------------------------------------------------')
response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"turn this into detailed bullet points and use of markdown for better formatting. making sure to retain as much detail as possible as they should be good enough to study for a test with: {final_before}",
        temperature=0.7,
        max_tokens=900,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
)
print(response.choices[0].text)
with open("notes.md", "w") as file:
    file.write(response.choices[0].text)

print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
