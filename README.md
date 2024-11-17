# AgentApp
This uses two AI Agents to compose a motivational email.


1. generate a daily motivational quote
2. compose an email around the input motivational quote
    - This is overkill, as one model could do both. However, it's a fun example of how to have two agents interact.   
   
Finally, the resulting email is sent to a mailing list based on an input list of emails. This is relatively trival, but you can substitute the functionality for the output API of your choice (twitter, facebook etc.)
### Setup:  
1. Sign up for the anthropic API and load your account with some $ (each email is <$0.01, so I only did the minimum of $5)
2. Get a gmail API key so that the script can automatically send the email from your address
>Enable 2-Step Verification in your Google Account  
Go to Google Account → Security → App passwords   
Generate an App password for this application

3. You will need to create a `.env` file to store your API keys, as I will not be sharing mine here.
```commandline
ANTHROPIC_API_KEY=your-api-key
SENDER_EMAIL=your-gmail@gmail.com
SENDER_APP_PASSWORD=your-gmail-app-password
```
4. Enter your mailing list as a string of emails
```Python
# Example mailing list
mailing_list = [
    "recipient1@example.com",
    "recipient2@example.com"
]
```


To Do:

- Read in the mailing list from a database (google sheets lol)
