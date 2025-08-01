import anyio
import config
from agno.tools.mcp import MultiMCPTools
from agno.agent import Agent
from agno.models.google import Gemini

from mcp import StdioServerParameters
import asyncio
import datetime

async def run_agent(message: str) -> str:
    print(f"Starting run_agent with message: {message[:100]}...")
    try:
        mcp_tools_brevo = StdioServerParameters(
            command="node",
            args=["./youtube-video-summarizer-mcp/dist/index.js"],
        )
        
        async with MultiMCPTools(server_params_list=[mcp_tools_brevo], timeout_seconds=120.0) as mcp_tools_main:
            print("MCP Tools initialized successfully")
            agent = Agent(
                model=Gemini(api_key = config.get_api_key()),
                tools=[mcp_tools_main],
                markdown=True,
                show_tool_calls=True,
                retries=2,
            )
            
            print(f"Sending request to agent...")
            response = await agent.arun(message)
            response = response.content
            print(f"Agent response received: {response[:200]}..." if response else "No response from agent")
            
            if not response:
                raise ValueError("Empty response received from agent")
                
            return str(response)
            
    except anyio.ClosedResourceError as e:
        error_msg = f"MCP stream closed unexpectedly: {str(e)}"
        print(error_msg)
        raise RuntimeError(error_msg) from e
    except Exception as e:
        error_msg = f"Error in run_agent: {str(e)}"
        print(error_msg)
        print(f"Error details: {str(e)}")
        import traceback
        traceback.print_exc()
        raise RuntimeError(error_msg) from e
        
if __name__ == "__main__":
    video_link = input("Your youtube video link:")
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            run_agent(
                f"""{video_link}"""  )
        )
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            print("No problem: Event loop was already closed.")
        else:
            raise