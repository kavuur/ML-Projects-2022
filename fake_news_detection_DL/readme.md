```python
Done by Tanaka Nick Dhliwayo
```
required python packages for *veriNews* - fake news classifier application.

*using PyCharm may be easier*
```python
flask
googletrans
tensorflow
keras
nltk
textblob
numpy
```
1. Check if you have ```virtualenv``` using command: ```which virtualenv```
2. If no, enter the following in your terminal to install it.
```pip install virtualenv```
   
3. Create a virtual environment in current directory: ```virtualenv <my_env_name>```
4. ```source <my_env_name>/bin/activate``` to activate the new environment.
5. ```pip install -r requirements.txt``` to install the requirements in current environment.

6. Start Flask server and access application on *http://127.0.0.1:5000/* in your browser.
Be sure to be connected to the internet for the Translation API to work.

7. Find news in any language you want to verify copy text and paste on application and enjoy!