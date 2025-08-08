import { render, screen } from '@testing-library/react';
import App from './App';

test('renders chatbot app title', () => {
  render(<App />);
  const titleElement = screen.getByText(/My AI Assistant/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders chatbot component', () => {
  render(<App />);
  const chatbotElement = screen.getByText(/GPT Chatbot/i);
  expect(chatbotElement).toBeInTheDocument();
});

test('renders message input field', () => {
  render(<App />);
  const inputElement = screen.getByPlaceholderText(/Type your message and press Enter/i);
  expect(inputElement).toBeInTheDocument();
});

test('renders send button', () => {
  render(<App />);
  const sendButton = screen.getByRole('button', { name: /send/i });
  expect(sendButton).toBeInTheDocument();
});
