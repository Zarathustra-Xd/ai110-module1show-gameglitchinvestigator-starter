# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

--> Allowed attempts shows 7, when it's supposed to be 8.

--> "Out of attempts" error message shows up even when the attemps left is 1. It should show up when the attempts left is 0.

--> Pressing Enter doesn't submit the guess. The guess should be submitted with pressing Enter.

--> Hints are reversed. It says "Go Lower" instead of "Go Higher", and vice versa.

--> New game button does not renews Attemps, Score, and History. It doesn't start a new game. It should start a fresh game with all the attributes renewed.

--> Whe you change the difficulty level, it still says "Guess a number between 1 and 100." It should change according to the difficulty level.

--> The difficulty level are not set according to the actual difficulty of the game. Guessing between 1 to 100 should be harder than guessing between 1 to 50. But in our program, hard is 1 to 50 and normal is 1 to 100.


## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

--> I used ChatGPT as my primary AI tool while working on this project.

--> One helpful suggestion it gave was to use a Streamlit form (st.form) so that pressing the Enter key submits the guess, instead of requiring the user to click the submit button. I tested this by running the app after implementing the change and confirming that pressing Enter correctly triggered the guess submission.

--> However, one suggestion was misleading when debugging the attempt counter display. The AI initially suggested moving the st.info() block below the submit logic, which fixed the counter but unintentionally changed the UI layout of the app. After testing it, I realized the layout change was undesirable, so I instead adjusted the displayed value of remaining attempts while keeping the UI structure the same. This experience showed me that AI suggestions can be helpful, but they still need to be tested and sometimes adapted to fit the program’s design.



## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

--> I decided a bug was fixed by testing it manually in the Streamlit app and observing the behavior directly. For example, after fixing the hints, I submitted a guess higher than the secret number and confirmed that the message said "Go LOWER!" instead of the backwards "Go HIGHER!". Once I was confident the specific bug behavior had changed, I knew the fix was working.

--> I ran pytest on the test suite we created for logic_utils.py, which tested all four functions (get_range_for_difficulty, parse_guess, check_guess, and update_score) with various inputs including edge cases like boundary values and invalid inputs. When I first ran pytest, all tests passed, showing that the refactored functions in logic_utils.py were working correctly and that the hints, scoring, and range validation were all functioning as expected. This gave me confidence that the logic errors had been properly fixed and wouldn't regress.

--> Yes, AI helped me design the test suite by suggesting comprehensive test cases that covered multiple scenarios for each function. For example, for the check_guess function, AI suggested tests for winning guesses, too high, too low, and boundary cases (guesses just above/below the secret). For update_score, AI helped me understand how the scoring logic worked (winning deducts points based on attempts, wrong guesses affect score differently) and suggested tests for even/odd attempts. This structured approach to testing helped me catch potential edge case bugs that I might have missed with manual testing alone.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

--> Streamlit "reruns" are like hitting refresh on a website every time the user interacts with it. When a user clicks a button, types in a text box, or changes a slider, Streamlit runs the entire Python script from top to bottom again to update what the user sees. This is different from traditional web apps where only the specific part you changed gets updated. Because of this rerun behavior, any variable you create normally gets reset to its initial value every time Streamlit reruns, which would be a problem for tracking game progress.

--> Session state is Streamlit's solution to this problem—it's like a memory bank that persists across reruns. You store important data in `st.session_state` (like the secret number or attempts count), and even though the script reruns, those values are preserved from the last rerun. In our game, if we hadn't used session_state to store the secret number, it would have generated a new random number every time the user submitted a guess, making the game unplayable. I learned this the hard way when bugs in the attempt counter and secret number regeneration forced me to understand how session_state works and how the order of my code matters—I had to move the UI display elements to render after the state updates, not before.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

--> The habit I want to reuse is creating comprehensive test cases with edge cases early in the debugging process. Instead of just manually testing the happy path, I'll write tests that cover boundary conditions, invalid inputs, and different scenarios (like even/odd attempts, wins on first try vs. later attempts, etc.). This strategy helped me gain confidence in my fixes and prevented regressions. I also want to continue using git commits frequently to track progress on each bug fix, making it easy to see what changed and why.

--> Next time I work with AI on a coding task, I would ask the AI to explain what the code does and why it's the right approach, rather than just accepting the generated code at face value. I would also be more skeptical of AI suggestions that seem to "just work"—I'd test them in the actual context (like UI changes in Streamlit) to make sure they don't have unintended side effects. This project showed me that AI can suggest fixes that technically work but aren't ideal for the overall design.

--> This project fundamentally changed how I view AI-generated code: it's not production-ready and shouldn't be trusted without verification. AI can introduce subtle bugs (like the reversed hints and the str/int conversion logic) that seem reasonable at first but break functionality, so I now see my role as a critical reviewer who tests, debugs, and validates AI work rather than simply implementing it.
