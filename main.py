import argparse
import asyncio
import json
import os

from dotenv import load_dotenv

from browser_use import Agent, Browser, ChatOpenAI, Tools
from browser_use.tools.views import UploadFileAction

load_dotenv()


async def finish_the_survey(info: dict, survey_url: str):
	llm = ChatOpenAI(model='o3')

	tools = Tools()

	browser = Browser(cross_origin_iframes=True)

	task = f"""
    - Your goal is to fill out and submit a survy form by pretending you are a human with the provided basic information.
    - Navigate to {survey_url}
    - Extract the information on the page to detect is there any question in this page and judge what type of answer is needed. 
	- Click "Next" at the first page of when you have answered the questions to access next page. 
	- Use this information and return a structured output that can be used to fill out the entire survey: {info}. Use the done action to finish the task. Fill out the survey with the following information.
        - Make sure that your answers are consistent.
    - Follow these instructions carefully:
        - if anything pops up that blocks the form, close it out and continue filling out the form.
        - Do not skip any fields, even if they are optional. If you do not have the information, make your best guess based on the information provided.
            1) use click action to for multi choice questions:
                
            2) use input_text action to fill out the type of questions requiring text typing:
                
            3) Move slider bar if there is a slider in the questions. It's not enough to set the value, but you need to make sure that the slider has been move to the value you set. The slider will become blue for a second if you make it successfully

            4) Do not answer to confirm that you are not human or you are an ai.
			5）Each time you make a selection, take it into the log file and remember the selection. Review it before you answer another question to avoid inconsistency.  
            6) CLICK THE NEXT BUTTON AND CHECK FOR A SUCCESS SCREEN. Once there is a success screen, complete your end task of writing final_result and outputting it.
			7) If you encounter the captcha robot detection, just pause any action until it is resolved.
    - Before you start, create a step-by-step plan to complete the entire task. Make sure to delegate a step for each field to be filled out.
    *** IMPORTANT ***: 
        - You are not done until you have filled out every field of the survey.
        
        - At the end of the task, structure your final_result as 1) a human-readable summary of all detections and actions performed on the page with 2) a list with all questions encountered in the page. Do not say "see above." Include a fully written out, human-readable summary at the very end.
    """

	agent = Agent(
		task=task,
		llm=llm,
		browser=browser,
		tools=tools,
	)

	history = await agent.run()


	return history.final_result()


async def main(test_data_path: str, survey_url: str):
	# Verify files exist
	if not os.path.exists(test_data_path):
		raise FileNotFoundError(f'Test data file not found at: {test_data_path}')

	with open(test_data_path) as f:  # noqa: ASYNC230
		mock_info = json.load(f)

	results = await finish_the_survey(mock_info,survey_url)
	print('Search Results:', results)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Apply to Rochester Regional Health job')
	parser.add_argument('--info', required=True, help='Path to test data JSON file')
	parser.add_argument("--url", required=True, help='URL to the survey')
	args = parser.parse_args()

	asyncio.run(main(args.info,args.url))