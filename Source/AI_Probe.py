# AI_Probe
# Author Stephen Witty switty@level500.com
# 9-9-23
# Test uniqueness of GPT responses
#
# Example code from rollbar.com - GPT example
#
# V1 9-9-23 - Initial release / dev
# V2 9-10-23 - Correct prompt constant
# V3 9-11-23 - Put in GPT timeout and corrected error bug
#
# Notes - Add your OpenAI key below

import openai
import time
import sys
import os
import random

# Put OpenAI API key here
openai.api_key = "XXXXXXXXXXXXXXXXXXXXXXXXX"

# Uncomment GPT model desired here
gpt_model='gpt-3.5-turbo'
#gpt_model = "gpt-4"

###################### Constants ##########################################################
NUMBER_OF_CYCLES = 150                                  # Number of cycles to run before exiting
GPT_RETRY_LIMIT = 25                                    # Number of times to retry GPT if errors occur
PROMPT = "Create a sentence about a girl and her dog."  # GPT prompt

########## This function creates the AI prompt #######
def create_gpt_prompt():

   prompt_message = PROMPT

   return prompt_message

########### This function formats an output string ####################
def print_string(string):
   cnt = 0
   for char in string:
      if not (char == " " and cnt == 0):
         print(char, end = "")
         cnt = cnt + 1
      if (cnt > 115 and char == " "):
         print()
         cnt = 0
   print()
   sys.stdout.flush()

############### Function - Call ChatGPT #########################################
def call_gpt(prompt_message):
   try:
      response = openai.ChatCompletion.create(model=gpt_model, messages=[ {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt_message}],request_timeout=15)
   except Exception as e:
      return False, "", "WARNING:  System Error during ChatGPT call: " + str(e)

   return True, response.choices[0]["message"]["content"], ""

###############  Start of main routine ##############################################################
number_of_cycles = 0
answer_history = []
duplicate = 0
duplicate_history = []
time_history = []
max_time = 0
min_time = 9999999999
gpt_errors = 0
min_words = 999999999
max_words = 0
word_history = []

while(number_of_cycles < NUMBER_OF_CYCLES): # Main loop to run prompts

   # Create GPT prompt
   prompt = create_gpt_prompt()

   print("\n************************************** GPT Prompt ********************")
   print_string(prompt)

   retry_count = 0
   success = False # Keep running prompt until we get a valid answer to check

   while (not success):

      if (retry_count == GPT_RETRY_LIMIT):
         print("\n\nERROR: Too many GPT errors, exiting\n")
         sys.exit()

      store_time = time.time()

      success, gpt_reply, error_text = call_gpt(prompt) # Call GPT, retry if error
      if (not success):
         print(error_text)
         retry_count = retry_count + 1
         gpt_errors = gpt_errors + 1
         continue

      final_time = time.time() - store_time
      time_history.append(final_time)
      if (max_time < final_time):
         max_time = final_time
      if (min_time > final_time):
         min_time = final_time

      number_of_words = len(gpt_reply.split())
      if (max_words < number_of_words):
         max_words = number_of_words
      if (min_words > number_of_words):
         min_words = number_of_words
      word_history.append(number_of_words)

      print("\n*************** GPT Answer *****************")
      print_string(gpt_reply)
      if (gpt_reply in answer_history):
         print("\nFOUND DUPLICATE.........")
         duplicate = duplicate + 1
         duplicate_history.append(gpt_reply)
      else:
         answer_history.append(gpt_reply)

   number_of_cycles = number_of_cycles + 1
   print("\nTotal cycles: " + str(number_of_cycles) + " Number of duplicates: " + str(duplicate))

avg_time = 0
for i in time_history:
   avg_time = avg_time + i
avg_time = avg_time / number_of_cycles

avg_words = 0
for i in word_history:
   avg_words = avg_words + i
avg_words = avg_words / number_of_cycles

print("\nFinal report **************************************")
print("GPT Test Prompt: " + PROMPT)
print("\nFirst 5 non duplicate answers **********")
for i in range(0,5,1):
   print(answer_history[i])

print("\nNumber of cycles: " + str(number_of_cycles))
print("GPT Errors: " + str(gpt_errors))
print("GPT prompt min time in seconds: " + str(round(min_time,2)))
print("GPT prompt max time in seconds: " + str(round(max_time,2)))
print("GPT average prompt time in seconds: " + str(round(avg_time,2)))
print("Max words in a reply: " + str(max_words))
print("Min words in a reply: " + str(min_words))
print("Average words in a reply: " + str(round(avg_words,2)))
print("Duplicate replies: " + str(duplicate))

if (duplicate > 0):
   print("\nDuplicate answers ***********")
   for i in duplicate_history:
      print(i)

print("\n")
