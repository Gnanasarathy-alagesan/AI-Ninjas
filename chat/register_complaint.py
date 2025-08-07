# def chat(user_input, chat_history):
#     conversation_history.append({"role": "user", "content": user_input})

#     prompt = build_prompt(conversation_history)

#     response = model.generate_text(
#         prompt=prompt,
#         params={"decoding_method": "greedy", "max_new_tokens": 500},
#         raw_response=False,
#     )

#     conversation_history.append({"role": "assistant", "content": response})

#     # Check if the AI produced final JSON
#     try:
#         data = json.loads(response)
#         # Save to file
#         complaint_record = {"timestamp": datetime.now().isoformat(), **data}
#         with open("complaints.json", "a") as f:
#             f.write(json.dumps(complaint_record) + "\n")

#         # Reset conversation for next person
#         conversation_history.clear()

#         return chat_history + [(user_input, response)], gr.update(interactive=False)

#     except json.JSONDecodeError:
#         return chat_history + [(user_input, response)], gr.update()
