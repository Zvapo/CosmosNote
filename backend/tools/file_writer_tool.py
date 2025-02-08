from langchain_core.tools import tool

@tool
def file_writer_tool(file_name: str, content: str):
    """
    Write content to a file.
    """
    try:
        with open(f"../quartz/content/{file_name}.md", "w") as f:
            f.write(content)
        return f"File {file_name}.md written successfully."
    except Exception as e:
        return f"Error writing file {file_name}.md: {e}"
    

print(file_writer_tool.invoke({ "file_name": "test", "content": "Hello, world!" }))