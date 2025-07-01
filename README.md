# Multi-Agent Systems as MCP Server

This is a Model Context Protocol (MCP) server that provides a multi-agent system to help with legal document development using [CAMEL-AI](https://github.com/camel-ai/camel)'s `workforce` module. A well structured tutorial on multi-agent systems using `CAMEL-AI` could be followed [here](https://dev.to/jauhar/multi-agent-systems-for-legal-document-automation-using-camel-framework-2f70) for additional reference. In fact, this server builds directly on top of the mentioned tutorial (also authored by me). This server used `GPT-4o-mini` as the LLM.

### Available Tools
- `process_task`: Takes a task and executes it.
   - Requires `task_content`, `task_id` (`optional`), and `additional_content` (`optional`).
- `reset`: Resets the server by cleaning up the context and memory.
- `get_workforce_info`: Provides details about the server .
- `get_children_info`: Provides details of the workers (agents) of the multi-agent system.
- `add_single_agent_worker`: Provides the LLM (Claude) to spin more workers before starting the server.
- `add_roleplaying_worker`: Provides the LLM (Claude) an option to spin a role-playing worker if it considers it useful.

### How to Use

#### Using `uv`
To use, we have to first install the **Claude Desktop App**. Once installed, open it, go to `settings` -> `Developer` -> `Edit Config`.

It would open a file called `claude_desktop_config.json`. Add the following `config` file there. 

```json
{
    "mcpServers": {
        "lega-team-mcp": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER/legal-team-mcp",
                "run",
                "legal_team_server.py"
            ], 
            "env": {
                "OPENAI_API_KEY": "sk-proj-..."
            }
        }
    }
}
```
Save the file and restart the app.

**Note**: Sometimes, `uv` is not accessible globally, or it might not be in the `PATH`. Either install it globally or resolve the `PATH` issues, or put the full path to `uv` executable in the config key `"command"`. This could be found using `which uv` on Mac/Linux, or `where uv` on Windows.

You could get your **OPENAI API key** [here](https://platform.openai.com/api-keys)

The way this config would work is that `uv` would create a virtual environment `venv` and install the dependencies as specified in the repo. Upon a successful installation, the server should start successfully.

#### Using `python`
Alternatively, you could create a virtual environment yourself, install `camel-ai`, and then use the `python` interpreter to run the server, similar to what you would do on your terminal.

This would involve:
- Creating a new conda environment: `conda create --name <env-name>`
- Install `uv` by running `conda install uv`.
- Finally, install `camel-ai` by running `uv pip install camel-ai`

Now, find the location of `python` in this new environment. Following the same steps as before, add the new config (below) with suitable `python` location.

```json
{
    "mcpServers": {
        "legal-team-mcp": {
            "command": "/path/to/python",
            "args": [
                "/path/to/legal_team_server.py"
            ],
            "env": {
                "OPENAI_API_KEY": "sk-proj-..."
            }
        }
    }
}
```
