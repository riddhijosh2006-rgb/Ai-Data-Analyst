# AI Data Analyst (Gemini)

1. Create an environment: `python -m venv venv`
2. Activate it: Windows `venv\Scripts\activate` | macOS/Linux `source venv/bin/activate`
3. Install packages: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your Gemini API key.
5. Start the app: `streamlit run app.py`

The app is a general conversational chatbot as well as a data analyst. It can
answer greetings, jokes, general questions, and follow-up conversation; it only
starts data analysis when you ask about the loaded file/database or request a
chart/dashboard. For data questions, it generates read-only SQL against loaded
tables, executes it, and shows the exact results and SQL for inspection.
Follow-up questions include the exact results of earlier queries as context.
