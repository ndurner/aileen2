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
def find_confirm_button() -> str
    """
        Get the pixels coordinates of the confirmation button
    """

def report_error_to_user(error_msg: str)
"""
    Report an error to the our customer (human user) in case of unrecoverable failure

    :error_msg str: the text to be sent to the user
"""'''
