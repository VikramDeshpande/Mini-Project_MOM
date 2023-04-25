import json
import re
import torch
from transformers import BartTokenizer, BartForConditionalGeneration
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

def main_bart(conversation, summary_length):
  
  # Load model and tokenizer
  tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
  model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

  desired_length = min(summary_length, len(conversation.split())/4)
     
  # people = set([name.strip() for name in re.findall("([A-Z][a-z]*):", conversation)])

  # # Prompt user for which person to add a templating for
  # print("The following people were found in the conversation:")
  # print(", ".join(people))
  # name = input(f"Which person's pronoun would you like to template? Choose from {', '.join(people)}: ")

  # # Get pronoun to use for the selected person
  # pronoun = "he/she" if re.search(f"{name}:", conversation).group(0)[0] == "H" else "him/her"

  # # Replace the selected person's name with a pronoun in the conversation
  # conversation = re.sub(f"{name}:", pronoun, conversation)

  # Generate summary
  max_length = int(desired_length * 1.2) # Set maximum length to 120% of desired length
  min_length = int(desired_length * 0.9) # Set minimum length to 90% of desired length
  summary_ids = model.generate(tokenizer.encode(conversation, truncation=True, return_tensors='pt'), max_length=max_length, min_length=min_length, num_beams=4, no_repeat_ngram_size=2, early_stopping=True)
  summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

  # Replace pronoun with the selected person's name in the generated summary
  # summary = re.sub(f"{pronoun}", name, summary)

  # Split the summary into individual sentences and add bullet points
  main_summary = "\n\nMain Points:\n"
  for i, sentence in enumerate(summary.split(".")):
      if sentence.strip() != "":
          main_summary += f"\n{i+1}. {sentence.strip()}."

  # Get intro summary
  intro_length = min(int(len(summary) * 0.3), desired_length) # Set intro summary length to minimum of 30% of main summary length and desired length
  intro_ids = model.generate(tokenizer.encode(summary, truncation=True, return_tensors='pt'), max_length=intro_length, num_beams=2, no_repeat_ngram_size=2, early_stopping=True)
  intro_text = tokenizer.decode(intro_ids[0], skip_special_tokens=True)

  # Get conclusion summary
  # conclusion_length = min(int(len(summary) * 0.5), desired_length) # Set conclusion summary length to minimum of 30% of main summary length and desired length
  # conclusion_ids = model.generate(tokenizer.encode(summary[-conclusion_length:], truncation=True, return_tensors='pt'), max_length=conclusion_length, num_beams=2, no_repeat_ngram_size=2, early_stopping=True)
  # conclusion_text = tokenizer.decode(conclusion_ids[0], skip_special_tokens=True)

  # Add template
  main_points = main_summary

  # Print template with summary and conclusion
  output_text = f"\nIntro:\n{intro_text}{main_points}\n"
  print(output_text)
  return output_text

