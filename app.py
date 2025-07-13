import streamlit as st
import pandas as pd
import io
from datetime import datetime
import re
import PyPDF2
from typing import List, Dict, Any
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Financial Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for chat-like interface
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px 0;
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 30px;
    }
    
    .greeting {
        text-align: center;
        font-size: 1.8em;
        color: white;
        margin-bottom: 40px;
        padding: 30px;
        background-color: transparent;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 20px;
        background-color: transparent;
        border-radius: 0;
        margin-bottom: 20px;
    }
    
    .input-container {
        display: flex;
        justify-content: center;
        margin: 30px auto;
        max-width: 900px;
        align-items: center;
    }
    
    .input-wrapper {
        width: 100%;
        background-color: transparent;
        border: none;
        border-radius: 0;
        padding: 15px 20px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .file-upload-section {
        display: flex;
        gap: 10px;
        align-items: center;
    }
    
    .file-upload-btn {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 8px 12px;
        cursor: pointer;
        transition: all 0.3s;
        font-size: 14px;
        color: #666;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .file-upload-btn:hover {
        background-color: #e9ecef;
        border-color: #007bff;
        color: #007bff;
    }
    
    .text-input-section {
        flex: 1;
        margin: 0 15px;
    }
    
    .send-btn-section {
        display: flex;
        align-items: center;
        justify-content: center;
        width: auto;
    }
    
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 12px 18px;
        border-radius: 18px;
        margin: 10px 0;
        margin-left: 20%;
        text-align: right;
    }
    
    .assistant-message {
        background-color: #e9ecef;
        color: #333;
        padding: 12px 18px;
        border-radius: 18px;
        margin: 10px 0;
        margin-right: 20%;
    }
    
    /* Attempting more specific targeting for the send button */
    /* This targets the button element directly within a div that contains our 'send_button' key */
    /* Streamlit often wraps buttons, so we target the button inside the parent div */
    div.stButton > button {
        background-color: #f0f0f0 !important; /* Lighter grayish for better distinction */
        color: #333 !important;
        border: 1px solid #ccc !important; /* Slightly darker border */
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        transition: all 0.3s !important;
        min-width: 120px !important;
        height: 50px !important;
        font-size: 18px !important;
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    div.stButton > button:hover {
        background-color: #e0e0e0 !important;
        border-color: #aaa !important;
        color: #333 !important;
        transform: translateY(-1px) !important;
    }
    
    div.stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Target specific button if data-testid helps */
    [data-testid="stFormSubmitButton"] button {
        background-color: #f0f0f0 !important; /* Ensure this also gets the style */
        color: #333 !important;
        border: 1px solid #ccc !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        min-width: 120px !important;
        height: 50px !important;
        font-size: 18px !important;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #e0e0e0 !important;
        border-color: #aaa !important;
    }
    
    .stTextInput > div > div > input {
        border: 2px solid #ddd;
        outline: none;
        padding: 12px 15px;
        font-size: 16px;
        background: white;
        width: 100%;
        color: #333;
        border-radius: 25px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #007bff;
        box-shadow: 0 2px 12px rgba(0,123,255,0.2);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #999;
    }
    
    .stTextInput > div > div {
        border: none;
        background: transparent;
        border-radius: 0;
    }
    
    .stTextInput > div {
        border: none;
        background: transparent;
        border-radius: 0;
    }
    
    .stTextInput {
        margin: 0;
        padding: 0;
    }
    
    .invoice-table {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stFileUploader > div {
        border: none;
        background: transparent;
        padding: 0;
        margin: 0;
        min-height: auto;
    }
    
    .stFileUploader > div > div {
        border: none;
        background: transparent;
        padding: 0;
        margin: 0;
        min-height: auto;
    }
    
    .stFileUploader label {
        display: none;
    }
    
    .stFileUploader button {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 8px 12px;
        font-size: 14px;
        color: #666;
        transition: all 0.3s;
    }
    
    .stFileUploader button:hover {
        background-color: #e9ecef;
        border-color: #007bff;
        color: #007bff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'parsed_invoices' not in st.session_state:
    st.session_state.parsed_invoices = []

def parse_csv_invoice(file) -> Dict[str, Any]:
    """Parse CSV invoice file"""
    try:
        df = pd.read_csv(file)
        return {
            'filename': file.name,
            'type': 'CSV',
            'data': df,
            'summary': {
                'total_rows': len(df),
                'columns': list(df.columns),
                'total_amount': df.select_dtypes(include=['float64', 'int64']).sum().sum() if not df.select_dtypes(include=['float64', 'int64']).empty else 0
            }
        }
    except Exception as e:
        return {'error': f"Error parsing CSV: {str(e)}"}

def parse_pdf_invoice(file) -> Dict[str, Any]:
    """Parse PDF invoice file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Extract basic invoice information using regex
        invoice_data = {
            'filename': file.name,
            'type': 'PDF',
            'text': text,
            'extracted_info': extract_invoice_info(text)
        }
        return invoice_data
    except Exception as e:
        return {'error': f"Error parsing PDF: {str(e)}"}

def extract_invoice_info(text: str) -> Dict[str, Any]:
    """Extract invoice information from text"""
    info = {}
    
    # Extract invoice number
    invoice_match = re.search(r'invoice\s*#?\s*:?\s*(\w+)', text, re.IGNORECASE)
    if invoice_match:
        info['invoice_number'] = invoice_match.group(1)
    
    # Extract date
    date_match = re.search(r'date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE)
    if date_match:
        info['date'] = date_match.group(1)
    
    # Extract total amount
    total_match = re.search(r'total\s*:?\s*\$?(\d+[.,]\d{2})', text, re.IGNORECASE)
    if total_match:
        info['total_amount'] = total_match.group(1)
    
    return info

def process_financial_query(query: str) -> str:
    """Process financial queries"""
    query_lower = query.lower()
    
    if 'audit' in query_lower:
        return "🔍 *Audit Analysis*: I can help you with audit preparations, compliance checks, and financial statement reviews. Please upload your financial documents for detailed analysis."
    
    elif 'budget' in query_lower:
        return "📊 *Budget Analysis*: I can analyze your budget allocation, track expenses, and provide cost optimization suggestions. Share your budget files for comprehensive review."
    
    elif 'tax' in query_lower:
        return "💰 *Tax Assistance*: I can help with tax calculations, deduction identification, and compliance verification. Upload your tax documents for detailed analysis."
    
    elif 'invoice' in query_lower:
        return "📄 *Invoice Processing*: I can process and analyze invoices, extract key information, and identify discrepancies. Upload your invoice files to get started."
    
    elif 'expense' in query_lower:
        return "💳 *Expense Tracking*: I can categorize expenses, identify patterns, and provide spending insights. Upload your expense reports for analysis."
    
    else:
        return "🤖 *Financial Assistant*: I can help with various financial tasks including audit preparation, budget analysis, tax assistance, invoice processing, and expense tracking. Please specify your query or upload relevant documents."

# Main UI
st.markdown('<div class="main-header">💰 Financial Assistant</div>', unsafe_allow_html=True)

# Chat messages container
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Show greeting only if no messages yet
    if not st.session_state.messages:
        st.markdown('''
        <div class="greeting">
            🚀 Hello! Which financial query should I solve today or which audit should I fix?
        </div>
        ''', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Chat input container - single line with file buttons, input, and send button
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)

# File upload buttons
st.markdown('<div class="file-upload-section">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    csv_uploaded = st.file_uploader(
        "📊 CSV",
        type=['csv'],
        key="csv_uploader",
        help="Upload CSV files (max 500MB)", # Updated help text
        label_visibility="collapsed"
    )
with col2:
    pdf_uploaded = st.file_uploader(
        "📄 PDF", 
        type=['pdf'],
        key="pdf_uploader",
        help="Upload PDF files (max 500MB)", # Updated help text
        label_visibility="collapsed"
    )
st.markdown('</div>', unsafe_allow_html=True)

# Text input section
st.markdown('<div class="text-input-section">', unsafe_allow_html=True)
user_input = st.text_input(
    "Message",
    placeholder="Ask about audits, budgets, taxes, invoices, or expenses...",
    key="user_input",
    label_visibility="hidden"
)
st.markdown('</div>', unsafe_allow_html=True)

# Send button section
st.markdown('<div class="send-btn-section">', unsafe_allow_html=True)
send_button = st.button("Send", key="send_button", help="Send message")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close input-wrapper
st.markdown('</div>', unsafe_allow_html=True)  # Close input-container

# Process uploaded files
uploaded_files = []
if csv_uploaded:
    # Check file size (500MB limit)
    if csv_uploaded.size > 500 * 1024 * 1024:  # 500MB in bytes
        st.error("❌ File size exceeds 500MB limit!")
    else:
        uploaded_files.append(csv_uploaded)
        
if pdf_uploaded:
    # Check file size (500MB limit)
    if pdf_uploaded.size > 500 * 1024 * 1024:  # 500MB in bytes
        st.error("❌ File size exceeds 500MB limit!")
    else:
        uploaded_files.append(pdf_uploaded)

if uploaded_files:
    for file in uploaded_files:
        if file not in st.session_state.uploaded_files:
            st.session_state.uploaded_files.append(file)
            
            # Process the file
            if file.type == 'text/csv':
                parsed_data = parse_csv_invoice(file)
            elif file.type == 'application/pdf':
                parsed_data = parse_pdf_invoice(file)
            
            if 'error' not in parsed_data:
                st.session_state.parsed_invoices.append(parsed_data)
                st.success(f"✅ *{file.name}* uploaded and processed successfully!")
            else:
                st.error(f"❌ {parsed_data['error']}")

# Display processed files (if any)
if st.session_state.parsed_invoices:
    st.markdown("### 📋 Processed Files")
    
    for i, invoice in enumerate(st.session_state.parsed_invoices):
        with st.expander(f"📄 *{invoice['filename']}* ({invoice['type']})", expanded=False):
            if invoice['type'] == 'CSV':
                st.markdown("*Data Preview:*")
                st.dataframe(invoice['data'].head(), use_container_width=True)
                
                st.markdown("*Summary:*")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rows", invoice['summary']['total_rows'])
                with col2:
                    st.metric("Columns", len(invoice['summary']['columns']))
                with col3:
                    st.metric("Total Amount", f"${invoice['summary']['total_amount']:.2f}")
                
            elif invoice['type'] == 'PDF':
                st.markdown("*Extracted Information:*")
                info = invoice['extracted_info']
                if info:
                    for key, value in info.items():
                        st.write(f"{key.replace('_', ' ').title()}:** {value}")
                else:
                    st.write("No specific invoice information could be extracted.")
                
                with st.expander("View Full Text", expanded=False):
                    st.text_area("PDF Content", invoice['text'], height=200)

# Handle message sending
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate response
    response = process_financial_query(user_input)
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update the display
    st.rerun()

# Clear chat button
if st.session_state.messages:
    st.markdown('<div style="text-align: center; margin: 20px 0;">', unsafe_allow_html=True)
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        💰 Financial Assistant - Upload files and ask questions about your financial data
    </div>
    """,
    unsafe_allow_html=True
)