import {getByPlaceholderText, render, screen, fireEvent} from '@testing-library/react';
import Login from '../components/Login/Login';
import {BrowserRouter} from 'react-router-dom';

describe('Login', () => {
    test('renders Login component', () => {
        render(
            <BrowserRouter>
                <Login />
            </BrowserRouter>
        );
        const linkElement = screen.getByPlaceholderText(/Enter your name/i);
        expect(linkElement).toBeInTheDocument();
    });

    test('throws error when name is empty', () => {
        render(
            <BrowserRouter>
                <Login />
            </BrowserRouter>
        );
        const buttonElement = screen.getByRole('button', {name: /Enter/i});
        fireEvent.click(buttonElement);
        const error = screen.getByText(/Please enter a name/i);
        expect(error).toBeInTheDocument();
    });

    test('logs in when name is not empty', () => {
        render(
            <BrowserRouter>
                <Login />
            </BrowserRouter>
        );
        const inputElement = screen.getByPlaceholderText(/Enter your name/i);
        fireEvent.change(inputElement, {target: {value: 'test'}});
        const buttonElement = screen.getByRole('button', {name: /Enter/i});
        fireEvent.click(buttonElement);
        const error = screen.queryByText(/Please enter a name/i);
        expect(error).toBeNull();
    });
});

