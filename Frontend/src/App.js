import React, { useState, useRef } from 'react';

const FinancialAuditUI = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [csvFile, setCsvFile] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const csvInputRef = useRef(null);
  const pdfInputRef = useRef(null);

  const handleFileUpload = (event, type) => {
    const file = event.target.files[0];
    if (!file) return;

    const maxSize = 500 * 1024 * 1024; // 500MB in bytes
    const fileName = file.name;

    if (file.size > maxSize) {
      alert('File too large (max 500MB)');
      return;
    }

    if (type === 'csv') {
      setCsvFile({ name: fileName, status: 'success' });
    } else {
      setPdfFile({ name: fileName, status: 'success' });
    }

    addMessage(`📁 Uploaded: ${fileName}`, 'user');
    addMessage('🔄 Processing document... Analysis will appear in the results panel.', 'system');
  };

  const addMessage = (text, sender) => {
    setMessages(prev => [...prev, { text, sender, id: Date.now() }]);
  };

  const clearChat = () => {
    setMessages([]);
  };

  const sendMessage = () => {
    if (inputValue.trim()) {
      addMessage(inputValue, 'user');
      setInputValue('');

      // Simulate AI response
      setTimeout(() => {
        const responses = [
          '🤖 Analyzing your request... Processing through our advanced audit engine.',
          '📊 Running comprehensive audit checks across financial parameters...',
          '⚡ Processing through multiple AI models for detailed analysis.',
          '🔍 Scanning for anomalies, compliance issues, and generating insights...'
        ];
        
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];
        addMessage(randomResponse, 'ai');
      }, 1000);
    }
  };

  const suggestedPrompt = (prompt) => {
    setInputValue(prompt);
    setTimeout(() => sendMessage(), 100);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 overflow-hidden">
      {/* Left Side - Chat Interface */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto p-6 bg-slate-900/50">
          {messages.length === 0 ? (
            <div className="text-center py-16 text-slate-300">
              <div className="text-5xl mb-6 text-slate-400">💬</div>
              <div className="text-xl font-semibold mb-3 text-slate-200">Welcome to Financial Audit AI</div>
              <div className="text-slate-400 leading-relaxed max-w-sm mx-auto">
                Upload your financial documents and start conversing to receive comprehensive audit insights and recommendations.
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`p-4 rounded-lg max-w-4/5 break-words ${
                    message.sender === 'user'
                      ? 'bg-slate-700 text-slate-100 ml-auto border border-slate-600'
                      : message.sender === 'ai'
                      ? 'bg-slate-800 text-slate-200 border border-slate-700'
                      : 'bg-slate-800/50 text-slate-300 border-l-4 border-slate-600'
                  }`}
                >
                  {message.text}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Chat Input */}
        <div className="p-6 bg-slate-800/30 border-t border-slate-700/30">
          {/* File Upload Status */}
          {(csvFile || pdfFile) && (
            <div className="mb-4 space-y-2">
              {csvFile && (
                <div className="flex items-center justify-between bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-3">
                  <div className="flex items-center space-x-3">
                    <span className="w-8 h-8 bg-emerald-500/20 rounded-lg flex items-center justify-center text-emerald-400">📊</span>
                    <div>
                      <p className="text-emerald-400 font-medium text-sm">{csvFile.name}</p>
                      <p className="text-emerald-300 text-xs">CSV file uploaded</p>
                    </div>
                  </div>
                  <button
                    onClick={() => setCsvFile(null)}
                    className="w-6 h-6 text-emerald-400 hover:text-red-400 rounded-full hover:bg-red-500/20 flex items-center justify-center transition-all duration-200"
                    title="Remove file"
                  >
                    ✕
                  </button>
                </div>
              )}
              
              {pdfFile && (
                <div className="flex items-center justify-between bg-red-500/10 border border-red-500/30 rounded-lg p-3">
                  <div className="flex items-center space-x-3">
                    <span className="w-8 h-8 bg-red-500/20 rounded-lg flex items-center justify-center text-red-400">📄</span>
                    <div>
                      <p className="text-red-400 font-medium text-sm">{pdfFile.name}</p>
                      <p className="text-red-300 text-xs">PDF file uploaded</p>
                    </div>
                  </div>
                  <button
                    onClick={() => setPdfFile(null)}
                    className="w-6 h-6 text-red-400 hover:text-red-300 rounded-full hover:bg-red-500/20 flex items-center justify-center transition-all duration-200"
                    title="Remove file"
                  >
                    ✕
                  </button>
                </div>
              )}
            </div>
          )}
          
          {/* Clear Chat Button */}
          {messages.length > 0 && (
            <div className="mb-4 flex justify-center">
              <button
                onClick={clearChat}
                className="px-4 py-2 bg-slate-700/50 hover:bg-red-600/50 text-slate-300 hover:text-white text-sm rounded-lg transition-all duration-200 hover:shadow-md border border-slate-600/30 hover:border-red-500/50 flex items-center space-x-2 group"
              >
                <span className="group-hover:rotate-12 transition-transform">🗑️</span>
                <span>Clear Chat</span>
              </button>
            </div>
          )}
          
          <div className="flex items-center bg-slate-700/50 rounded-lg p-3 border border-slate-600/50 focus-within:border-slate-500 focus-within:bg-slate-700/70 transition-all duration-300">
            {/* File Upload Buttons */}
            <div className="flex items-center space-x-2 mr-3">
              <input
                type="file"
                accept=".csv"
                onChange={(e) => handleFileUpload(e, 'csv')}
                ref={csvInputRef}
                className="hidden"
              />
              <button
                onClick={() => csvInputRef.current?.click()}
                className="w-9 h-9 bg-slate-600/70 hover:bg-emerald-600/70 text-slate-300 hover:text-white rounded-lg flex items-center justify-center transition-all duration-200 hover:scale-105 group"
                title="Upload CSV file"
              >
                <span className="text-sm group-hover:scale-110 transition-transform">📊</span>
              </button>
              
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => handleFileUpload(e, 'pdf')}
                ref={pdfInputRef}
                className="hidden"
              />
              <button
                onClick={() => pdfInputRef.current?.click()}
                className="w-9 h-9 bg-slate-600/70 hover:bg-red-600/70 text-slate-300 hover:text-white rounded-lg flex items-center justify-center transition-all duration-200 hover:scale-105 group"
                title="Upload PDF file"
              >
                <span className="text-sm group-hover:scale-110 transition-transform">📄</span>
              </button>
            </div>
            
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1 bg-transparent outline-none text-slate-200 placeholder-slate-400"
              placeholder="Ask about financial audits, compliance, or document analysis..."
            />
            <button
              onClick={sendMessage}
              className="ml-3 w-10 h-10 bg-slate-600 hover:bg-slate-500 text-slate-200 rounded-lg flex items-center justify-center transition-all duration-200 hover:scale-105"
            >
              ➤
            </button>
          </div>
        </div>
      </div>

      {/* Right Side - Professional Dashboard */}
      <div className="w-1/2 bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 flex flex-col">
        
        {/* Dashboard Header */}
        <div className="bg-gradient-to-r from-slate-800 to-slate-700 text-white p-6 border-b border-slate-600/30 shadow-xl">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-slate-100">📋 Audit Dashboard</h2>
              <p className="text-slate-300 text-sm mt-1">Real-time analysis and insights</p>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
              <span className="text-xs text-slate-300">Live</span>
            </div>
          </div>
        </div>

        {/* Dashboard Content */}
        <div className="flex-1 p-8 bg-gradient-to-br from-slate-900/50 to-slate-800/50 overflow-y-auto">
          {/* Stats Cards */}
          <div className="grid grid-cols-2 gap-4 mb-8">
            <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700/50 shadow-lg backdrop-blur-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-400 text-xs font-medium uppercase tracking-wider">Documents</p>
                  <p className="text-2xl font-bold text-slate-100 mt-1">{(csvFile ? 1 : 0) + (pdfFile ? 1 : 0)}</p>
                </div>
                <div className="w-10 h-10 bg-slate-700/50 rounded-lg flex items-center justify-center text-slate-300">
                  📁
                </div>
              </div>
            </div>
            
            <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700/50 shadow-lg backdrop-blur-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-400 text-xs font-medium uppercase tracking-wider">Queries</p>
                  <p className="text-2xl font-bold text-slate-100 mt-1">{messages.filter(m => m.sender === 'user').length}</p>
                </div>
                <div className="w-10 h-10 bg-slate-700/50 rounded-lg flex items-center justify-center text-slate-300">
                  💬
                </div>
              </div>
            </div>
          </div>

          {/* Analysis Status */}
          <div className="bg-slate-800/60 rounded-xl border border-slate-700/50 shadow-lg backdrop-blur-sm p-6 mb-6">
            <h3 className="font-semibold text-slate-100 mb-4 flex items-center">
              <span className="w-6 h-6 bg-slate-700/50 rounded-full flex items-center justify-center mr-3 text-sm text-slate-300">⚡</span>
              Analysis Status
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg border border-slate-600/30">
                <span className="text-slate-200 text-sm">Document Processing</span>
                <span className="text-xs px-2 py-1 bg-emerald-500/20 text-emerald-400 rounded-full border border-emerald-500/30">Ready</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg border border-slate-600/30">
                <span className="text-slate-200 text-sm">AI Analysis Engine</span>
                <span className="text-xs px-2 py-1 bg-emerald-500/20 text-emerald-400 rounded-full border border-emerald-500/30">Active</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg border border-slate-600/30">
                <span className="text-slate-200 text-sm">Compliance Checker</span>
                <span className="text-xs px-2 py-1 bg-slate-600/50 text-slate-300 rounded-full border border-slate-500/30">Standby</span>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-slate-800/60 rounded-xl border border-slate-700/50 shadow-lg backdrop-blur-sm p-6">
            <h3 className="font-semibold text-slate-100 mb-4 flex items-center">
              <span className="w-6 h-6 bg-slate-700/50 rounded-full flex items-center justify-center mr-3 text-sm text-slate-300">🎯</span>
              Quick Actions
            </h3>
            <div className="space-y-3">
              {[
                { icon: '🔍', text: 'Analyze invoice discrepancies', prompt: 'Analyze invoice discrepancies' },
                { icon: '⚠️', text: 'Check for duplicate transactions', prompt: 'Check for duplicate transactions' },
                { icon: '✅', text: 'Validate expense compliance', prompt: 'Validate expense compliance' },
                { icon: '📊', text: 'Generate comprehensive audit report', prompt: 'Generate audit summary' }
              ].map((item, index) => (
                <button
                  key={index}
                  onClick={() => suggestedPrompt(item.prompt)}
                  className="w-full text-left p-3 bg-slate-700/30 hover:bg-slate-700/50 rounded-lg transition-all duration-200 hover:shadow-md border border-slate-600/30 hover:border-slate-500/50 group"
                >
                  <div className="flex items-center">
                    <span className="w-8 h-8 bg-slate-600/50 rounded-lg flex items-center justify-center mr-3 text-sm group-hover:scale-110 transition-transform text-slate-300">
                      {item.icon}
                    </span>
                    <span className="text-slate-200 text-sm font-medium">{item.text}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Footer Info */}
          <div className="mt-8 text-center">
            <p className="text-xs text-slate-400">
              Powered by advanced AI • Secure & Compliant • Real-time Processing
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FinancialAuditUI;