from transformers import pipeline

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"


try:
    summarizer = pipeline("summarization", model=MODEL_NAME)
except Exception as e:
    print(f"Error loading model {MODEL_NAME}: {e}")
    summarizer = None


def summarize_text(text, max_length=130, min_length=30):
    if summarizer is None:
        return text

    input_length = len(text.split())
    if input_length < max_length:
        max_length = max(10, input_length // 2 + 5)  # dynamic adjustment

    result = summarizer(
        text,
        max_length=max_length,
        min_length=min_length if min_length < max_length else max_length - 5,
        do_sample=False
    )
    return result[0]["summary_text"]
