### Ordered

1. This repo is implemented based on the Browser-use open-source package.
2. After gitclone the code, please change the name of .env.example file to .env and fill in the API you will use and the key.
3. Install all the dependence in the requirements.txt and run
   ```
   pip install browser-use
   ```
4. Prepare a json file including all the basic infomations you would like the bot to know in advance (see `intro.json` as an example).
5. Run the main file using the command
   ```
   python main.py --info (your intro file) --url (your survey url)

   ```

