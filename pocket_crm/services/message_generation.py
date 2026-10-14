from google import genai
from django.conf import settings
from apps.contacts.models import Contact

def generate_message_draft(contact: Contact, purpose=None, tone=None, length=None, custom_instruction=None):
    """
    Generates a personalized message draft using Gemini based on contact history.
    """
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    # Gather context
    memories = contact.memories.filter(include_in_drafts=True)
    interactions = contact.interactions.order_by('-occurred_at')[:5] # Last 5 interactions

    # Build prompt context
    context_parts = []
    context_parts.append(f"Contact Name: {contact.name}")
    if contact.relationship:
        context_parts.append(f"Relationship: {contact.get_relationship_display()}")
    
    if memories.exists():
        context_parts.append("\nRelevant Context (Memories):")
        for memory in memories:
            context_parts.append(f"- [{memory.get_category_display()}] {memory.content}")
            
    if interactions.exists():
        context_parts.append("\nRecent Interactions:")
        for interaction in interactions:
            summary = interaction.summary or "No summary recorded"
            context_parts.append(f"- {interaction.occurred_at.date()} ({interaction.get_channel_display()}): {summary}")

    # Build prompt instruction
    instruction_parts = ["Draft a message to the contact using the provided context."]
    if purpose:
        instruction_parts.append(f"Purpose: {purpose}")
    if tone:
        instruction_parts.append(f"Tone: {tone}")
    if length:
        instruction_parts.append(f"Length: {length}")
    if custom_instruction:
        instruction_parts.append(f"Additional Instructions: {custom_instruction}")
        
    prompt = "\n".join(instruction_parts) + "\n\n" + "\n".join(context_parts)

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Failed to generate message: {str(e)}")
