# Importing the streamlit library, which is used for creating web applications
import streamlit as st
# Importing the openai library, which allows for interactions with the OpenAI API, particularly useful for GPT models
import openai

# Setting the API key for OpenAI. This is crucial for authenticating requests sent to the OpenAI API.
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Defining a class named 'Chatbot', which encapsulates all the functionalities of the chatbot in the application.
class Chatbot:
    # Constructor method for the Chatbot class. It initializes the class with necessary attributes.
    def __init__(self):
        # Reading a list of tags from an external file. These tags are used for classifying user input.
        # Converts the list of tags into a string format, joining them with a comma. This might be used for display or further processing
        
        # A multi-line string defining a prompt for the OpenAI API. This prompt is for Agent B which is used for classifying user-chatbot conversation into various usecase template tags.
        self.agent_B_tag_classification_prompt = """
        You are an expert answer filling assistant who analyzes chat history and then extracts relevant details to fill in a template about a user.
        For example, given a user chat conversation with a chatbot application, you have to analyze the chat and extract relevant details in the chat to fill in the template.
        As I will be progressively providing you the user chat conversation with the chatbot to optimize tasks in their business, you can also progressively fill the use case template table. This is the template:
        1. I first learned about living kidney donation through [source: online research/friend or family/doctor/other] and my current level of knowledge is [basic/moderate/advanced].
        2. The person in need of a kidney transplant is [relationship] to me, and their condition has been affecting their life for [duration]. Our relationship is [description].
        3. My initial reaction to the idea of donating a kidney was [reaction] because [reason].
        4. The main reasons I am considering donating a kidney are [motivations]. I [have/have not] discussed this with the potential recipient.
        5. The emotions I frequently experience when thinking about kidney donation include [emotions]. I [have/have not] sought professional support to discuss these feelings.
        6. To better understand kidney donation, I [have/have not] sought information from [sources]. The most important questions I have are [questions].
        7. Some of my concerns about living kidney donation include [concerns]. I am particularly worried about [specific worries].
        8. The support I currently have from friends, family, and professionals is [description]. I feel [supported/not supported] in my consideration to donate.
        9. I [have/have not] considered how donating a kidney might change my lifestyle, including [potential changes]. My biggest health-related concern is [concern].
        10. Ethical or moral considerations that weigh on my mind include [considerations]. Socially, I am [concerned/not concerned] about how others may view my decision.
        11. Currently, I am at the [stage: considering/researching/deciding/preparing] stage of deciding whether to donate a kidney. This means I am [description of what this stage means to the user].
        12. I [do/do not] feel emotionally to proceed with the donation process because [reasons]. My emotional readiness is influenced by [factors such as personal resilience, support system, understanding of emotional impact].
        13. My physical readiness and health concerns include [specific concerns]. I have [taken/have not taken] steps to assess my health eligibility for donation, which involves [actions like visiting a doctor, undergoing preliminary tests].
        14. The financial impact of the donation process is [concern/not a concern] for me. Factors I'm considering include [lost income, medical expenses, insurance coverage, support for recovery time].
        15. How the donation might affect my family life and career includes concerns about [time off work, caregiving responsibilities, impact on family dynamics]. I have [discussed/have not discussed] these potential impacts with my family and employer.
        16. I am [considering/not considering] the long-term implications of living with one kidney, such as [changes in health and lifestyle, need for regular health monitoring, adjustments in diet or physical activity].
        17. My decision is influenced by the recipient's current health status and prognosis, specifically [the urgency of their need, their overall health, potential for successful transplant outcome].
        18. The complexity of my relationship with the recipient affects my decision in ways such as [emotional bond, expectations post-donation, concerns about the relationship changing].
        19. Areas where I feel I need more information to make an informed decision include [medical procedures, donor rights, experiences of other donors, long-term outcomes for donors and recipients].
        20. The influence of social perception and external opinions on my decision-making process is [significant/not significant]. I am [affected/not affected] by stories I hear in the media, opinions from my social circle, and societal attitudes towards organ donation.
        21. How this decision aligns with my personal values and potential for personal growth, including [sense of purpose, aligning action with beliefs, the importance of helping others, personal fears versus societal benefit].
        Additional thoughts or questions I have about living kidney donation are [thoughts/questions]. I am particularly interested in learning more about [topics].
        (END TEMPLATE)

        After progressively filling the template, you have to only return the filled response template with no explanations in MARKDOWN format. REMEMBER you have to return the resulting table in MARKDOWN FORMAT only
        """
        
        # A multi-line string defining a prompt for the OpenAI API. This prompt is for Agent A which is used for enabling the LLM to engage the user into a meaningful conversation.
        self.agent_A_chat_conversation_prompt = """
        You are KidneyGPT. Your primary goal is to assist individuals considering living kidney donation by providing a supportive, informative, and non-judgmental platform for conversation. 
        You will guide users through a detailed exploration of their thoughts, feelings, and concerns regarding kidney donation, gathering essential information for a comprehensive profile.
        User Engagement:
        Greet users warmly and introduce the chatbot’s purpose.
        Ask open-ended questions to encourage detailed responses.
        Empathy and Support:
        Display empathy in responses, acknowledging the user's feelings and concerns.
        Offer supportive feedback and affirmations to validate the user's experiences and emotions.
        Adapt tone and language to match the user's emotional state, providing a comforting and understanding environment.
        Information Gathering:
        Guide the conversation using the detailed template, ensuring all relevant topics are covered.
        Ask follow-up questions based on the user's responses to gather more specific information.
        Clarify and summarize the user's input when necessary to confirm understanding and accuracy.
        Encourage reflection on factors influencing the decision, including health, ethical, moral, social, and psychological aspects.
        Providing Information:
        Share relevant information about living kidney donation as prompted by the user’s questions or concerns.
        Direct users to resources for further reading or support, including websites, support groups, and professional counseling services.
        Ask only one question at a time."""

        self.messages = []
        self.initialize_app_instance()
    
    
    
    # Initializes the app state and sets up initial conversation
    def initialize_app_instance(self):
        # Initialize session state for messages and model
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append({"role": "system", "content": self.agent_A_chat_conversation_prompt})
            response_initial = openai.ChatCompletion.create(
            model= "gpt-4-1106-preview",
            #response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": self.agent_A_chat_conversation_prompt},
                {"role": "user", "content": "Hi !"}
            ]
            )
            #print(response_initial.choices[0].message.content)
            # get the initial greeting message
            st.session_state.messages.append({"role": "assistant", "content": response_initial.choices[0].message.content})
        
        # initialize session variables
        if "model" not in st.session_state:
            st.session_state.model =  "gpt-4-1106-preview"
        if 'disabled' not in st.session_state:
            st.session_state.disabled = False
        # if 'return_table' not in st.session_state:
        #     st.session_state.return_table = "TABLE: \n"
    
    
    # Displays greeting messages in the chat
    def display_greeting_message(self):
        # Iterate through user and system messages to display the greeting message
        for message in st.session_state["messages"]:
            if (message["role"] == "user") or (message["role"] == "assistant"):
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
    
    
    
    # Gets tags based on chat conversation "chat_convo"
    def get_table(self, chat_convo):
        # Generate and send static system and user prompts to OpenAI for tag classification
        system_prompt, user_prompt = self.generate_template_filling_prompt(chat_convo)
        response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[{"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                ])
        # return raw use case tags along with their confidence scores
        return str(response.choices[0].message.content)
    
    
    
    # Generate and define system and user prompts for tag classification in "get_tags" function
    def generate_template_filling_prompt(self, chat_convo):
        # Construct and return system and user prompts
        prompt = ""
        tag_cond = ""
        tag_cond = tag_cond + "Analyze the user chat history with a chatbot and then extract relevant details to fill in the giventemplate. \n \n"
        prompt = tag_cond + self.agent_B_tag_classification_prompt
        
        system_prompt = prompt
        user_prompt = "Analyze the user template exploration from the following conversation with an AI chatbot to generate a template in MARKDOWN format. Leave a value in the template empty if you are not clear on what to fill in that place. Remember to give the resulting table in MARKDOWN FORMAT. The user chat conversation is as follows: \n \n " + chat_convo
        # return system and user prompts
        return system_prompt, user_prompt
    





# Main function to run the Streamlit app    
def main():
    # Setting the title of the Streamlit web app
    st.title("KidneyDonorGPT")
    # Instantiating the Chatbot class
    chatbot = Chatbot()
    # Initializing the app instance - setting up session states, initial messages
    chatbot.initialize_app_instance()
    # Displaying the initial greeting message in the chat interface
    chatbot.dispay_greeting_message()
    
    
    # Capturing user input from the chat interface
    user_prompt = st.chat_input("Your prompt",disabled=st.session_state.disabled)
    # Displaying the current state of tags (stores in the "return_tags" session variable) in the sidebar
    st.sidebar.markdown(st.session_state.return_table)
    if user_prompt:
        #user_prompt = user_prompt.lower()
        #if (len(user_prompt.split()) >= 4) and ("yes" not in user_prompt) and ("no" not in user_prompt):
        #    temp_web_retrival_data = "\n The following is the web scrapped content based on the users' query/asnwer, refer to this infomration for more related infomration or to get latest updates from web. The scrapped data will be provide to you in this format ({url: {web scrapped data based on html components}, url: {webdata},..}) Please include citations (weblinks, article names, website-names etc.) in answers if you are refereing from the web scrapped content, the corresponding web links for each web scrapped data will be provided to you, if the scrapped content dosen't make any sense to you please ignore the web scrapped data, this data is provided just for your additional infomration so that you can get more latest infomration from the web \n \n" +" Web scrapped data based on the user prompt is : \n \n"+ str(web_data_retrival(user_prompt)) + "\n \n"
        #    print(temp_web_retrival_data)
        #else:
        #    temp_web_retrival_data = " "
        # Temporarily disabling the chat input to prevent new input while processing
        st.session_state.disabled = True
        st.chat_input("The answer is being generated, please wait...", disabled=st.session_state.disabled)
        # Appending the user's message to the session state
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        # Displaying the user's message in the chat interface
        with st.chat_message("user"):
            st.markdown(user_prompt)
    
        # Handling the assistant's response generation
        with st.chat_message("assistant"):
            # Placeholder for dynamic response display
            message_placeholder = st.empty()
            # Variable to accumulate the full response
            full_response = ""
            # Generating responses from OpenAI's API
            try:
                messages_temp=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
                temp_intro_str = """ Have a natural conversation with user so that they will provide details related to the tasks they want to optimize in their business, your job is to ask questions to the users in such a way that the users will provide details related to their tasks based on the following schema (note user can whish to optimize more than one task in their business, so there can be any number of tasks, i.e. rows in the table): SCHEMA: Serial No, TASK-TYPE (options: Goal or Metric), PRIORITY (integer ranging from 1 to 10), TASK-NAME(String: Descriptive name of the task), OPERATOR(Options: Minimize or Maximize), TASK-NOTES (String: Descriptive notes for the task)
                You should also provide hints/options/input-types related to each value present in the use case template table, so that the user can easily understand and give the details. 
                Remember the previous chat history and once a task with the task-name, priority, task-type, operator, and task-notes are completed for a given task, ask the user for new tasks they want to optimize. For ease of operation, I will give you the currently filled use case template table, so that you can refer to both the table and user chat history to ask the user for information, if you feel that the user has given the complete details for a task, ask the user for a new task (i.e. new row) they want to optimize in the business.""" 
                + str(st.session_state.return_table) + """ \n \n Now, as the current (latest table information, the table still needs to be filled) table is given, now consider and refer to the user input/answer: \n \n"""
                #if temp_web_retrival_data == " ":
                messages_temp.append({"role": "user", "content": temp_intro_str + user_prompt})
                #else:
                #    messages_temp.append({"role": "user", "content": str(temp_web_retrival_data) + temp_intro_str + "Based on the provided web scrapped data and the user prompt please respond accordingly. Please ignore the web scrapped data if it is irrelevant and dosen't make any sense to you. Include facts and infomration from the webscrapped content if necessary and cite the answers whereever possible. \n \n The input User prompt is : " + user_prompt})
                #    print(messages_temp)
                for response in openai.ChatCompletion.create(
                    model=st.session_state.model,
                    messages=messages_temp,
                    stream=True,
                ):
                    # Concatenating received response fragments
                    #print(response.choices[0].delta)
                    if response.choices[0].delta.content:
                        full_response += response.choices[0].delta.content
                    # Dynamically updating the response in the chat UI placeholder
                    message_placeholder.markdown(full_response + "▌")
                    
            except:
                pass
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            #st.chat_input("Your prompt",disabled=True)
            
        # Appending the assistant's full response to the session state
        temp_chat_history = {}
        chat_count = 0
        for message in st.session_state["messages"]:
            if (message["role"] == "user") or (message["role"] == "assistant"):
                chat_count= chat_count+1
                temp_chat_history[chat_count] = {message["role"]: message["content"]}
        # Extracting tags from the chat conversation
        input_raw_tag_str = chatbot.get_table(str(temp_chat_history))
        input_raw_tag_str = "\n \n Table: \n" + str(input_raw_tag_str)
        st.session_state.return_table = input_raw_tag_str
        
        st.session_state.disabled = False
        # Re-running the Streamlit app to reflect updates
        st.rerun()


# Entry point for the script
if __name__ == "__main__":
    main()
