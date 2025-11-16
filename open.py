from browser_use import Agent, ChatOpenAI, Browser
from dotenv import load_dotenv
import asyncio

load_dotenv()


extend_system_message = (
    "Always use Google (https://www.google.com) as the only search engine for finding information. "
    "Do not use any other source or any direct link open follow the google search engine path under any circumstances."
)


browser = Browser(
        keep_alive=True,
        executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        user_data_dir=r'C:\Users\badar\AppData\Local\Google\Chrome\User Data',
        profile_directory='Profile 16',
    )


async def main():
    llm = ChatOpenAI(model="gpt-4.1-mini")
    task = "Open youtube and play a song named 'Shape of you'"
    agent = Agent(task=task, llm=llm,
                          extend_system_message=extend_system_message,
                          browser=browser)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())