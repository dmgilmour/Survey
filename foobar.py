def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/PittESC/messages",
        auth=("api", "b6183ad4-8af3555d"),
        data={"from": "Excited User <mailgun@PittESC>",
            "to": ["dmgilmour@pitt.edu"],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomness!"})

def main():
    print("ayyo")
    print(send_simple_message())
