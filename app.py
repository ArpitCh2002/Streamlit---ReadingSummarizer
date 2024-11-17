import streamlit as st
from PyPDF2 import PdfReader
from newspaper import Article
import openai
from gtts import gTTS
from io import BytesIO

# Set up OpenAI API key
openai.api_key = "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"  # Replace with your actual API key

st.title("PDF/Summarizer with Audio Option")

# Select input type
option = st.radio("Choose input type:", ("PDF Upload", "Article URL"))

# Handle PDF or URL input
text = ""
if option == "PDF Upload":
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        text = "".join(page.extract_text() for page in pdf_reader.pages)
elif option == "Article URL":
    url = st.text_input("Enter the article URL")
    if url:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text

# Summarize and generate bullet points using OpenAI
if text:
    # Edit response as per required summary
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=(
        "You are an expert summarizer. Summarize the following text using the "
        "structure provided below. Ensure the summary is concise, clear, and adheres to the format:\n\n"
        "Format:\n"
        "- **Overview**: Provide a brief 5-6 sentence summary of the document with word range of 250-300 words\n"
        "- **Main Sections**: Summarize the key sections in 10 bullet points, focusing on important details. Make sure that these details cover all the major talking points of the reading/article\n"
        "- **Actionable Insights**: List the key takeaways, insights, or conclusions from the text.\n\n"
        "- **Discussion Points**: At the end of all, give a small paragraph of 100 words that one can share as what he understood from the article and that can be shared with others showing what you understood from that reading/article.\n\n"
        f"Text to summarize:\n{text}"
    ),
        temperature=0.5,
        max_tokens=400
    )
    summary = response.choices[0].text.strip()

    st.subheader("Summary")
    st.write(summary)

    # Convert summary to audio
    tts = gTTS(text=summary)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)

    # Display audio player and download options
    st.audio(audio_bytes, format="audio/mp3")
    st.download_button("Download Summary as Text", data=summary, file_name="summary.pdf")
    st.download_button("Download Audio", data=audio_bytes, file_name="summary.mp4", mime="audio/mp4")
