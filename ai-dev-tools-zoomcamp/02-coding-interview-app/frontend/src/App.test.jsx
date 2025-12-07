import { render, screen } from '@testing-library/react';
import App from './App';
import { describe, it, expect } from 'vitest';

describe('App', () => {
    it('renders without crashing', () => {
        render(<App />);
        // Since App redirects or shows Home, let's check for something common
        // Actually, App renders Router. Home renders "Coding Interview App"
        expect(screen.getByText(/Coding Interview App/i)).toBeInTheDocument();
    });
});
