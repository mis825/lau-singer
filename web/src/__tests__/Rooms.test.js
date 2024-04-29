import {
  getByPlaceholderText,
  render,
  screen,
  fireEvent,
} from "@testing-library/react";
import Rooms from "../components/Rooms/Rooms";
import { BrowserRouter } from "react-router-dom";

describe("Rooms", () => {
  test("renders Rooms component", () => {
    render(
      <BrowserRouter>
        <Rooms name="test" loggedIn={true} />
      </BrowserRouter>
    );
    const createButton = screen.getByRole("button", { name: /Create/i });
    expect(createButton).toBeInTheDocument();
    const refreshButton = screen.getByRole("button", { name: /Refresh/i });
    expect(refreshButton).toBeInTheDocument();
  });

  test("navigate to login when not logged in", () => {
    render(
      <BrowserRouter>
        <Rooms name="" loggedIn={false} />
      </BrowserRouter>
    );
    const error = screen.getByText(/Please log in to access the rooms/i);
    expect(error).toBeInTheDocument();
  });

  test("navigate to game when create button is clicked", () => {
    render(
      <BrowserRouter>
        <Rooms name="test" loggedIn={true} />
      </BrowserRouter>
    );
    const createButton = screen.getByRole("button", { name: /Create/i });
    fireEvent.click(createButton);
    const error = screen.queryByText(/Please log in to access the rooms/i);
    expect(error).toBeNull();
  });
});
