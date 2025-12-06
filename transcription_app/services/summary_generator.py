from transformers import pipeline
import json

_generator = None


def get_generator():
    global _generator
    if _generator is None:
        # lazy load
        _generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base"
        )
    return _generator


def generate_structured_summary(text: str):
    generator = get_generator()

    prompt = (
        "Read this meeting transcript and extract:\n"
        "1. Key Points\n"
        "2. Decisions Made\n"
        "3. Risks or Concerns\n"
        "4. Deadlines or Timelines\n\n"
        "Transcript:\n"
        f"{text}\n\n"
        "Return JSON with keys: key_points, decisions, risks, deadlines, full_summary."
    )

    output = generator(prompt, max_length=512)[0]["generated_text"]

    try:
        data = json.loads(output)
    except:
        data = {
            "key_points": [],
            "decisions": [],
            "risks": [],
            "deadlines": [],
            "full_summary": output,
        }

    return data
