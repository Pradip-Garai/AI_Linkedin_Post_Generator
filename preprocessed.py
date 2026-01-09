import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm


def process_posts(raw_file_path, processed_file_path="Data/preprocessed_post.json"):
    enriched_posts = []

    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)

        for post in posts:
            metadata = extract_metadata(post["text"])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        # ✅ FIX: safe mapping (no KeyError)
        post["tags"] = list({unified_tags.get(tag, tag) for tag in post["tags"]})

    with open(processed_file_path, mode="w", encoding="utf-8") as outfile:
        json.dump(enriched_posts, outfile, indent=4)


def get_unified_tags(posts):
    unique_tags = set()
    for post in posts:
        unique_tags.update(post["tags"])

    unique_tags_list = ", ".join(unique_tags)

    PROMPT = """
I will give you a list of tags. You need to unify tags with the following requirements:

1. Merge similar tags into one unified tag.
2. Use Title Case for all tags.
3. Output must be a valid JSON object. No preamble.
4. Output must map original tag to unified tag.

Example Output:
{{
  "Job Hunting": "Job Search",
  "Jobseeker": "Job Search",
  "Motivation": "Motivation"
}}

Here is the list of tags:
{tags}
"""

    pt = PromptTemplate.from_template(PROMPT)
    chain = pt | llm
    response = chain.invoke({"tags": unique_tags_list})

    try:
        parser = JsonOutputParser()
        return parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Failed to parse unified tags JSON")


def extract_metadata(post):
    PROMPT = """
You are given a LinkedIn post. Extract metadata using these rules:

1. Return ONLY valid JSON. No preamble.
2. JSON must have exactly three keys:
   - line_count (number)
   - language ("English" or "Hinglish")
   - tags (array, max 2 tags)

Here is the post:
{post}
"""

    pt = PromptTemplate.from_template(PROMPT)
    chain = pt | llm
    response = chain.invoke({"post": post})

    try:
        parser = JsonOutputParser()
        return parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Failed to parse metadata JSON")


if __name__ == "__main__":
    process_posts("Data/raw_post.json", "Data/preprocessed_post.json")
