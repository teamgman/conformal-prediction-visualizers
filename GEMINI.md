# Antigravity Agent Rules: Technical Document Generation

Whenever tasked with creating or refactoring frontend interfaces, web views, or dashboard visualizers (such as `build_html.py` or any HTML output), you must strictly bypass generic templates and enforce the following rules:

## 1. Visual Theme (Sage Green Academic)

- **Canvas Background:** #f2f4f2 (Desaturated, pale sage-ash to prevent monitor glare).
- **Graph Panels:** #ffffff (Pure white backgrounds reserved exclusively to anchor data plots).
- **Typography & Ink:** #1c231c (High-contrast charcoal for all headers, formulas, body text, and line indicators).

## 2. Edward Tufte Data-Ink Architecture

- **Eliminate Chartjunk:** Delete all nested layout boxes, border frames, card panels, glassmorphism, drop shadows, and glowing border trails.
- **Structural Spacing:** Use simple horizontal rules (`<hr>`) and clean white margins to create layout hierarchy instead of drawing geometric border cells.
- **Typography:** Enforce a single font family (`Georgia`, serif) globally across titles, axes, and text blocks. Monospace (`Courier New`) is restricted strictly to raw data matrices.

## 3. Automation & Verification Loops

- **Plotly Configuration:** You must configure all interactive plots using the `plotly_white` template. Explicitly remove all gridlines, background shading, and external legend boxes. Use direct labeling on data lines where possible.
- **Verification Rule:** Whenever updating a visualizer file, you are required to implicitly run the `/browser` command. You must load the page, verify that CDN components (Plotly, MathJax) execute without console errors, and ensure the UI respects this minimalist styling before pushing code changes to the workspace.
