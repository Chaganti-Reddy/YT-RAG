# transcript_loader.py

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from deep_translator import GoogleTranslator

def translate_text(text, target="en"):
    try:
        return GoogleTranslator(source="auto", target=target).translate(text)
    except Exception as e:
        print(f"⚠️ Translation failed: {e}")
        return text  # Fallback to original if translation fails

def get_transcript_with_language_selection(video_id: str, preferred_language: str = "en"):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        all_transcripts = list(transcript_list)

        for transcript in all_transcripts:
            if transcript.language_code == preferred_language:
                print(f"✅ Found preferred language: {preferred_language}")
                fetched = transcript.fetch()
                text = " ".join([x.text for x in fetched])
                return text, preferred_language

        # Preferred language not found
        available_languages = [t.language_code for t in all_transcripts]
        print("⚠️ Preferred not found. Available:", available_languages)

        # Just fetch the first available and translate it
        selected = all_transcripts[0]
        fetched = selected.fetch()
        text = " ".join([x.text for x in fetched])
        translated_text = translate_text(text)

        print(f"🔄 Translated from {selected.language_code} to en")
        return translated_text, selected.language_code

    except TranscriptsDisabled:
        print("🚫 Transcripts are disabled for this video.")
        return None, []

    except NoTranscriptFound:
        print("🚫 No transcripts found.")
        return None, []

    except Exception as e:
        print(f"⚠️ Error while fetching transcript: {e}")
        return None, []

