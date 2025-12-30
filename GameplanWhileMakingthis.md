Here was my thought process as I made this application:

Your goal is to design a simple Q&A web tool over medical policies; in particular, this BCBS policy for total knee arthroplasty. The system should comprise of:
A simple frontend that can accept user input and stream a thinking + final response from the backend
An agentic architecture that can perform grounded Q&A based on medical information in a single policy, and scale to multiple policies

    Requirements:
        We need to create a place to accept user input.
        We need to stream chain of Thought + a final response from the backend
            we probably want to makde it extensible to multiple policies
        Agentic Architecture to do Questions and Answers based on medical information that can scale to multiple policies.

MVD:
user input -> edit variable field
stream chain of thought -> chatbot.py with anthropic documentation
    over medical policy -> rag chromadb with embedded chunks

Post-design, we’ll focus our efforts on implementation of the agentic architecture on the backend. Concretely, our goal is to design an agent that
Accepts a user’s input (a question about the policy)
Performs multiple query steps to find the relevant sections that might answer the question, in a loop. The policy will initially be represented as a PDF, and there’s flexibility about how to properly read and extract relevant information here.
Streams intermediate progress as response (there’s flexibility on how to implement this)
When relevant stopping conditions are met, synthesize the information and return it to the user

Feel free to use whichever language you please. We ask that you restrict AI coding assistant use to “tab-complete” (as opposed to end-to-end workflow) tools, until the initial agent is complete. If time remains to plug this into the rest of a fully functioning implementation, workflow tools are permitted.
