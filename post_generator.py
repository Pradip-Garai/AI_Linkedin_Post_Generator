from llm_helper import get_llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 7 lines"
    if length == "Medium":
        return "8 to 12 lines"
    if length == "Long":
        return "13 to 16 lines"

def generate_post(length,language,topic):
    length_str = get_length_str(length)
    PROMPT = f''' 
      Generate a LinkdIn Post using the below information. No Preamble.
      1) Topic: {topic} 
      2) Length: {length_str}
      3) Language: {language}
        If Language is Hinglish then it means it is a mix of Hindi and English, but text will be in english
        like example of hinglish : Hello Everyone, aap sab kya se ho ?? ( not full 50% hinglish and 50% english).
      4) At last of add some hastag(#) Writing related to topics 
         like for Job Search we can add at last this types : #JobSearchTips #CareerAdvice #ProductivityHacks"
         do not attach it with main writting , write in next line 
    '''

    examples = few_shot.get_filter_post(length,language,topic)
    
    if len(examples) > 0:
        PROMPT+="\n5) Use the writing style as per the following examples."
        for i,post in enumerate(examples):
            post_text = post['text']
            PROMPT+=f"\n\n Example{i} \n\n {post_text}"

            if i==1:
                break


    llm = get_llm()
    response = llm.invoke(PROMPT)
    return response.content