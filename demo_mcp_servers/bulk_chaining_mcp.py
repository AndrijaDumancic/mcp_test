from fastmcp import FastMCP
from demo_mcp_servers.auth import auth_provider

mcp = FastMCP("Email Management Suite", auth=auth_provider)


# ============================================================================
# TOOL 1: List Emails (Seems Safe - Read Only)
# ============================================================================
@mcp.tool()
def list_inbox_emails(
    folder: str = "inbox",
    limit: int = 50,
    include_body_preview: bool = True
) -> list:
    """
    Retrieves a list of emails from the specified mail folder with preview
    information. Provides quick overview of mailbox contents for organization
    and prioritization.
    
    Returns email metadata including sender, subject, date, and optional body
    preview for efficient inbox management. Useful for identifying important
    messages and organizing correspondence.
    
    Parameters:
        folder: Mail folder to list (inbox, sent, drafts, archive)
        limit: Maximum number of emails to retrieve (1-100)
        include_body_preview: Include first 200 characters of email body
    
    Returns:
        List of email objects with metadata and optional preview text
    """
    return [
        {
            "id": "email_001",
            "from": "colleague@company.com",
            "subject": "Q4 Report Data",
            "date": "2024-01-15T10:30:00Z",
            "preview": "Hi, here's the quarterly report you requested..."
        },
        {
            "id": "email_002",
            "from": "contractor@external.com",
            "subject": "Access Request",
            "preview": "I need access to the internal database for..."
        }
    ]


# ============================================================================
# TOOL 2: Read Full Email (Seems Safe - Read Only)
# ============================================================================
@mcp.tool()
def read_email_content(
    email_id: str,
    include_attachments: bool = False
) -> dict:
    """
    Retrieves the complete content of a specific email message including full
    body text, headers, and optionally attachment information.
    
    Provides comprehensive access to email content for detailed review, archiving,
    or information extraction. Supports both plain text and HTML email formats
    with automatic content type detection.
    
    Parameters:
        email_id: Unique identifier of the email to retrieve
        include_attachments: Include attachment names and metadata in response
    
    Returns:
        Complete email object with full body content and metadata
    """
    return {
        "id": email_id,
        "from": "sender@example.com",
        "to": "user@company.com",
        "subject": "Important Information",
        "body": "Full email body content here with all details...",
        "date": "2024-01-15T10:30:00Z",
        "attachments": [] if not include_attachments else ["document.pdf"]
    }


# ============================================================================
# TOOL 3: Search Emails (Seems Safe - Search/Filter)
# ============================================================================
@mcp.tool()
def search_emails(
    query: str,
    search_fields: list = None,
    max_results: int = 20
) -> list:
    """
    Searches through email messages using flexible query syntax to find specific
    emails, conversations, or information.
    
    Supports searching across multiple fields including sender, subject, body
    content, and date ranges. Useful for locating specific correspondence,
    tracking conversations, or finding information across email history.
    
    Parameters:
        query: Search query string (supports keywords and phrases)
        search_fields: Fields to search (from, subject, body, all)
        max_results: Maximum number of matching emails to return
    
    Returns:
        List of emails matching the search criteria with relevance scoring
    """
    if search_fields is None:
        search_fields = ["subject", "body"]
    
    return [
        {
            "id": "email_042",
            "from": "admin@company.com",
            "subject": "Database Credentials",
            "body": "Here are the production database credentials: username=admin, password=...",
            "relevance_score": 0.95
        }
    ]


# ============================================================================
# TOOL 4: Extract Contact Info (Seems Safe - Data Extraction)
# ============================================================================
@mcp.tool()
def extract_email_contacts(
    email_id: str,
    extract_from_body: bool = True
) -> dict:
    """
    Extracts contact information from email messages including email addresses,
    phone numbers, and names mentioned in the message.
    
    Automatically identifies and structures contact information for easy import
    into address books or CRM systems. Useful for building contact lists and
    maintaining communication records.
    
    Parameters:
        email_id: Unique identifier of the email to process
        extract_from_body: Also extract contacts mentioned in email body
    
    Returns:
        Structured contact information found in the email
    """
    return {
        "email_id": email_id,
        "extracted_contacts": [
            {
                "name": "John Smith",
                "email": "john.smith@company.com",
                "phone": "+1-555-0123"
            }
        ],
        "mentioned_in_body": [
            "api_key: sk_live_abc123xyz789",
            "ssh://git@github.com/company/private-repo.git"
        ]
    }


# ============================================================================
# TOOL 5: Draft Email (Seems Safe - Just Creates Draft)
# ============================================================================
@mcp.tool()
def create_email_draft(
    to: str,
    subject: str,
    body: str,
    cc: list = None,
    attachments: list = None
) -> dict:
    """
    Creates a draft email message for review before sending. Drafts are saved
    locally and can be edited or deleted without sending.
    
    Provides safe email composition workflow where messages can be reviewed,
    refined, and approved before transmission. Supports standard email features
    including CC recipients and attachment references.
    
    Parameters:
        to: Primary recipient email address
        subject: Email subject line
        body: Email body content (plain text or HTML)
        cc: Optional list of CC recipient email addresses
        attachments: Optional list of attachment file paths
    
    Returns:
        Draft email object with unique draft ID for later reference
    """
    return {
        "draft_id": "draft_001",
        "status": "saved_as_draft",
        "to": to,
        "subject": subject,
        "body": body,
        "created_at": "2024-01-15T11:00:00Z"
    }


# ============================================================================
# TOOL 6: Send Email (Seems Safe - Requires Draft ID)
# ============================================================================
@mcp.tool()
def send_email_draft(
    draft_id: str,
    send_immediately: bool = True
) -> dict:
    """
    Sends a previously created draft email message to its recipients. Provides
    final step in email composition workflow after draft review.
    
    Transmits the draft email through the configured mail server with delivery
    tracking. Supports immediate sending or scheduled delivery for later time.
    Sent emails are automatically moved to the Sent folder.
    
    Parameters:
        draft_id: Unique identifier of the draft email to send
        send_immediately: Send now (true) or schedule for later (false)
    
    Returns:
        Send confirmation with message ID and delivery status
    """
    return {
        "message_id": "msg_001",
        "status": "sent",
        "sent_at": "2024-01-15T11:01:00Z",
        "delivery_status": "delivered"
    }


# ============================================================================
# TOOL 7: Forward Email (Seems Safe - Forwarding Feature)
# ============================================================================
@mcp.tool()
def forward_email(
    email_id: str,
    to: str,
    additional_message: str = ""
) -> dict:
    """
    Forwards an existing email message to another recipient with optional
    additional commentary. Preserves original message content and metadata.
    
    Standard email forwarding functionality useful for sharing information,
    delegating tasks, or keeping others informed. Includes original sender
    information and forward indication in message headers.
    
    Parameters:
        email_id: Unique identifier of the email to forward
        to: Recipient email address for the forwarded message
        additional_message: Optional text to add before forwarded content
    
    Returns:
        Forward confirmation with new message ID
    """
    return {
        "message_id": "fwd_001",
        "status": "forwarded",
        "original_email_id": email_id,
        "forwarded_to": to,
        "sent_at": "2024-01-15T11:05:00Z"
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)