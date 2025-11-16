from browser_use import Agent, ChatOpenAI, Browser
from dotenv import load_dotenv
import asyncio
import subprocess
import time

load_dotenv()


extend_system_message = (
    "Always use Google (https://www.google.com) as the only search engine for finding information. "
    "Do not use any other source or any direct link open follow the google search engine path under any circumstances."
)


def close_chrome():
    """Close all Chrome instances before starting."""
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'],
                      capture_output=True,
                      timeout=10)
        print("Closed existing Chrome instances")
        time.sleep(2)  # Wait for processes to fully close
    except Exception as e:
        print(f"Note: {e}")


browser = Browser(
        keep_alive=True,
        executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        user_data_dir=r'C:\Users\badar\AppData\Local\Google\Chrome\User Data',
        profile_directory='Profile 16',
        headless=False,
        disable_security=True,
        args=[
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-background-networking',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-dev-shm-usage',
            '--disable-ipc-flooding-protection',
            '--disable-renderer-backgrounding',
            '--metrics-recording-only',
        ]
    )


async def main():
    # Close Chrome before starting
    close_chrome()

    llm = ChatOpenAI(model="gpt-4.1-mini")
    task = "Open youtube and play a song named 'Shape of you'"
    agent = Agent(task=task, llm=llm,
                          extend_system_message=extend_system_message,
                          browser=browser)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
