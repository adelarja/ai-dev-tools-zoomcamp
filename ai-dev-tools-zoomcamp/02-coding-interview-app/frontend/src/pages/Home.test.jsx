import { render, screen, fireEvent } from '@testing-library/react';
import Home from './Home';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect, vi } from 'vitest';

describe('Home', () => {
    it('renders create button', () => {
        render(
            <BrowserRouter>
                <Home />
            </BrowserRouter>
        );
        expect(screen.getByText(/Create New Interview/i)).toBeInTheDocument();
    });
});
