"""
🤖 OpenAI Agents SDK × Browser-Use Orchestrator
Immediate execution with proper browser initialization
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


async def restart_browser():
    """Restart browser from scratch"""
    global browser

    # Close existing browser
    if browser:
        try:
            await browser.stop()
        except:
            pass
        browser = None

    # Wait a moment for cleanup
    await asyncio.sleep(1)

    # Create and start fresh browser with user's Chrome profile
    # Using 'Profile 16' - your specific Chrome profile
    browser = Browser(
        headless=False,
        keep_alive=True,
        window_size={'width': 1280, 'height': 720},
        executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        user_data_dir=r'C:\Users\badar\AppData\Local\Google\Chrome\User Data',
        profile_directory='Profile 16'
    )

    await browser.start()
    print("🌐 Browser restarted!\n")

    return browser


async def get_or_start_browser():
    """Get existing browser or start new one"""
    global browser

    # If browser already exists, return it
    if browser:
        return browser

    # Create new browser instance with user's Chrome profile
    # Using 'Profile 16' - your specific Chrome profile
    browser = Browser(
        headless=False,  # VISIBLE - You can watch!
        keep_alive=True,  # Keep browser open between tasks
        window_size={'width': 1280, 'height': 720},
        executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        user_data_dir=r'C:\Users\badar\AppData\Local\Google\Chrome\User Data',
        profile_directory='Profile 16'
    )

    # Start the browser
    await browser.start()

    print("🌐 Browser started! It will stay open for all tasks.\n")

    return browser


@function_tool
async def browser_automation(task: str, url: str = "") -> dict:
    """
    Execute browser automation immediately. Just describe what you want to do.

    Args:
        task: What to do (e.g., "Open YouTube and search for Honey Singh songs")
        url: Starting URL if known (optional)
    """
    global _last_history

    print("\n" + "="*70)
    print("🌐 EXECUTING BROWSER AUTOMATION")
    print("="*70)
    print(f"📋 Task: {task}")
    if url:
        print(f"🌐 URL: {url}")
    print(f"👁️  Browser: VISIBLE ✓")
    print("="*70 + "\n")

    # Retry logic for connection errors
    max_retries = 2
    for attempt in range(max_retries):
        try:
            # Build task
            full_task = task
            if url:
                full_task = f"Navigate to {url}\n{task}"

            # Get or start browser (reuses existing browser)
            if attempt == 0:
                browser_instance = await get_or_start_browser()
            else:
                # On retry, restart browser
                print(f"🔄 Retry {attempt}/{max_retries-1} - Restarting browser...\n")
                browser_instance = await restart_browser()

            # Create browser agent
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.0
            )

            print("⏳ Executing automation...\n")

            agent = BrowserAgent(
                task=full_task,
                llm=llm,
                browser=browser_instance,
                use_vision=True,
            )

            # Execute
            history = await agent.run(max_steps=50)
            _last_history = history

            print("\n" + "="*70)
            print("✅ AUTOMATION COMPLETED")
            print("="*70)
            print(f"📊 Steps: {history.number_of_steps()}")
            print(f"⏱️  Duration: {history.total_duration_seconds():.2f}s")
            print(f"✓ Success: {history.is_successful()}")
            print("="*70)
            print("🌐 Browser stays open - ready for next task!\n")

            # DON'T close browser - keep it open for next task

            return {
                "status": "success",
                "result": str(history.final_result()) if history.final_result() else "Task completed",
                "steps": history.number_of_steps(),
                "success": history.is_successful()
            }

        except Exception as e:
            error_msg = str(e)

            # Check if it's a connection error
            if "ConnectionClosedError" in error_msg or "no close frame" in error_msg:
                if attempt < max_retries - 1:
                    print(f"\n⚠️  Connection error detected. Retrying with fresh browser...\n")
                    continue  # Retry with fresh browser
                else:
                    print(f"\n❌ Connection error persists after {max_retries} attempts.")
                    print("💡 Try: Close ALL Chrome windows and run the script again.\n")
            else:
                # Non-connection error, don't retry
                print(f"\n❌ Error: {error_msg}\n")

            print("🌐 Browser stays open - you can try again or give a new task!\n")

            return {
                "status": "error",
                "error": error_msg
            }

    # Should not reach here, but just in case
    return {
        "status": "error",
        "error": "Max retries exceeded"
    }


@function_tool
async def ask_user(question: str) -> str:
    """
    Ask the user a question when you need specific information.
    Only use this when absolutely necessary (e.g., login credentials, specific preferences).

    Args:
        question: The question to ask the user
    """
    print(f"\n❓ {question}")
    answer = input("👤 Your answer: ").strip()
    return answer


class BrowserOrchestrator:
    """Main orchestrator"""

    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")

        # Create main agent
        self.agent = OpenAIAgent(
            name="Browser Automation Agent",
            model="gpt-4o",
            instructions="""You are a Browser Automation Agent that executes tasks immediately.

**Core Principles:**

1. **Try first, ask later** - Always attempt the task first. The browser might already be logged in or have the needed access.
2. **Execute immediately** - Call browser_automation tool right away without asking for permission
3. **Assume browser state exists** - User might already be logged in to sites, tabs might already be open, etc.
4. **Only ask when browser agent fails** - If automation fails due to missing login, THEN ask for credentials

**How to handle requests:**

- Call browser_automation immediately with the task
- Let the browser agent try the task first
- The browser agent will handle navigation, detect login requirements, etc.
- If automation returns an error about needing login or missing info, THEN use ask_user
- After automation completes, briefly confirm what was done

**When to use ask_user:**
- ONLY AFTER browser_automation fails and reports it needs credentials/info
- ONLY when browser agent explicitly says it encountered a login page
- NOT before trying the automation
- NOT for confirmations or permissions
- NOT preemptively "just in case"

**Examples:**

User: "go to linkedin and like my post"
You: *immediately call browser_automation* (don't ask for password first!)
→ If browser agent returns "login required", THEN ask for credentials
→ If browser agent succeeds (already logged in), done!

User: "check my gmail"
You: *immediately call browser_automation* (don't ask which email!)
→ If browser agent is already on Gmail, it uses that
→ If browser agent needs login, THEN ask

**What NOT to do:**
- Don't ask "Do you need to login?" - Just try!
- Don't ask for credentials upfront - Try first!
- Don't ask "Should I proceed?" - Just proceed!
- Don't over-explain - Execute first, summarize after

Your job is to TRY the automation immediately, and only ask questions if the browser agent actually needs something.""",
            tools=[browser_automation, ask_user],
        )

        print("✅ OpenAI Agent initialized")

    def print_banner(self):
        """Print welcome banner"""
        print("\n" + "="*70)
        print("🤖 BROWSER AUTOMATION AGENT")
        print("="*70)
        print("Powered by: OpenAI Agents SDK + Browser-Use")
        print("\n💡 Tell me any browser task - I'll execute it immediately!")
        print("   Browser window will be VISIBLE - watch it work!")
        print("   Browser STAYS OPEN between tasks (new tabs for each task)")
        print("   Type 'exit' to quit and close the browser\n")

    async def chat(self, user_message: str):
        """Process user message"""

        # Run the agent
        result = await Runner.run(self.agent, input=user_message)

        # Display response
        print(f"\n🤖 Agent: {result.final_output}\n")

        return result.final_output

    async def interactive_mode(self):
        """Run interactive chat"""

        self.print_banner()

        while True:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!\n")
                    break

                # Process
                await self.chat(user_input)

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")

    async def run_single_task(self, task: str):
        """Run single task"""

        print("\n" + "="*70)
        print("🤖 BROWSER AUTOMATION AGENT")
        print("="*70)
        print(f"📋 Task: {task}\n")

        await self.chat(task)


async def main():
    """Entry point"""

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n" + "="*70)
        print("❌ ERROR: OPENAI_API_KEY not found!")
        print("="*70)
        print("\nPlease create a .env file with:")
        print("OPENAI_API_KEY=sk-proj-your_actual_key_here")
        print("\nGet your key at: https://platform.openai.com/api-keys")
        print("="*70 + "\n")
        return

    try:
        # Create orchestrator
        orchestrator = BrowserOrchestrator()

        # Check if running in interactive or single task mode
        import sys
        if len(sys.argv) > 1:
            # Single task mode
            task = " ".join(sys.argv[1:])
            await orchestrator.run_single_task(task)
        else:
            # Interactive mode
            await orchestrator.interactive_mode()

    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Keep browser open - don't close it when script exits
        print("\n🌐 Browser will remain open. Close it manually when you're done.\n")
        pass


if __name__ == "__main__":
    asyncio.run(main())
