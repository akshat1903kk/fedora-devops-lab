import { render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import App from './App';

describe('App', () => {
  beforeEach(() => {
    global.fetch = vi.fn().mockResolvedValue({
      json: vi.fn().mockResolvedValue({ status: 'ok' }),
    });
  });

  it('renders the App component', () => {
    render(<App />);
    expect(screen.getByText('Fedora DevOps Lab Frontend')).toBeInTheDocument();
  });

  it('displays "Checking..." as the initial API status', () => {
    render(<App />);
    expect(screen.getByText('API Status:')).toBeInTheDocument();
    expect(screen.getByText('Checking...')).toBeInTheDocument();
  });

  it('fetches API status and displays it', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText('{"status":"ok"}')).toBeInTheDocument();
    });
  });
});
