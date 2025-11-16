"""
🤖 OpenAI Agents SDK × Browser-Use Orchestrator
Following simplified architecture with error recovery
"""

import asyncio
import os
from typing import Optional
from dotenv import load_dotenv

# OpenAI Agents SDK imports
from agents import Agent as OpenAIAgent, Runner
from agents.tool import function_tool

# Browser-Use imports
from browser_use import Agent as BrowserAgent, Browser, ChatOpenAI
from browser_use.agent.views import AgentHistoryList

# Load environment variables
load_dotenv()

# Global browser instance
browser: Optional[Browser] = None
_last_history: Optional[AgentHistoryList] = None

# System message to enforce Google search
extend_system_message = (
    "Always use Google (https://www.google.com) as the only search engine for finding information. "
    "Do not use any other source or any direct link open follow the google search engine path under any circumstances."
)


async def get_or_start_browser():
    """Get existing browser or start new one with timeout handling"""
    global browser

    # If browser already exists, return it
    if browser:
        print("♻️  Reusing existing browser session")
        return browser

    # Create new browser instance with user's Chrome profile
    print("🚀 Starting new browser session...")
    browser = Browser(
        headless=False,  # VISIBLE - You can watch!
        keep_alive=True,  # Keep browser open between tasks
        window_size={'width': 1280, 'height': 720},
        executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        user_data_dir=r'C:\Users\badar\AppData\Local\Google\Chrome\User Data',
        profile_directory='Profile 16',
        extra_chromium_args=[
            '--disable-extensions',
            '--disable-dev-shm-usage',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-popup-blocking',
        ]
    )

    # Retry browser start with longer timeout
    max_start_attempts = 3
    for attempt in range(max_start_attempts):
        try:
            print(f"   Attempt {attempt + 1}/{max_start_attempts}...")
            await asyncio.wait_for(browser.start(), timeout=90.0)
            print("✅ Browser started successfully!\n")
            return browser

        except asyncio.TimeoutError:
            print(f"⚠️  Timeout on attempt {attempt + 1}")
            if attempt < max_start_attempts - 1:
                print("🔄 Retrying...\n")
                await asyncio.sleep(2)
                browser = Browser(
                    headless=False,
                    keep_alive=True,
                    window_size={'width': 1280, 'height': 720},
                    executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                    user_data_dir=r'C:\Users\badar\AppData\Local\Google\Chrome\User Data',
                    profile_directory='Profile 16',
                    extra_chromium_args=[
                        '--disable-extensions',
                        '--disable-dev-shm-usage',
                        '--no-first-run',
                        '--no-default-browser-check',
                        '--disable-popup-blocking',
                    ]
                )
            else:
                raise Exception("Browser failed to start after multiple attempts. Please close all Chrome windows and try again.")

    return browser


@function_tool
async def Automation(task: str) -> str:
    """
    Execute browser automation tasks using BrowserAgent.

    Args:
        task: Description of what to do (e.g., "open LinkedIn and like my 2 feed posts")

    Returns:
        str: Result of the automation or error message
    """
    global _last_history

    print("\n" + "="*70)
    print("🌐 EXECUTING BROWSER AUTOMATION")
    print("="*70)
    print(f"📋 Task: {task}")
    print("="*70 + "\n")

    try:
        # Get or start browser (reuses existing browser)
        browser_instance = await get_or_start_browser()

        # Create LLM
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.0
        )

        # Create browser agent with extended system message
        agent = BrowserAgent(
            task=task,
            llm=llm,
            extend_system_message=extend_system_message,
            browser=browser_instance,
            use_vision=True,
        )

        print("⏳ Executing automation...\n")

        # Execute
        history = await agent.run(max_steps=50)
        _last_history = history

        # Check for errors
        if history.has_errors():
            print("\n⚠️  Task completed with errors")
            print("="*70)

            # Return error info for continue_workflow to handle
            error_details = []
            for step in history.history:
                if hasattr(step, 'error') and step.error:
                    error_details.append(str(step.error))

            return f"Task encountered errors: {'; '.join(error_details) if error_details else 'Check history for details'}"

        # Success
        print("\n" + "="*70)
        print("✅ AUTOMATION COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"📊 Steps: {history.number_of_steps()}")
        print(f"⏱️  Duration: {history.total_duration_seconds():.2f}s")
        print("="*70)
        print("🌐 Browser stays open - ready for next task!\n")

        result = str(history.final_result()) if history.final_result() else "Task completed successfully"
        return result

    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error: {error_msg}\n")
        print("🌐 Browser stays open - you can try again!\n")

        # Return error for potential retry
        return f"Error during automation: {error_msg}"


@function_tool
async def required_info(question: str) -> str:
    """
    Ask the user for required information.
    Only use when absolutely necessary.

    Args:
        question: The question to ask the user

    Returns:
        str: The user's response
    """
    answer = input(f'{question} > ')
    return f'The human responded with: {answer}'


# Continue workflow agent for error recovery
continue_workflow = OpenAIAgent(
    name="Complete the remaining work",
    instructions="""You're required to complete the remaining work as per the initial instructions.

    If the previous automation encountered errors:
    1. Analyze what went wrong
    2. Use required_info if you need additional information from the user
    3. Try Automation again with adjusted approach
    4. Don't give up - keep trying alternative approaches
    """,
    tools=[Automation, required_info],
)


async def main():
    """Entry point"""

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n" + "="*70)
        print("❌ ERROR: OPENAI_API_KEY not found!")
        print("="*70)
        print("\nPlease create a .env file with:")
        print("OPENAI_API_KEY=sk-proj-your_actual_key_here")
        print("="*70 + "\n")
        return

    # Create main agent
    agent = OpenAIAgent(
        name="Automation Agent",
        instructions="""
        You are a helpful assistant designed to perform automated tasks efficiently.

        **Core Principles:**
        1. Always use the Automation tool for browser automation tasks
        2. Execute tasks immediately - don't say "not possible" without trying first
        3. Only use required_info when absolutely necessary to obtain specific information
        4. Do NOT call required_info at the beginning - only when you actually need user input
        5. If automation returns errors, analyze and retry with adjustments
        6. Be persistent but smart about retries

        **Workflow:**
        - User gives task → Call Automation immediately
        - If Automation succeeds → Report success
        - If Automation has errors → Analyze, ask for info if needed, retry
        - Only use required_info when you truly need additional context from the user
        """,
        tools=[Automation, required_info],
        handoffs=[continue_workflow],
    )

    # Print welcome banner
    print("\n" + "="*70)
    print("🤖 BROWSER AUTOMATION AGENT")
    print("="*70)
    print("Powered by: OpenAI Agents SDK + Browser-Use")
    print("\n💡 Tell me any browser task - I'll execute it immediately!")
    print("   Browser window will be VISIBLE - watch it work!")
    print("   Browser STAYS OPEN between tasks")
    print("   Type 'exit' to quit\n")

    # Main interaction loop
    while True:
        user_input = input("User: ")

        if user_input.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Exiting the Automation agent.")
            print("🌐 Browser will remain open. Close it manually when done.\n")
            break

        if not user_input.strip():
            continue

        # Run the agent
        result = await Runner.run(agent, user_input)
        print(f"\nAgent: {result.final_output}\n")


if __name__ == "__main__":
    asyncio.run(main())
