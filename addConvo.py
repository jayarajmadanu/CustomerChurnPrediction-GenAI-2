from src.Customer import Customer

cu = Customer(1005)

text = '''
"Customer: Hi, I just wanted to express my gratitude for the exceptional service I received from your bank's online support team.
Representative: Thank you for your feedback, Customer! We're thrilled to hear about your positive experience. Can you tell me more about what happened?
Customer: I had some technical issues with my online banking account, and your support team assisted me promptly and effectively. They guided me through the troubleshooting process with patience and expertise.
Representative: That's wonderful to hear, Customer! Our online support team works hard to ensure our customers receive the assistance they need promptly and efficiently.
Customer: I'm genuinely impressed by the level of service I received. It's reassuring to know that I can rely on your bank's support whenever I encounter issues.
Representative: We're delighted to hear that, Customer! If you ever need assistance in the future or have any questions, please don't hesitate to reach out to us.
Customer: Will do. Thanks again for your outstanding support!
Representative: It's our pleasure, Customer. Have a fantastic day!
"
'''
text = text.replace('\n',' ')
cu.add_chat_convo(text)


text = '''
"Customer: Hi, I just wanted to send a quick note to express my appreciation for the excellent service I consistently receive from your bank.
Representative: Thank you for your kind words, Customer! We're delighted to hear about your positive experience. Is there anything specific you'd like to commend?
Customer: Your online banking platform is incredibly user-friendly and intuitive. It makes managing my finances a breeze, and I appreciate the convenience it offers.
Representative: That's fantastic to hear, Customer! We continuously strive to enhance our online banking experience for our customers, and it's rewarding to hear that you find it valuable.
Customer: Absolutely! Your bank's commitment to innovation and customer satisfaction sets you apart from the competition.
Representative: We're grateful for your loyalty, Customer. If you ever have suggestions for further improvements or encounter any issues, please feel free to share them with us.
Customer: Will do. Keep up the excellent work!
Representative: Thank you, Customer. We appreciate your feedback. Have a wonderful day!"
'''
text = text.replace('\n',' ')
cu.add_chat_convo(text)
text='''
"Customer: Hi, I just wanted to take a moment to thank your bank for the exceptional customer service I received yesterday.
Representative: Thank you for reaching out, Customer! We're thrilled to hear about your positive experience. Can you tell me more about what happened?
Customer: I had an issue with a transaction on my account, and your customer service team resolved it promptly and efficiently. They were courteous, knowledgeable, and went above and beyond to assist me.
Representative: That's fantastic to hear, Customer! Providing excellent service is our top priority, and I'm glad we could assist you effectively.
Customer: Absolutely! I've been a customer for several years now, and experiences like this reaffirm my decision to bank with you.
Representative: We're grateful for your loyalty, Customer. If you ever encounter any issues or have questions in the future, please feel free to reach out to us.
Customer: Will do. Keep up the great work!
Representative: Thank you, Customer. We appreciate your kind words. Have a wonderful day!"
'''
text = text.replace('\n',' ')
cu.add_email_convo(text)
text = '''
"Customer: Hi, I'm interested in applying for a credit card with your bank. Can you provide me with more information about your options?                 
Representative: Of course, Customer. I'd be happy to assist you with that. Our bank offers a range of credit cards with various benefits and rewards programs. Do you have any specific preferences or features you're looking for in a credit card?                 
Customer: I'm mainly interested in cashback rewards and a low annual fee.                 
Representative: In that case, I'd recommend our Cashback Rewards card. It offers competitive cashback rates on purchases and has a relatively low annual fee. Would you like me to walk you through the application process?                 
Customer: Yes, please.                 
Representative: Great. I'll need some personal and financial information from you to complete the application. Let's start with your full name and contact details.                 
Customer: Okay, my name is Customer, and my phone number is [Phone Number].                 
Representative: Thank you, Customer. I'll guide you through the rest of the application process step by step.                 
Customer: Sounds good. Thank you for your assistance.                 
Representative: You're welcome, Customer. If you have any questions or need further assistance, feel free to ask.                 
Customer: Will do. Thanks again for your help.                 
Representative: Have a great day!"
'''
text = text.replace('\n',' ')
cu.add_email_convo(text)
text = '''
"Customer: Hi, I'm trying to set up a recurring transfer between my accounts, but I'm having trouble figuring out how to do it online.                 
Representative: I'm here to help, Customer. Let's walk through the process together. Can you please log into your online banking account?                 
Customer: Sure, I'm logged in now.                 
Representative: Great. Let's navigate to the transfers section. Do you see the option to set up recurring transfers?                 
Customer: Yes, I found it.                 
Representative: Perfect. Now, let's input the necessary details for the transfer, including the amount, frequency, and accounts involved.                 
Customer: Okay, I've filled in the information.                 
Representative: Wonderful. Double-check the details, and if everything looks correct, you can confirm the setup.                 
Customer: Alright, I've confirmed it. Thank you for your guidance.                 
Representative: You're welcome, Customer. If you have any further questions or encounter any issues, don't hesitate to reach out.                 
Customer: I will. Thanks again for your help.                 
Representative: Have a great day!  "
'''
text = text.replace('\n',' ')
cu.add_chat_convo(text)
text='''
"Customer: I received a notification about an unauthorized transaction on my credit card, and I've been trying to reach your fraud department, but no one is responding.
Representative: I apologize for the delay, Customer. Let me escalate this issue to our fraud department immediately. Can you please provide me with your credit card number?
Customer: [Provides credit card number] This is unacceptable! Your bank's security measures are clearly inadequate.
Representative: I understand your concern, Customer. We take security very seriously, and I'll ensure this issue is addressed promptly by our fraud team"
'''
text = text.replace('\n',' ')
cu.add_chat_convo(text)