import os

# Set Hugging Face cache to the current script directory
os.environ["HUGGINGFACE_HUB_CACHE"] = os.path.join(os.getcwd(), "hf_cache")

from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")


# Save the model locally for offline use.
model.save_pretrained("./local_model")
tokenizer.save_pretrained("./local_model")