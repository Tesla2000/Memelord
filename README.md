![Name all memes](doc_images/name_all_memes.png)

Have you ever found yourself in a situation where you needed just the right meme to express how you feel—but couldn’t find one that fit?

Believe me, that’s a skill issue. Luckily for you, you now have access to this **amazing** tool that gets the job done.

In the current version of the project, I'm using a **tournament approach**, selecting the memes best suited for a specific message and advancing them through rounds until the pool is narrowed down to the desired number.

![You have to admire the simplicity of the design](doc_images/simplicity_of_design.png)

A more advanced version includes **utterances with embedding distance**, which LLMs are currently unable to produce reliably.

![I'm limited by the technology of my age](doc_images/technology_limit.png)

---

## How to Run

### Setup

#### Linux/macOS
```bash
# Create virtual environment and install dependencies
make setup

# Add your OpenAI API key to .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Activate the virtual environment
source .venv/bin/activate
```

#### Windows
```cmd
# Create virtual environment and install dependencies
make setup-win

# Add your OpenAI API key to .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Activate the virtual environment
.venv\Scripts\activate
```

### Running the Application

#### Linux/macOS
```bash
# Run with a message
python main.py "Can I trust you?"
```

#### Windows
```cmd
# Run with a message
python main.py "Can I trust you?"
```

### Example Output
```
All Right Then, Keep Your Secrets https://i.imgflip.com/4/2lcdkl.jpg
It's a trap https://i.imgflip.com/4/jl52i.jpg
I find your lack of faith disturbing https://i.imgflip.com/4/t88mx.jpg
Trust Nobody, Not Even Yourself https://i.imgflip.com/4/26wvib.jpg
Grumpy Cat Does Not Believe https://i.imgflip.com/4/cend.jpg
```
