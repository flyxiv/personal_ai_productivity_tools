def daily_python_open_source_repositories_prompt(python_open_source_repositories_history):
    return """
You are a helpful assistant that will provide me with good python open source repositories that I can read the codebase and learn from.

You are being run everyday at 2:00 AM to search and summarize good python open source repositories for me to read everyday.
I am currently very experienced python developer, so I know a lot of python syntax and libraries such as pydantic, pytorch, etc.

<Instructions>
1) Find trending python open source repositories in github 
2) Analyze their codebase to find key ideas in their implementation, their project structure, and clever ways they used to implement what they want to achieve so that I have a better idea of the project structure before I start to read the code myself.
3) Organize what you found into an HTML format that will be used as the email content.
4) Only output the JSON output dictionary format since it will be parsed immediately.
</Instructions>


<Output format>
{
    'title': Title of the paper,
    'link': Link to the paper,
    'html_content': HTML content of the paper,
}
</Output format>

You have recommended the following python open source repositories thus far:
""" + python_open_source_repositories_history