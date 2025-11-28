# import torch
# from transformers import pipeline
# import os
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, PageTemplate
# from reportlab.lib.pagesizes import letter
# import datetime as dt

# pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")
# def _create_pdf(title, text):    
#     file_name = dt.datetime.now(dt.timezone.utc).timestamp()

#     if not os.path.exists('assets/documents'):
#       os.makedirs('assets/documents')
#     # Create pdf doc  
#     pdf_path = f"assets/documents/{file_name}.pdf"

#     # Define margins
#     left_margin = 36
#     right_margin = 36
#     top_margin = 36
#     bottom_margin = 36

#     # Create a SimpleDocTemplate
#     pdf_doc = SimpleDocTemplate(pdf_path, pagesize=letter,
#                                 leftMargin=left_margin, rightMargin=right_margin,
#                                 topMargin=top_margin, bottomMargin=bottom_margin)

#     # Define a frame with adjusted margins
#     frame = Frame(left_margin, bottom_margin, letter[0] - left_margin - right_margin,
#                   letter[1] - top_margin - bottom_margin, showBoundary=False)

#     # Create a PageTemplate and add the frame to it
#     page_template = PageTemplate(id='main', frames=[frame])

#     # Add the PageTemplate to the SimpleDocTemplate
#     pdf_doc.addPageTemplates([page_template])

#     # Set font to Times New Roman
#     styles = getSampleStyleSheet()

#     # Title
#     title_paragraph = Paragraph(title, styles['Title'])
#     text_paragraphs = [Paragraph(line, styles['BodyText']) for line in text.split('\n')]

#     # Build a Story with paragraphs
#     story = [title_paragraph] + text_paragraphs
    
#     # Build the PDF document with the Story
#     pdf_doc.build(story)
#     # return f"assets/documents/{file_name}.pdf"
    
# topic="Hotel Automation Software"
# description="A hotel has a certain number of rooms. Each room can be either single bed or double bed type and may be AC or Non-AC type. The rooms have different rates depending on whether they are of single or double, AC or Non-AC types. Guests can reserve rooms in advance or can reserve rooms on the spot depending upon availability of rooms. The receptionist would enter data pertaining to guests such as their arrival time, advance paid, approximate duration of stay, and the type of the room required. Depending on this data and subject to the availability of a suitable room, the computer would allot a room number to the guest and assign a unique token number to each guest. If the guest cannot be accommodated, the computer generates an apology message. The hotel catering services manager would input the quantity and type of food items as and when consumed by the guest, the token number of the guest, and the corresponding date and time. When a customer prepares to check-out, the hotel automation software should generate the entire bill for the customer and also print the balance amount payable by him. During check-out, guests can opt to register themselves for a frequent guests program."

# messages = [
#     {
#         "role": "system",
#         "content": "You are a chatbot who can generate an SRS document!",
#     },
#     {"role": "user", "content": f"Generate an SRS document where the topic is {topic} and description is {description}"},
# ]
# prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
# outputs = pipe(prompt, max_new_tokens=102, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
# print(outputs[0]["generated_text"].split('<|assistant|>\n')[1])



# srs_output = outputs[0]["generated_text"].split('<|assistant|>\n')[1]
# _create_pdf("SRS Document", srs_output)
