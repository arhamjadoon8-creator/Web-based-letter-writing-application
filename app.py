
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Smart Letter & Word Assistant",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Smart Letter & Word Assistant")
st.write("Generate professional letters/applications from simple hints and find word meanings.")

# Get API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

tab1, tab2 = st.tabs(["📄 Letter/Application Writer", "📚 Word Meaning"])

# -------------------------------
# TAB 1 - LETTER WRITER
# -------------------------------

with tab1:

    st.header("Letter / Application Writer")

    department = st.text_input(
        "Department / Organization",
        placeholder="Example: Education Department"
    )

    recipient = st.text_input(
        "Recipient",
        placeholder="Example: Director Education"
    )

    hints = st.text_area(
        "Enter your hints",
        placeholder="""
Example:
Need 3 days leave
family emergency
from 18 September
employee ID 1234
"""
    )

    tone = st.selectbox(
        "Select tone",
        [
            "Professional",
            "Formal",
            "Polite",
            "Simple",
            "Request",
            "Complaint"
        ]
    )

    language = st.selectbox(
        "Language",
        ["English", "Urdu"]
    )

    if st.button("Generate Letter", type="primary"):

        if not hints:
            st.warning("Please enter some hints.")

        else:

            prompt = f"""
You are a professional letter and application writer.

Write a complete {tone.lower()} application or official letter.

Department/Organization:
{department}

Recipient:
{recipient}

User hints:
{hints}

Language:
{language}

Requirements:
- Convert the short hints into a complete professional letter.
- Use clear and respectful language.
- Add an appropriate subject.
- Add proper salutation.
- Organize the information logically.
- Do not invent unnecessary facts.
- End with an appropriate closing.
"""

            try:

                response = client.responses.create(
                    model="gpt-5.6",
                    input=prompt
                )

                result = response.output_text

                st.subheader("Generated Letter")

                st.text_area(
                    "Result",
                    value=result,
                    height=400
                )

            except Exception as e:
                st.error(f"Error: {e}")


# -------------------------------
# TAB 2 - WORD MEANING
# -------------------------------

with tab2:

    st.header("Word Meaning")

    word = st.text_input(
        "Enter a word",
        placeholder="Example: diligent"
    )

    meaning_language = st.selectbox(
        "Meaning language",
        ["English", "English + Urdu"]
    )

    if st.button("Find Meaning"):

        if not word:
            st.warning("Please enter a word.")

        else:

            prompt = f"""
Explain the word:

{word}

Give:
1. Simple meaning
2. Part of speech
3. Example sentence
4. Synonyms
5. Antonyms

Meaning language:
{meaning_language}

If English + Urdu is selected, also provide a simple Urdu meaning.
"""

            try:

                response = client.responses.create(
                    model="gpt-5.6",
                    input=prompt
                )

                st.markdown(response.output_text)

            except Exception as e:
                st.error(f"Error: {e}")
