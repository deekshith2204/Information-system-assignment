import React from "react";
import { renderToString } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import App from "./App";

describe("App", () => {
  test("renders the main navigation and search page content", () => {
    const html = renderToString(
      <MemoryRouter initialEntries={["/search"]}>
        <App />
      </MemoryRouter>
    );

    expect(html).toContain("Babla Cars");
    expect(html).toContain("Search Trips");
    expect(html).toContain("Find rides");
  });
});
