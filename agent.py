"""
Fixed Email Agent - Compatible with Latest CrewAI Version
Run this with: python agent.py
"""

from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
from datetime import datetime

# ============================================
# CUSTOM TOOLS (No decorator needed)
# ============================================

def analyze_email_tool(email_content: str) -> Dict[str, Any]:
    """
    Analyzes email content to extract key information like urgency and spam indicators.
    
    Args:
        email_content: The raw email text content
        
    Returns:
        Dictionary with analyzed email components
    """
    urgency_keywords = ['urgent', 'asap', 'important', 'deadline', 'meeting', 'confirm', 
                       'manager', 'client', 'tomorrow', 'today', 'emergency']
    
    is_urgent = any(keyword in email_content.lower() for keyword in urgency_keywords)
    
    spam_indicators = ['lottery', 'winner', 'click here', 'free money', 'nigerian prince', 
                      'congratulations you won', 'act now']
    is_spam = any(indicator in email_content.lower() for indicator in spam_indicators)
    
    return {
        'is_urgent': is_urgent,
        'is_spam': is_spam,
        'content_length': len(email_content)
    }


def classify_email_tool(email_content: str) -> str:
    """
    Classifies email into categories: Work, Personal, Spam, or Other.
    
    Args:
        email_content: The email text
        
    Returns:
        Classification category as string
    """
    # Check for spam first
    spam_indicators = ['lottery', 'winner', 'click here', 'free money']
    if any(indicator in email_content.lower() for indicator in spam_indicators):
        return "Spam"
    
    work_keywords = ['meeting', 'project', 'deadline', 'manager', 'client', 'proposal', 
                    'presentation', 'report', 'team', 'office', 'schedule']
    personal_keywords = ['friend', 'family', 'weekend', 'party', 'dinner', 'birthday']
    
    email_lower = email_content.lower()
    
    work_score = sum(1 for keyword in work_keywords if keyword in email_lower)
    personal_score = sum(1 for keyword in personal_keywords if keyword in email_lower)
    
    if work_score > personal_score:
        return "Work"
    elif personal_score > work_score:
        return "Personal"
    else:
        return "Other"


# ============================================
# AGENTS
# ============================================

def create_email_analyzer_agent() -> Agent:
    """Creates an agent specialized in analyzing emails"""
    return Agent(
        role='Email Analyzer',
        goal='Analyze emails to extract key information and determine urgency',
        backstory="""You are an expert at quickly reading and understanding emails. 
        You can identify important details, assess urgency, and detect spam or 
        unnecessary messages with high accuracy.""",
        verbose=True,
        allow_delegation=False
    )


def create_email_classifier_agent() -> Agent:
    """Creates an agent specialized in categorizing emails"""
    return Agent(
        role='Email Classifier',
        goal='Accurately classify emails into Work, Personal, Spam, or Other categories',
        backstory="""You are a master at categorizing emails based on their content, 
        context, and tone. You understand the nuances between professional and personal 
        communication.""",
        verbose=True,
        allow_delegation=False
    )


def create_email_summarizer_agent() -> Agent:
    """Creates an agent specialized in summarizing emails"""
    return Agent(
        role='Email Summarizer',
        goal='Create clear and concise 2-3 sentence summaries of emails',
        backstory="""You are skilled at distilling complex information into brief, 
        clear summaries. You capture the essence of any message in just a few sentences.""",
        verbose=True,
        allow_delegation=False
    )


def create_reply_writer_agent() -> Agent:
    """Creates an agent specialized in drafting professional replies"""
    return Agent(
        role='Reply Writer',
        goal='Draft professional, contextually appropriate email replies',
        backstory="""You are an expert communicator who writes polite, concise, and 
        professional email replies. You adapt your tone based on whether the email is 
        work-related or personal, always maintaining professionalism.""",
        verbose=True,
        allow_delegation=False
    )


# ============================================
# NOTIFICATION SYSTEM
# ============================================

class NotificationManager:
    """Manages console notifications"""
    
    def send_notification(self, message: str, title: str = "Email Alert"):
        """Send console notification"""
        print("\n" + "="*70)
        print(f"🔔 {title}")
        print("="*70)
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📧 {message}")
        print("="*70 + "\n")


# ============================================
# MAIN EMAIL ASSISTANT
# ============================================

class EmailAssistant:
    """Main class that orchestrates the email processing workflow"""
    
    def __init__(self):
        self.analyzer_agent = create_email_analyzer_agent()
        self.classifier_agent = create_email_classifier_agent()
        self.summarizer_agent = create_email_summarizer_agent()
        self.reply_agent = create_reply_writer_agent()
        self.notifier = NotificationManager()
    
    def process_email(self, email_content: str) -> Dict[str, str]:
        """
        Process an email through the complete workflow
        
        Args:
            email_content: The raw email text
            
        Returns:
            Dictionary with summary, classification, reply, and notification
        """
        print(f"\n⏳ Processing email at {datetime.now().strftime('%H:%M:%S')}...")
        
        # STEP 1: Quick urgency check for real-time notification
        if self._is_urgent(email_content):
            subject = self._extract_subject(email_content)
            self.notifier.send_notification(
                message=f"Important email received: {subject}",
                title="🚨 URGENT EMAIL ALERT"
            )
        
        # STEP 2: Analyze email
        print("\n📊 Step 1: Analyzing email...")
        analysis_result = analyze_email_tool(email_content)
        print(f"   ✅ Analysis complete: {analysis_result}")
        
        # STEP 3: Classify email
        print("\n📂 Step 2: Classifying email...")
        classification = classify_email_tool(email_content)
        print(f"   ✅ Classification: {classification}")
        
        # STEP 4: Summarize email using AI
        print("\n📝 Step 3: Generating summary...")
        summary_task = Task(
            description=f"""Summarize the following email in 2-3 clear, concise sentences.
            
            Email Content:
            {email_content}
            
            Capture the main point, any requests, and key details.""",
            expected_output="A 2-3 sentence summary of the email",
            agent=self.summarizer_agent
        )
        
        summary_crew = Crew(
            agents=[self.summarizer_agent],
            tasks=[summary_task],
            process=Process.sequential,
            verbose=False
        )
        
        summary = str(summary_crew.kickoff()).strip()
        print(f"   ✅ Summary generated")
        
        # STEP 5: Draft reply using AI
        print("\n✍️  Step 4: Drafting reply...")
        
        tone_guide = {
            "Work": "professional, respectful tone",
            "Personal": "friendly and warm tone",
            "Spam": "polite indication that no reply is needed",
            "Other": "neutral, polite tone"
        }
        
        reply_task = Task(
            description=f"""Draft a professional reply to the following email.
            
            Email Content:
            {email_content}
            
            Classification: {classification}
            
            Guidelines:
            - Use {tone_guide.get(classification, 'professional tone')}
            - Keep it concise and contextually appropriate
            - Address any requests or questions in the email
            - If spam, simply state no reply is needed""",
            expected_output="A professional, well-formatted email reply",
            agent=self.reply_agent
        )
        
        reply_crew = Crew(
            agents=[self.reply_agent],
            tasks=[reply_task],
            process=Process.sequential,
            verbose=False
        )
        
        reply = str(reply_crew.kickoff()).strip()
        print(f"   ✅ Reply drafted")
        
        # STEP 6: Generate notification text
        notification = self._generate_notification(email_content)
        
        return {
            'summary': summary,
            'classification': classification,
            'reply': reply,
            'notification': notification
        }
    
    def _is_urgent(self, email_content: str) -> bool:
        """Quick urgency check for real-time alerts"""
        urgent_keywords = ['urgent', 'meeting', 'deadline', 'manager', 'client', 
                          'tomorrow', 'today', 'asap', 'important', 'emergency']
        return any(keyword in email_content.lower() for keyword in urgent_keywords)
    
    def _extract_subject(self, email_content: str) -> str:
        """Extract subject or first line from email"""
        lines = email_content.strip().split('\n')
        subject = lines[0] if lines else "New Email"
        return subject[:60] + "..." if len(subject) > 60 else subject
    
    def _generate_notification(self, email_content: str) -> str:
        """Generate notification text for output"""
        if self._is_urgent(email_content):
            subject = self._extract_subject(email_content)
            return f"🚨 IMPORTANT EMAIL ALERT: {subject}"
        return "None"
    
    def format_output(self, result: Dict[str, str]) -> str:
        """Format the final output in the specified structure"""
        return f"""Summary: {result['summary']}
Classification: {result['classification']}
Draft Reply: {result['reply']}
Notification: {result['notification']}"""


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("="*70)
    print("EMAIL AGENT - SMART EMAIL ASSISTANT")
    print("="*70)
    
    # Initialize the Email Assistant
    assistant = EmailAssistant()
    
    # Example 1: Urgent work email
    print("\n📧 EXAMPLE 1: Urgent Work Email")
    print("-"*70)
    
    example_email_1 = """Email:  
Hello Laxmana,  
I'd like to schedule an URGENT meeting tomorrow at 3PM to discuss the AI project.  
Please confirm your availability immediately.
Regards,  
Project Manager"""
    
    result1 = assistant.process_email(example_email_1)
    
    print("\n" + "="*70)
    print("📋 RESULT")
    print("="*70)
    print(assistant.format_output(result1))
    print("="*70)
    
    # Example 2: Personal email
    print("\n\n📧 EXAMPLE 2: Personal Email")
    print("-"*70)
    
    example_email_2 = """Email:
Hey Laxmana!
How are you doing? Want to grab dinner this weekend? 
Let me know if Saturday works for you!
Cheers,
Raj"""
    
    result2 = assistant.process_email(example_email_2)
    
    print("\n" + "="*70)
    print("📋 RESULT")
    print("="*70)
    print(assistant.format_output(result2))
    print("="*70)
    
    # Example 3: Spam email
    print("\n\n📧 EXAMPLE 3: Spam Email")
    print("-"*70)
    
    example_email_3 = """Email:
CONGRATULATIONS! You've won the lottery!
Click here now to claim your free money!
Act now, limited time offer!"""
    
    result3 = assistant.process_email(example_email_3)
    
    print("\n" + "="*70)
    print("📋 RESULT")
    print("="*70)
    print(assistant.format_output(result3))
    print("="*70)
    
    print("\n✅ All examples completed!")
    print("\n💡 To process your own emails, modify the email content and run again."
          )
