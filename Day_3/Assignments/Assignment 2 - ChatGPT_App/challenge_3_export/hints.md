# Challenge 3: Export Functionality - Progressive Hints

Use these hints if you get stuck, but try to implement as much as possible on your own first!

## Hint 1: Getting Started (5 minutes in)

**If you're not sure where to begin:**

Start by adding a basic export button to your sidebar:

```python
with st.sidebar:
    st.header("📤 Export")

    if st.session_state.messages:
        if st.button("Export as TXT"):
            # We'll implement this next
            pass
    else:
        st.info("No conversation to export yet.")
```

Focus on getting the UI structure in place first, then worry about the actual export logic.

---

## Hint 2: Basic TXT Export (10 minutes in)

**If you want to start with a simple text export:**

Create a function to convert your messages to text:

```python
def export_as_txt(messages):
    txt_content = "Chat Export\n"
    txt_content += "=" * 20 + "\n\n"

    for message in messages:
        role = "You" if message["role"] == "user" else "Assistant"
        txt_content += f"{role}: {message['content']}\n\n"

    return txt_content

# In your sidebar
if st.button("Export as TXT"):
    content = export_as_txt(st.session_state.messages)
    st.text_area("Export content:", content, height=200)
```

This gives you a basic export. We'll make it downloadable next!

---

## Hint 3: Adding Download Functionality (15 minutes in)

**If you want users to actually download the file:**

Use Streamlit's `st.download_button`:

```python
if st.button("Export as TXT"):
    content = export_as_txt(st.session_state.messages)

    # Generate filename with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_export_{timestamp}.txt"

    st.download_button(
        label="💾 Download TXT",
        data=content,
        file_name=filename,
        mime="text/plain"
    )
```

Now users can actually save the file to their computer!

---

## Hint 4: Adding Timestamps (20 minutes in)

**If you want to include timestamps in your exports:**

First, you need to add timestamps to your messages when they're created:

```python
# When adding messages to session state
from datetime import datetime

message = {
    "role": role,
    "content": content,
    "timestamp": datetime.now()
}
st.session_state.messages.append(message)
```

Then use them in your export:

```python
def export_as_txt(messages):
    txt_content = "Chat Export\n"
    txt_content += "=" * 20 + "\n\n"

    for message in messages:
        role = "You" if message["role"] == "user" else "Assistant"

        if "timestamp" in message:
            time_str = message["timestamp"].strftime("%H:%M:%S")
            txt_content += f"[{time_str}] {role}: {message['content']}\n\n"
        else:
            txt_content += f"{role}: {message['content']}\n\n"

    return txt_content
```

---

## Hint 5: JSON Export (25 minutes in)

**If you want to add JSON export functionality:**

```python
import json

def export_as_json(messages):
    export_data = {
        "export_timestamp": datetime.now().isoformat(),
        "total_messages": len(messages),
        "conversation": []
    }

    for i, message in enumerate(messages):
        msg_data = {
            "message_id": i + 1,
            "role": message["role"],
            "content": message["content"]
        }

        if "timestamp" in message:
            msg_data["timestamp"] = message["timestamp"].isoformat()

        export_data["conversation"].append(msg_data)

    return json.dumps(export_data, indent=2)

# In sidebar
export_format = st.selectbox("Export Format:", ["TXT", "JSON"])

if st.button("📤 Export"):
    if export_format == "TXT":
        content = export_as_txt(st.session_state.messages)
        mime = "text/plain"
        ext = "txt"
    else:  # JSON
        content = export_as_json(st.session_state.messages)
        mime = "application/json"
        ext = "json"

    filename = f"chat_export_{timestamp}.{ext}"
    st.download_button("💾 Download", content, filename, mime)
```

---

## Hint 6: CSV Export (30 minutes in)

**If you want to add CSV export for data analysis:**

```python
import csv
import io

def export_as_csv(messages):
    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(["Message_ID", "Role", "Content", "Character_Count"])

    # Data rows
    for i, message in enumerate(messages, 1):
        writer.writerow([
            i,
            message["role"],
            message["content"].replace('\n', ' '),  # Clean newlines
            len(message["content"])
        ])

    return output.getvalue()
```

CSV is great for importing into spreadsheets and data analysis tools!

---

## Hint 7: Adding Statistics (35 minutes in)

**If you want to include conversation statistics:**

```python
def calculate_stats(messages):
    if not messages:
        return {}

    user_messages = [m for m in messages if m["role"] == "user"]
    assistant_messages = [m for m in messages if m["role"] == "assistant"]

    return {
        "total_messages": len(messages),
        "user_messages": len(user_messages),
        "assistant_messages": len(assistant_messages),
        "total_characters": sum(len(m["content"]) for m in messages),
        "average_length": sum(len(m["content"]) for m in messages) // len(messages)
    }

# Include in your export functions
def export_as_txt(messages):
    stats = calculate_stats(messages)

    txt_content = f"Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    txt_content += "=" * 50 + "\n\n"

    # Add statistics
    txt_content += "STATISTICS:\n"
    txt_content += f"Total Messages: {stats['total_messages']}\n"
    txt_content += f"User Messages: {stats['user_messages']}\n"
    txt_content += f"Assistant Messages: {stats['assistant_messages']}\n"
    txt_content += f"Total Characters: {stats['total_characters']}\n\n"

    # Add conversation...
    # (rest of your export logic)
```

---

## Hint 8: Export Settings/Options (40+ minutes in)

**If you want to give users control over what gets exported:**

```python
with st.sidebar.expander("Export Settings"):
    include_timestamps = st.checkbox("Include Timestamps", True)
    include_stats = st.checkbox("Include Statistics", True)
    export_range = st.selectbox("Export Range", ["All Messages", "Last 10", "Last 50"])

# Use these settings in your export functions
def export_as_txt(messages, include_timestamps=True, include_stats=True):
    # Modify your export logic based on these settings
    pass
```

This gives users fine-grained control over their exports.

---

## Common Issues & Solutions

### "Download button doesn't work"
- Make sure you're returning the content from your export function
- Check that the `data` parameter in `st.download_button` contains your content
- Verify the MIME type is correct for your file format

### "Special characters look weird in exports"
- Add encoding handling: `content.encode('utf-8')`
- For JSON: use `ensure_ascii=False` in `json.dumps()`
- For CSV: handle quotes and commas properly

### "Timestamps are missing"
- Make sure you're adding timestamps when messages are created
- Handle cases where old messages don't have timestamps
- Use try/except for timestamp formatting

### "Large conversations cause issues"
- Add progress indicators for large exports
- Consider chunking large exports
- Add memory management for very long conversations

---

## Advanced Features to Try

If you finish early:

1. **ZIP Export**: Bundle multiple formats together
```python
import zipfile
import io

def create_zip_export(messages):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr("chat.txt", export_as_txt(messages))
        zip_file.writestr("chat.json", export_as_json(messages))
    return zip_buffer.getvalue()
```

2. **Export Filtering**: Let users export date ranges or specific message types

3. **Rich Statistics**: Add word counts, reading time estimates, conversation topics

4. **Preview**: Show a preview of the export before downloading

5. **Multiple Conversations**: If you have session management, export multiple conversations

---

## Testing Your Implementation

Try these test scenarios:
- **Empty Conversation**: What happens when there are no messages?
- **Special Characters**: Messages with emojis, newlines, quotes
- **Large Conversation**: 50+ messages to test performance
- **Different Formats**: Verify all formats work correctly
- **Settings**: Test different export options

Remember: The goal is creating genuinely useful exports. Think about how users would actually want to use these files!