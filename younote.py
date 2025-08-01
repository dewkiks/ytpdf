from typing import TypedDict
import os
import config

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import re
from datetime import datetime
import prompts
import pdf_converter
from yt_mcp import run_agent

class State(TypedDict):
    youtube_url: str
    content: str
    decision: int
    decision_text:str
    markdown_content:str
    pdf_bytes: bytes
    error: str 

async def analyze_video_content(state: State) -> State:
    try:
        youtube_url = state["youtube_url"]
        print(f"Analyzing video: {youtube_url}")
        
        prompt = prompts.get_video_analysis_prompt(youtube_url)
        print("Prompt generated successfully")
        print(f"Prompt: {prompt[:200]}...") 
        
        print("Calling run_agent...")
        response = await run_agent(prompt)
        print(f"Raw response from run_agent: {response[:500]}...")
        
        if not response or len(response.strip()) == 0:
            raise ValueError("Empty response received from agent")
            
        state["content"] = response
        return state
        
    except Exception as e:
        import traceback
        error_msg = f"Error in analyze_video_content: {str(e)}"
        print(error_msg)
        print("Detailed traceback:")
        traceback.print_exc()
        state["error"] = error_msg
        return state


async def display_content(state: State) -> State:
    if state.get("error"):
        print(f"Error: {state['error']}")
    else:
        print(state["content"])
    
    return state

def convert_markdown_format(state: State) -> State:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=config.get_api_key(),
        temperature=0
    )
    
    content = state["content"]
    decision = state["decision"]

    if decision == 1:
        state["decision_text"] = "short"
        prompt = prompts.get_short_convert_markdown_prompt(content)
    elif decision == 2:
        state["decision_text"] = "long"
        prompt = prompts.get_long_convert_markdown_prompt(content)

    response = llm.invoke(prompt)
    state["markdown_content"] = response.content if hasattr(response, 'content') else str(response)
    
    return state

def process_video_to_pdf(video_url, markdown_notes, note_type):
    """
    Complete workflow: video URL + generated notes -> PDF
    
    Args:
        video_url (str): YouTube URL
        markdown_notes (str): Generated markdown content from your prompts
        note_type (str): "short" or "long" for filename distinction
    """
    
    # Generate appropriate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_id = re.search(r'(?:v=|youtu\.be/)([^&\n?#]+)', video_url)
    video_id_str = video_id.group(1) if video_id else "unknown"
    
    output_filename = f"notes_{note_type}_{video_id_str}_{timestamp}.pdf"
    
    return pdf_converter.convert_notes_to_pdf(
        markdown_content=markdown_notes,
        output_filename=output_filename,
        video_title=f"Educational Notes ({note_type.title()})",
        video_url=video_url
    )

def markdown_pdf(state: State) -> State:
    """Generates a PDF from markdown and stores the bytes in the state."""
    try:
        pdf_data = pdf_converter.convert_notes_to_pdf(
            markdown_content=state["markdown_content"],
            video_title=f"YouTube Notes ({state['decision_text'].title()})",
            video_url=state["youtube_url"],
        )
        state["pdf_bytes"] = pdf_data
        print("✅ PDF generated in memory.")
    except Exception as e:
        error_msg = f"PDF conversion failed: {e}"
        print(f"❌ {error_msg}")
        state["error"] = error_msg
    return state

# Build workflow
workflow = StateGraph(State)

workflow.add_node("analyze_video", analyze_video_content)
workflow.add_node("display", display_content)
workflow.add_node("markdown",convert_markdown_format)
workflow.add_node("markdown_to_pdf",markdown_pdf)

workflow.set_entry_point("analyze_video")

workflow.add_edge("analyze_video","markdown")
workflow.add_edge("markdown","markdown_to_pdf")
workflow.add_edge("markdown_to_pdf", END)

app = workflow.compile()

async def extract_youtube_content(youtube_url: str, decision: int):
    """Invokes the workflow and returns the final state dictionary."""
    initial_state = State(
        youtube_url=youtube_url,
        content="",
        decision=decision,
        decision_text="",
        markdown_content="",
        pdf_bytes=None,
        error=None,
    )
    final_state = await app.ainvoke(initial_state)
    return final_state

async def main(yt,dec):
    # if api:
    #     os.environ["GEMINI_API_KEY"] = api
    # else:
    #     os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API")
    
    await extract_youtube_content(yt, dec)
     

# if __name__ == "__main__":
#     import asyncio
    
#     os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API")
#     url = input("Enter YouTube URL: ")
    
#     while True:
#         decision = input("Enter 1 for short note / 2 for long note: ")
#         try:
#             decision = int(decision)
#             if decision in [1, 2]:
#                 print(f"You opted for {'short' if decision == 1 else 'long'} notes, please wait...")
#                 break
#             else:
#                 print("Please enter 1 or 2")
#         except ValueError:
#             print("Please enter a valid number")

#     asyncio.run(extract_youtube_content(url, decision))