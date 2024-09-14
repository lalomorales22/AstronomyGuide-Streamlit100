# Astronomy Guide: Virtual Universe Explorer

Embark on a cosmic journey with Astronomy Guide, an interactive Streamlit application designed to provide a virtual exploration of the universe. This educational tool leverages AI technology to offer an immersive learning experience about celestial objects, astronomical phenomena, and the wonders of space.

## Features

- Virtual tours of celestial bodies and cosmic regions
- Multiple learning modes (e.g., Concept Explanation, Historical Timeline, Space News)
- AI-powered explanations and interactive quizzes
- Customizable difficulty levels for learners of all backgrounds
- Real-time space news and updates
- Scientist spotlights and equipment guides
- Dark/Light theme for comfortable viewing
- Conversation saving and loading for continued exploration
- Token usage tracking for AI interactions

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/lalomorales22/AstronomyGuide-Streamlit100.git
   cd AstronomyGuide-Streamlit100
   ```

2. Set up a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

1. Launch the application:
   ```
   streamlit run app.py
   ```

2. Access the app in your browser at `http://localhost:8501`

3. Start your cosmic journey:
   - Select an astronomy topic
   - Choose a learning mode
   - Set your preferred difficulty level
   - Engage with the AI guide to explore the universe!

## Learning Modes

- Virtual Tour: Take a guided journey through space
- Concept Explanation: Deep dive into astronomical theories
- Historical Timeline: Explore the history of space discovery
- Interactive Quiz: Test your cosmic knowledge
- Image Analysis: Understand astronomy through visuals
- Space News: Stay updated with the latest discoveries
- Astronomical Phenomena: Learn about celestial events
- Scientist Spotlight: Meet the minds behind astronomy
- Equipment Guide: Understand tools used in space exploration

## Customization

Modify `ASTRONOMY_TOPICS` and `LEARNING_MODES` in `app.py` to expand or focus the app's content.

## Contributing

Contributions to improve Astronomy Guide are welcome! Please feel free to submit pull requests or open issues for discussion.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the astronomy community for inspiration and factual verification
- Gratitude to the open-source contributors of the libraries used in this project

Explore the cosmos from the comfort of your screen with Astronomy Guide!
