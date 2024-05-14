from fastapi import FastAPI
import uvicorn
from app.schemas import LLMInput
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="team-llmm")

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key='')


def create_app() -> FastAPI:
    _app = FastAPI(title="team-llmm")
    return _app


app = create_app()


@app.on_event("startup")
async def startup():
    print("app started")


@app.on_event("shutdown")
async def shutdown():
    print("SHUTDOWN")


@app.get("/")
async def hello():
    return "Hello team llmm"


def scraper():
    pass


def dynamic_chunking():
    return ""


def semantic_chunking():
    chunk = """In July, Alexander-Walker agreed to a two-year, $9 million contract with Minnesota. 
    For the first time in his career, the role he wanted and the one his team needed were in agreement.
    """
    return chunk


def basic_chunking():
    basic_chunk = """
    AFTER BEING DRAFTED by New Orleans and traded three times, Alexander-Walker finally had a choice of where he wanted to play when he became a free agent last summer.

    Remaining in Minnesota would give him the opportunity to do something he'd never done before either: start the season with the same coach he finished the previous year with.
    
    Finch said the team pitched him on both in an effort to bring him back.
    
    "It was so important to re-sign him," Finch said in December. "We saw what he could do to help this team last year down the stretch. He feels really comfortable here. I think we have a greater appreciation for who he is as a player. Now, the defense is way better than we had anticipated, and he understands that that's his ticket to making an impact on the floor."
    
    In July, Alexander-Walker agreed to a two-year, $9 million contract with Minnesota. For the first time in his career, the role he wanted and the one his team needed were in agreement.
    
    "It was a two-way buy-in," Boylan says. "We bought into him, but he bought into us at the same time."
    
    His teammates have bought in too.
    
    
    "For me, I respect work more than anything," Gobert tells ESPN. "And first of all, I love the way he works every day. And that translates to the court ... every minute that he is on the court. He takes every play serious. He takes every possession serious. ... Everything that he does has a purpose."
    
    """
    return basic_chunk


@app.post("/question-answering")
async def question_answering(input_request: LLMInput):


    if input_request.chunking_type == 'dynamic_chunking':
        chunk = dynamic_chunking()
    elif input_request.chunking_type == 'semantic_chunking':
        chunk = semantic_chunking()
    elif input_request.chunking_type == 'basic_chunking':
        chunk = basic_chunking()

    prompt = f"""You are a helpful assistant. Use the content provided to answer the inquiries
    
    CONTENT:
    
    {chunk}
    """

    openai_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_request.input_question},
        ]
    )
    response = openai_response.choices[0].message.content

    return response




if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3928)