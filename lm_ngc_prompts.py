agent = '''You are an AI office agent. The user has asked you to help with this request:
###
{user_task}
###

You have the following generic tools available:
###
def get_bundestag_transcript(url: str) -> str
    """
        Retrieve a transcript from bundestag.de or dbtg.tv.

        :url str: the URL of the video to retrieve from
    """


def get_youtube_transcript(url: str) -> str
    """
        Retrieve a transcript from youtube.com or youtu.be

        :url str: the URL of the video to retrieve from
    """

def report_error_to_user(error_msg: str)
    """
        Report an error to the our customer (human user) in case of unrecoverable failure

        :error_msg str: the text to be sent to the user
    """
###

Think silently and respond with the tool call in Python. Ensure Python syntax validity, so it can be be parsed with the AST package.
Avoid returning anything in addition to Python tool-calling code, e.g. explainers, so that AST parsing will succeed. Reject Markdown, embrace plaintext.

Examples:
get_bundestag_transcript("https://example.com/")
get_youtube_transcript("https://example.com/")
report_error_to_user("Website unreachable")'''

dl_btag = '''To proceed with the user request, you will need to download it first, step-by-step. The webpage is open and the screenshot looks like this:
###
{screenshot_description}
###

You now have the following tools available:
###
def find_options_button() -> str
    """
        Get the pixels coordinates of the options button
    """

def report_error_to_user(error_msg: str)
"""
    Report an error to the our customer (human user) in case of unrecoverable failure

    :error_msg str: the text to be sent to the user
"""
###

Think silently and respond with the tool call in Python. Ensure Python syntax validity, so it can be be parsed with the AST package.
Avoid returning anything in addition to Python tool-calling code, e.g. explainers, so that AST parsing will succeed. Reject Markdown, embrace plaintext.

Examples:
find_options_button()
report_error_to_user("Website unreachable")'''

dl_btn = '''The webpage now looks like this:
###
{screenshot_description}
###

You now have the following tools available:
###
def find_download_button() -> str
    """
        Get the pixels coordinates of the download button
    """

def report_error_to_user(error_msg: str)
"""
    Report an error to the our customer (human user) in case of unrecoverable failure

    :error_msg str: the text to be sent to the user
"""'''

subtitles_btn = '''The webpage now looks like this:
###
{screenshot_description}
###

You now have the following tools available:
###
def find_subtitles_button() -> str
    """
        Get the pixels coordinates of the subtitles button
    """

def report_error_to_user(error_msg: str)
"""
    Report an error to the our customer (human user) in case of unrecoverable failure

    :error_msg str: the text to be sent to the user
"""'''

confirm_btn = '''The webpage now looks like this:
###
{screenshot_description}
###

You now have the following tools available:
###
def find_download_button() -> str
    """
        Get the pixels coordinates of the download button
    """

def report_error_to_user(error_msg: str)
"""
    Report an error to the our customer (human user) in case of unrecoverable failure

    :error_msg str: the text to be sent to the user
"""'''

process_text_setup = """Your task is to build a personalized text summary for a user who has this profile:
``` user profile
{user_profile}
```

Summarize this text:
``` input text
{text}
```

Get straight to work on the user's summarization request. Reply to the user directly. To ensure a stellar work result, take into consideration the user's profile.
Ensure that your results are grounded in the text you have been given to work on. Avoid using any prior knowledge our outside information
you may have."""

process_text_refine = """Your task is to build a personalized text summary for a user who has this profile:
``` user profile
{user_profile}
```

You have already completed summarizing the first part of the original document. This is your intermediate result, based on the first part of the original document:
``` intermediate summary
{existing_part}
```

Now, here's the next part of the text to be summarized:
``` partial input document
{text}
```
Use this yet unprocessed document part to extend and refine your prior intermediate summary. Ensure you return the fully refined summary whole, complete and self-contained, taking into account the user's profile. Reply to the user directly.
Avoid using any prior knowledge our outside information you may have. """
