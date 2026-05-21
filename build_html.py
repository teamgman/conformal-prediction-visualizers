import json

with open("conformal_data.json", "r") as f:
    data_json = f.read()

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Full Conformal Prediction Visualizer</title>
    
    <!-- Plotly -->
    <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
    
    <!-- MathJax -->
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']]
            },
            options: {
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

    <style>
        :root {
            --bg-deep: #f2f4f2;
            --bg-card: #ffffff;
            --bg-raised: #ffffff;
            --text-main: #1c231c;
            --text-muted: #555555;
            
            --accent-main: #1c231c;
            --accent-red: #d62728;
            --accent-amber: #ff7f0e;
            --accent-green: #2ca02c;
            
            --border-color: #1c231c;
            
            --font-sans: 'Georgia', 'Times New Roman', serif;
            --font-mono: 'Courier New', Courier, monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-deep);
            color: var(--text-main);
            font-family: var(--font-sans);
            padding: 2rem;
            display: flex;
            justify-content: center;
            line-height: 1.6;
        }

        .container {
            width: 100%;
            max-width: 1100px;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        h1 {
            font-size: 1.75rem;
            font-weight: normal;
            color: var(--text-main);
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 0.25rem;
        }

        .card {
            background: transparent;
            border: none;
            padding: 1.5rem 0;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        hr.tufte-rule {
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 1rem 0;
        }

        /* Dashboard Grid */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
        }
        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        .stat-card {
            background: transparent;
            border: none;
            border-left: 2px solid var(--border-color);
            padding: 0.5rem 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .stat-label {
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
        }

        .stat-val {
            font-family: var(--font-mono);
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--accent-main);
        }

        /* Plotly Container */
        #plot-container {
            width: 100%;
            height: 500px;
            background: var(--bg-card);
        }

        /* Controls */
        .controls-row {
            display: flex;
            align-items: center;
            gap: 2rem;
            padding: 0.5rem 0;
            flex-wrap: wrap;
        }

        .slider-group {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            min-width: 300px;
        }

        .slider-header {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: var(--text-muted);
        }

        .slider-val-display {
            font-family: var(--font-mono);
            color: var(--accent-main);
            font-weight: bold;
        }

        input[type="range"] {
            -webkit-appearance: none;
            width: 100%;
            height: 6px;
            background: #e5e7eb;
            border: 1px solid var(--border-color);
            outline: none;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #112233;
            cursor: pointer;
        }

        .btn {
            background: #ffffff;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 0.6rem 1.2rem;
            font-family: var(--font-sans);
            font-size: 0.85rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn:hover {
            /* No hover per constraints */
        }
        
        .btn.active {
            font-weight: bold;
            border: 2px solid var(--border-color);
        }

        /* Status Badge */
        .status-badge-container {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .p-val-display {
            font-family: var(--font-mono);
            font-size: 1.1rem;
            font-weight: bold;
        }

        .badge {
            padding: 0.4rem 0.8rem;
            font-weight: bold;
            font-size: 0.85rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .badge-accepted {
            background: #ffffff;
            color: var(--accent-green);
            border: 2px solid var(--accent-green);
        }

        .badge-rejected {
            background: #ffffff;
            color: var(--accent-red);
            border: 2px solid var(--accent-red);
        }

        /* Math Section */
        .math-box {
            background: transparent;
            border: none;
            border-top: 1px solid var(--border-color);
            padding: 1.5rem 0;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        .math-box p {
            margin-bottom: 1rem;
        }
        .math-box p:last-child {
            margin-bottom: 0;
        }
        
        h2 {
            font-size: 1.25rem;
            font-weight: bold;
            color: var(--text-main);
        }

    </style>
</head>
<body>

    <div class="container">
        <nav style="margin-bottom: 1rem; font-size: 0.85rem; font-family: var(--font-mono); display: flex; gap: 1rem;">
            <a href="index.html" style="color: var(--text-muted); text-decoration: none;">← Back to Index</a>
            <span style="color: var(--text-muted);">|</span>
            <a href="https://gavinxiong.com" style="color: var(--text-muted); text-decoration: none;">gavinxiong.com</a>
        </nav>
        <header>
            <h1>Full Conformal Prediction Visualizer</h1>
            <p class="subtitle">Interactive demonstration of evaluating a single test point $Y_{n+1}$ across the domain.</p>
        </header>

        <hr class="tufte-rule" />

        <!-- Dashboard -->
        <div class="dashboard-grid">
            <div class="stat-card">
                <span class="stat-label">Training Size ($n$)</span>
                <span class="stat-val" id="stat-n">-</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">Test Input ($x_{n+1}$)</span>
                <span class="stat-val" id="stat-xtest">-</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">Significance ($\alpha$)</span>
                <span class="stat-val" id="stat-alpha">0.10</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">Prediction Interval</span>
                <span class="stat-val" id="stat-interval" style="font-size: 1.2rem;">-</span>
            </div>
        </div>

        <hr class="tufte-rule" />

        <!-- Plot Area -->
        <div class="card">
            <div id="plot-container"></div>
            
            <!-- Controls -->
            <div class="controls-row">
                <div class="slider-group">
                    <div class="slider-header">
                        <span>Trial y-value ($y_{trial}$)</span>
                        <span class="slider-val-display" id="y-val-display">0.00</span>
                    </div>
                    <input type="range" id="y-slider" min="0" max="199" step="1" value="100">
                </div>
                
                <div class="slider-group">
                    <div class="slider-header">
                        <span>Error value ($\alpha$)</span>
                        <span class="slider-val-display" id="alpha-val-display">0.10</span>
                    </div>
                    <input type="range" id="alpha-slider" min="0.01" max="0.50" step="0.01" value="0.10">
                </div>
                
                <button class="btn" id="autoplay-btn">▶ Autoplay</button>
                
                <div class="status-badge-container">
                    <div class="p-val-display" id="p-val-display">p = 0.000</div>
                    <div class="badge badge-accepted" id="status-badge">ACCEPTED</div>
                </div>
            </div>
        </div>

        <hr class="tufte-rule" />

        <!-- Mathematical Details -->
        <div class="card" style="border: none; padding: 0;">
            <h2>Mathematical Foundation</h2>
            <div class="math-box">
                <p>Unlike Split Conformal Prediction, <strong>Full Conformal Prediction</strong> (also known as Transductive Conformal Prediction) does not require data splitting. It achieves valid coverage by refitting the entire model for <em>every possible trial value</em> $y \in \mathbb{R}$ at the test point $X_{n+1}$.</p>
                <p>For a given trial value $y$, we construct an augmented dataset of size $n+1$:
                $$ \mathcal{D}^{y} = \{(X_1, Y_1), \dots, (X_n, Y_n), (X_{n+1}, y)\} $$</p>
                <p>We train the model (here, Kernel Ridge Regression) on $\mathcal{D}^{y}$ and compute the absolute residuals for all $n+1$ points:
                $$ R_i^y = |Y_i - \hat{f}^y(X_i)|, \quad \text{for } i = 1, \dots, n+1 $$</p>
                <p>Because the augmented dataset is exchangeable, the test residual $R_{n+1}^y$ is equally likely to rank anywhere among the $n+1$ residuals. The empirical p-value is the proportion of residuals at least as large as the test residual:
                $$ p(y) = \frac{1}{n+1} \sum_{i=1}^{n+1} \mathbb{I}\left(R_i^y \ge R_{n+1}^y\right) $$</p>
                <p>The prediction interval $C(X_{n+1})$ includes all $y$ where $p(y) > \alpha$. The plot above visualizes this process dynamically for a grid of trial values.</p>
            </div>
        </div>
    </div>

    <script>
        // Pre-computed data
        const data = __DATA_PLACEHOLDER__;
        
        let alpha = 0.10;
        const n_trials = data.y_trial_values.length;
        
        let y_min = null;
        let y_max = null;

        // Find the prediction interval (range of y where p > alpha)
        function computeInterval() {
            y_min = null;
            y_max = null;
            for (let i = 0; i < n_trials; i++) {
                if (data.p_values[i] > alpha) {
                    if (y_min === null) y_min = data.y_trial_values[i];
                    y_max = data.y_trial_values[i];
                }
            }
            document.getElementById('stat-interval').innerText = y_min !== null 
                ? `[${y_min.toFixed(2)}, ${y_max.toFixed(2)}]` 
                : "Empty";
            document.getElementById('stat-alpha').innerText = alpha.toFixed(2);
        }
        
        // Initial setup of interval
        computeInterval();
        
        // DOM Elements
        document.getElementById('stat-n').innerText = data.metadata.n_points;
        document.getElementById('stat-xtest').innerText = data.x_test.toFixed(2);

        const slider = document.getElementById('y-slider');
        const alphaSlider = document.getElementById('alpha-slider');
        const yValDisplay = document.getElementById('y-val-display');
        const alphaValDisplay = document.getElementById('alpha-val-display');
        const pValDisplay = document.getElementById('p-val-display');
        const statusBadge = document.getElementById('status-badge');
        const autoplayBtn = document.getElementById('autoplay-btn');

        // Initial Plotly Setup
        function initPlotly() {
            const init_idx = parseInt(slider.value);
            const init_y = data.y_trial_values[init_idx];
            const init_p = data.p_values[init_idx];
            
            // --- Left Plot (Data & Fit) ---
            const trace_scatter = {
                x: data.x_train,
                y: data.y_train,
                mode: 'markers',
                marker: { color: '#1f77b4', size: 6, opacity: 0.8 },
                name: 'Training Data',
                xaxis: 'x1',
                yaxis: 'y1',
                showlegend: false
            };
            
            const trace_curve = {
                x: data.x_grid,
                y: data.fitted_curves[init_idx],
                mode: 'lines',
                line: { color: '#1f77b4', width: 2 },
                name: 'Fitted Curve',
                xaxis: 'x1',
                yaxis: 'y1',
                showlegend: false
            };
            
            const trace_pseudo = {
                x: [data.x_test],
                y: [init_y],
                mode: 'markers',
                marker: { 
                    color: init_p > alpha ? '#2ca02c' : '#d62728', 
                    size: 10, 
                    line: { color: '#ffffff', width: 1 }
                },
                name: 'Trial Point',
                xaxis: 'x1',
                yaxis: 'y1',
                showlegend: false
            };

            // --- Right Plot (P-value Distribution) ---
            const trace_pvalue = {
                x: data.p_values,
                y: data.y_trial_values,
                mode: 'lines',
                line: { color: '#d62728', width: 0 },
                fill: 'tozerox',
                fillcolor: 'rgba(214, 39, 40, 0.4)', // Red fill like the diagram
                name: 'p-value',
                xaxis: 'x2',
                yaxis: 'y2',
                showlegend: false
            };
            
            const trace_tracker = {
                x: [init_p],
                y: [init_y],
                mode: 'markers',
                marker: { 
                    color: init_p > alpha ? '#2ca02c' : '#d62728', 
                    size: 8,
                    symbol: 'diamond'
                },
                xaxis: 'x2',
                yaxis: 'y2',
                showlegend: false
            };
            
            const trace_tracker_line = {
                x: [0, init_p],
                y: [init_y, init_y],
                mode: 'lines',
                line: { color: init_p > alpha ? '#2ca02c' : '#d62728', width: 1, dash: 'dot' },
                xaxis: 'x2',
                yaxis: 'y2',
                showlegend: false
            };

            const layout = {
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: { family: 'Georgia, serif', color: '#1c231c' },
                margin: { l: 50, r: 20, t: 30, b: 50 },
                grid: { rows: 1, columns: 2, pattern: 'independent' },
                xaxis: { 
                    domain: [0, 0.65], 
                    title: 'x', 
                    showgrid: false, 
                    zeroline: false,
                    showline: true,
                    linecolor: '#1c231c',
                    ticks: 'outside',
                    tickcolor: '#1c231c'
                },
                yaxis: { 
                    title: 'y', 
                    showgrid: false, 
                    zeroline: false,
                    showline: true,
                    linecolor: '#1c231c',
                    ticks: 'outside',
                    tickcolor: '#1c231c',
                    range: [-2.5, 2.0]
                },
                xaxis2: { 
                    domain: [0.7, 1.0], 
                    title: 'p-value', 
                    showgrid: false, 
                    zeroline: false,
                    showline: true,
                    linecolor: '#1c231c',
                    ticks: 'outside',
                    tickcolor: '#1c231c',
                    range: [0, 1.05], 
                    tickformat: '.2f' 
                },
                yaxis2: { 
                    showgrid: false,
                    zeroline: false,
                    showline: false,
                    range: [-2.5, 2.0], 
                    showticklabels: false 
                },
                shapes: getShapes()
            };

            Plotly.newPlot('plot-container', [
                trace_scatter, trace_curve, trace_pseudo,
                trace_pvalue, trace_tracker, trace_tracker_line
            ], layout, {responsive: true, displayModeBar: false});
            
            updateUI(init_idx);
        }

        function getShapes() {
            return [
                // Base vertical line at x_test (blue dashed)
                {
                    type: 'line',
                    x0: data.x_test, x1: data.x_test,
                    y0: -2.5, y1: 2.0,
                    xref: 'x1', yref: 'y1',
                    line: { color: '#1f77b4', width: 1, dash: 'dash' }
                },
                // Green valid interval line on left plot
                ...(y_min !== null ? [{
                    type: 'line',
                    x0: data.x_test, x1: data.x_test,
                    y0: y_min, y1: y_max,
                    xref: 'x1', yref: 'y1',
                    line: { color: '#2ca02c', width: 3 } // Green
                }] : []),
                // Threshold line at p = alpha
                {
                    type: 'line',
                    x0: alpha, x1: alpha,
                    y0: -2.5, y1: 2.0,
                    xref: 'x2', yref: 'y2',
                    line: { color: '#777777', width: 1, dash: 'dash' }
                },
                // Top boundary black line on right plot
                ...(y_max !== null ? [{
                    type: 'line',
                    x0: 0, x1: 1.0,
                    y0: y_max, y1: y_max,
                    xref: 'x2', yref: 'y2',
                    line: { color: '#111111', width: 1.5 } // Black lines
                }] : []),
                // Bottom boundary black line on right plot
                ...(y_min !== null ? [{
                    type: 'line',
                    x0: 0, x1: 1.0,
                    y0: y_min, y1: y_min,
                    xref: 'x2', yref: 'y2',
                    line: { color: '#111111', width: 1.5 } // Black lines
                }] : []),
                // Rejected region shading (p < alpha)
                {
                    type: 'rect',
                    x0: 0, x1: alpha,
                    y0: -2.5, y1: 2.0,
                    xref: 'x2', yref: 'y2',
                    fillcolor: 'rgba(214, 39, 40, 0.1)',
                    line: { width: 0 },
                    layer: 'below'
                }
            ];
        }

        function updatePlotly(idx) {
            const y_trial = data.y_trial_values[idx];
            const p_val = data.p_values[idx];
            const is_accepted = p_val > alpha;
            const color = is_accepted ? '#2ca02c' : '#d62728';

            // Restyle curve (trace 1), pseudo-point (trace 2), tracker (trace 4), tracker_line (trace 5)
            // trace_scatter is 0, trace_pvalue is 3
            Plotly.restyle('plot-container', {
                'y': [data.fitted_curves[idx], [y_trial], [y_trial], [y_trial, y_trial]],
                'x': [data.x_grid, [data.x_test], [p_val], [0, p_val]],
                'marker.color': [null, color, color, null],
                'line.color': ['#1f77b4', null, null, color]
            }, [1, 2, 4, 5]);

            updateUI(idx);
        }

        function updateUI(idx) {
            const y_trial = data.y_trial_values[idx];
            const p_val = data.p_values[idx];
            const is_accepted = p_val > alpha;
            
            yValDisplay.innerText = y_trial.toFixed(2);
            pValDisplay.innerText = `p = ${p_val.toFixed(3)}`;
            pValDisplay.style.color = is_accepted ? '#2ca02c' : '#d62728';
            
            statusBadge.innerText = is_accepted ? 'ACCEPTED' : 'REJECTED';
            statusBadge.className = `badge ${is_accepted ? 'badge-accepted' : 'badge-rejected'}`;
        }

        slider.addEventListener('input', (e) => {
            stopAutoplay();
            updatePlotly(parseInt(e.target.value));
        });
        
        alphaSlider.addEventListener('input', (e) => {
            alpha = parseFloat(e.target.value);
            alphaValDisplay.innerText = alpha.toFixed(2);
            computeInterval();
            Plotly.relayout('plot-container', { shapes: getShapes() });
            updatePlotly(parseInt(slider.value)); // to update colors of current point
        });

        // Autoplay Logic
        let autoplayReq;
        let isPlaying = false;
        let playDirection = 1;

        function stepAutoplay() {
            let current = parseInt(slider.value);
            current += playDirection;
            
            if (current >= n_trials - 1) {
                current = n_trials - 1;
                playDirection = -1; // bounce
            } else if (current <= 0) {
                current = 0;
                playDirection = 1; // bounce
            }
            
            slider.value = current;
            updatePlotly(current);
            
            if (isPlaying) {
                setTimeout(() => {
                    autoplayReq = requestAnimationFrame(stepAutoplay);
                }, 30);
            }
        }

        function toggleAutoplay() {
            if (isPlaying) {
                stopAutoplay();
            } else {
                isPlaying = true;
                autoplayBtn.innerText = '⏸ Pause';
                autoplayBtn.classList.add('active');
                stepAutoplay();
            }
        }
        
        function stopAutoplay() {
            isPlaying = false;
            autoplayBtn.innerText = '▶ Autoplay';
            autoplayBtn.classList.remove('active');
            if (autoplayReq) cancelAnimationFrame(autoplayReq);
        }

        autoplayBtn.addEventListener('click', toggleAutoplay);

        // Initialize
        initPlotly();

    </script>
</body>
</html>
"""

html_content = html_content.replace("__DATA_PLACEHOLDER__", data_json)

with open("conformal_visualization.html", "w") as f:
    f.write(html_content)

print("conformal_visualization.html written successfully.")
