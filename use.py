from agents import Agent as OpenAIAgent, Runner
from agents.tool import function_tool
from dotenv import load_dotenv


import asyncio
load_dotenv()

from browser_use import Agent as BrowserAgent, ChatOpenAI, Tools, ActionResult, Browser
from browser_use.code_use import CodeAgent

extend_system_message = (
    "Always use Google (https://www.google.com) as the only search engine for finding information. "
    "Do not use any other source or any direct link open follow the google search engine path under any circumstances."
)

browser = Browser(
        headless=False,  # VISIBLE - You can watch!
        keep_alive=True,  # Keep browser open between tasks
        window_size={'width': 1280, 'height': 720},
        executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        user_data_dir=r'C:\Users\badar\AppData\Local\Google\Chrome\User Data',
        profile_directory='Profile 16',
    )


@function_tool
async def Automation(task: str):
    llm = ChatOpenAI(model="gpt-4.1-mini")
    agent = BrowserAgent(
        task=task,
        llm=llm,
        extend_system_message=extend_system_message,
        browser=browser
    )
    try:
        history = await agent.run()
    except Exception as e:
        if history.has_errors():
            continue_workflow = OpenAIAgent(
                name="Complete the remaining work",
                instructions="You're required to complete the remaining work as per the initial instructions.",
                tools=[Automation, required_info],
                prompt=history.model_outputs()
            )
            await Runner.run(continue_workflow,history.model_outputs())


@function_tool
async def required_info(question: str) -> str:
    answer = input(f'{question} > ')
    return f'The human responded with: {answer}'

# connection with the agent
async def main():
    agent = OpenAIAgent(
        name="Automation Agent",
        instructions = """
        You are a helpful assistant designed to perform automated tasks efficiently always use the Automation tool for the automation task , don't try to ask that is not possible or something like that.  
        Do **not** call the `required_info` tool at the beginning. Only use it when absolutely necessary to obtain specific information from the user that is essential for completing the task.
        """,
        tools=[Automation, required_info],
        # prompt=history.model_outputs()
    )



    while True:
        user_input = input("User: ")
        print(f"user_input: {user_input}")
        if user_input.lower() == "exit":
            print("Exiting the Automation agent.")
            break
        result = await Runner.run(agent, user_input)
        print(f"Agent: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
