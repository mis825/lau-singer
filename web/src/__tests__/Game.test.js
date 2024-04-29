import {
  getByPlaceholderText,
  render,
  screen,
  fireEvent,
} from "@testing-library/react";
import TestGame from "../components/TestGame/TestGame";
import { CanvasProvider } from "../providers/CanvasProvider";
import { BrowserRouter } from "react-router-dom";

describe("Game", () => {
  test("renders Game component", () => {
    render(
      <BrowserRouter>
          <TestGame name="test" loggedIn={true} room={217298} />
      </BrowserRouter>
    );
    const chatButton = screen.getByRole("button", { name: /Chat/i });
    expect(chatButton).toBeInTheDocument();
    const canvas = screen.getByTestId("canvas");
    expect(canvas).toBeInTheDocument();
    const startButton = screen.getByRole("button", { name: /Start/i });
    expect(startButton).toBeInTheDocument();
    const deleteButton = screen.getByRole("button", { name: /Delete/i });
    expect(deleteButton).toBeInTheDocument();
  });
});
