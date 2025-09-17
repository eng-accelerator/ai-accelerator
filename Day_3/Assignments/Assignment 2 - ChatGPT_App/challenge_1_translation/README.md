# Challenge 1: Translation Mode

**Difficulty**: Intermediate
**Estimated Time**: 30-40 minutes
**Focus**: System prompts, multiple API calls, language detection

## Challenge Description

Transform your basic chatbot into an intelligent translation assistant that can automatically detect languages and provide high-quality translations with cultural context.

## User Story

*"As a user, I want to type text in any language and have the chatbot automatically detect the language and offer to translate it to my preferred target language. The bot should also provide cultural context and alternative translations when relevant."*

## Requirements

### Core Features (Must Have)
- [x] **Language Detection**: Automatically identify the input language
- [x] **Translation**: Translate text to user-selected target language
- [x] **Language Selection**: Sidebar control for target language selection
- [x] **Bidirectional Translation**: Support translation in both directions

### Advanced Features (Nice to Have)
- [x] **Cultural Context**: Provide cultural notes for idiomatic expressions
- [x] **Alternative Translations**: Offer multiple translation options
- [x] **Confidence Scoring**: Show confidence level of detection/translation
- [x] **Translation History**: Keep track of translation pairs

## Technical Approach

You'll need to modify your existing chatbot to:

1. **System Prompt Engineering**: Create a specialized prompt for translation tasks
2. **Two-Stage Process**: First detect language, then translate
3. **State Management**: Track source/target languages in session state
4. **UI Enhancements**: Add language selection controls

## Key Learning Objectives

- Master system prompt engineering for specialized tasks
- Handle multiple API calls in sequence
- Implement conditional logic based on AI responses
- Create professional translation UX patterns

## Getting Started

1. Copy your working chatbot from the main workshop
2. Add language selection to the sidebar
3. Modify the system prompt for translation tasks
4. Implement the two-stage detection + translation process

## Example Interactions

**Input**: "Bonjour, comment allez-vous?"
**Output**:
```
🔍 Detected Language: French
🎯 Translation (English): "Hello, how are you?"

💡 Cultural Note: This is a formal greeting in French. In casual settings,
   you might hear "Salut, ça va?" instead.
```

**Input**: "I love this weather"
**Output**:
```
🔍 Detected Language: English
🎯 Translation (Spanish): "Me encanta este clima"

🌟 Alternative: "Adoro este tiempo" (more emphatic)
💡 Regional Note: In Mexico, you might also hear "está padrísimo el clima"
```

## Hints Available

- Progressive hints in `hints.md`
- Complete solution in `solution.py`
- Don't peek at the solution until you've tried for at least 20 minutes!

## Success Criteria

Your translation bot should:
✅ Automatically detect input language
✅ Translate accurately to target language
✅ Provide cultural context when relevant
✅ Handle errors gracefully
✅ Maintain conversation history
✅ Have intuitive language selection UI

## Extension Ideas

- Add support for document translation
- Implement translation confidence scoring
- Create translation glossaries for technical terms
- Add pronunciation guides
- Support batch translation of multiple texts

Good luck! Remember, the goal is to learn the patterns - don't be afraid to experiment and iterate.