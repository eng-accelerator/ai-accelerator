# Challenge 2: Personality Selector

**Difficulty**: Beginner-Intermediate
**Estimated Time**: 25-35 minutes
**Focus**: Session state management, system prompts, UI controls

## Challenge Description

Transform your chatbot into a versatile assistant with multiple personalities that users can select from. Each personality should have a distinct communication style, expertise area, and approach to helping users.

## User Story

*"As a user, I want to choose from different AI personality modes (like Professional, Creative, Technical, etc.) so that I get responses that match the style and expertise I need for my current task."*

## Requirements

### Core Features (Must Have)
- [x] **Personality Selection**: Sidebar dropdown with at least 4 personality options
- [x] **Dynamic System Prompts**: Each personality uses a different system prompt
- [x] **Visual Indicators**: Show current personality in the chat interface
- [x] **Personality Persistence**: Remember selected personality across conversation

### Advanced Features (Nice to Have)
- [x] **Custom Personality**: Allow users to define their own personality
- [x] **Personality Descriptions**: Show what each personality is good for
- [x] **Response Style Preview**: Show example responses for each personality
- [x] **Personality Switching**: Allow mid-conversation personality changes

## Personality Options

### 1. Professional Business Assistant
- **Style**: Formal, structured, business-focused
- **Expertise**: Business strategy, professional communication
- **Tone**: Polite, efficient, results-oriented

### 2. Creative Writing Helper
- **Style**: Imaginative, expressive, inspiring
- **Expertise**: Creative writing, storytelling, artistic projects
- **Tone**: Enthusiastic, artistic, encouraging

### 3. Technical Expert
- **Style**: Precise, detailed, code-focused
- **Expertise**: Programming, technology, problem-solving
- **Tone**: Analytical, methodical, educational

### 4. Friendly Companion
- **Style**: Casual, supportive, conversational
- **Expertise**: General chat, emotional support, casual advice
- **Tone**: Warm, empathetic, encouraging

### 5. Custom Personality (Advanced)
- **Style**: User-defined
- **Expertise**: User-specified
- **Tone**: Customizable

## Technical Approach

You'll modify your existing chatbot to:

1. **Add Personality State**: Track selected personality in session state
2. **System Prompt Engineering**: Create distinct prompts for each personality
3. **UI Enhancement**: Add sidebar controls for personality selection
4. **Message Context**: Inject personality context into conversation

## Key Learning Objectives

- Master system prompt engineering for different use cases
- Implement dynamic behavior based on user selections
- Create intuitive personality switching UX
- Understand how context shapes AI responses

## Getting Started

1. Copy your working chatbot from the main workshop
2. Add personality selection to the sidebar
3. Create system prompts for each personality
4. Implement dynamic prompt switching

## Example Interactions

**Professional Mode**:
```
User: "How do I handle a difficult client meeting?"
Assistant: "I recommend a structured approach to managing challenging client interactions:

1. Preparation: Review all relevant documentation beforehand
2. Active Listening: Allow the client to express their concerns fully
3. Solution-Focused Discussion: Present 2-3 concrete options
4. Clear Next Steps: Document agreed actions with timelines

Would you like me to elaborate on any of these strategies?"
```

**Creative Mode**:
```
User: "How do I handle a difficult client meeting?"
Assistant: "Ah, the art of navigating stormy client waters! 🎭

Picture this: You're not just attending a meeting, you're crafting a story where everyone wins. Start by becoming a master listener - let their frustrations paint the full picture. Then, like a skilled storyteller, weave their concerns into solutions that feel like plot twists they never saw coming!

Transform the tension into creative energy. What if this 'difficult' meeting becomes the turning point where you surprise them with innovative approaches they hadn't considered? ✨"
```

## Success Criteria

Your personality selector should:
✅ Offer at least 4 distinct personalities
✅ Show clear differences in response style
✅ Maintain personality consistency throughout conversation
✅ Allow personality switching mid-conversation
✅ Display current personality clearly to users
✅ Handle personality changes gracefully

## Extension Ideas

- Add personality-specific conversation starters
- Implement personality learning (adapt based on user feedback)
- Create personality profiles with detailed descriptions
- Add visual avatars for each personality
- Enable personality mixing (combine traits from multiple personalities)

Remember: The goal is to understand how system prompts shape AI behavior. Experiment with different prompt styles and see how dramatically they change the responses!