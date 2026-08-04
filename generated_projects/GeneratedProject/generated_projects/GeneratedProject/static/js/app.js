document.addEventListener("DOMContentLoaded", () => {
    // UI Elements
    const expressionDisplay = document.getElementById("expressionDisplay");
    const resultDisplay = document.getElementById("resultDisplay");
    const errorMessage = document.getElementById("errorMessage");
    const keypad = document.getElementById("calculatorKeypad");
    const modeToggleBtn = document.getElementById("modeToggleBtn");
    const themeToggleBtn = document.getElementById("themeToggleBtn");
    const historyToggleBtn = document.getElementById("historyToggleBtn");
    const historyDrawer = document.getElementById("historyDrawer");
    const closeHistoryBtn = document.getElementById("closeHistoryBtn");
    const clearHistoryBtn = document.getElementById("clearHistoryBtn");
    const historyList = document.getElementById("historyList");

    // State Variables
    let currentExpression = "";
    let isCalculated = false;

    // --- Keypad Click Handling ---
    keypad.addEventListener("click", (e) => {
        const btn = e.target.closest(".btn");
        if (!btn) return;

        const action = btn.dataset.action;
        const value = btn.dataset.value;

        handleAction(action, value);
    });

    function handleAction(action, value) {
        hideError();

        if (action === "input") {
            if (isCalculated) {
                // If operator pressed after evaluation, continue with previous result
                if (["+", "-", "*", "/", "%", "^"].includes(value)) {
                    currentExpression = resultDisplay.textContent + value;
                } else {
                    currentExpression = value;
                }
                isCalculated = false;
            } else {
                currentExpression += value;
            }
        } else if (action === "func") {
            if (isCalculated) {
                currentExpression = value;
                isCalculated = false;
            } else {
                currentExpression += value;
            }
        } else if (action === "clear") {
            currentExpression = "";
            resultDisplay.textContent = "0";
            isCalculated = false;
        } else if (action === "backspace") {
            if (isCalculated) {
                currentExpression = "";
                resultDisplay.textContent = "0";
                isCalculated = false;
            } else {
                currentExpression = currentExpression.slice(0, -1);
            }
        } else if (action === "calculate") {
            executeCalculation();
            return;
        }

        updateDisplay();
    }

    function updateDisplay() {
        expressionDisplay.textContent = currentExpression;
    }

    async function executeCalculation() {
        if (!currentExpression.trim()) return;

        try {
            const response = await fetch("/api/calculate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ expression: currentExpression })
            });

            const data = await response.json();

            if (data.success) {
                resultDisplay.textContent = data.result;
                isCalculated = true;
                fetchHistory(); // Refresh history panel if open
            } else {
                showError(data.error || "Calculation error");
            }
        } catch (err) {
            showError("Server connection failed");
        }
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.classList.add("visible");
        setTimeout(() => hideError(), 3500);
    }

    function hideError() {
        errorMessage.classList.remove("visible");
    }

    // --- Scientific Mode Toggle ---
    modeToggleBtn.addEventListener("click", () => {
        keypad.classList.toggle("scientific-mode");
        modeToggleBtn.classList.toggle("active");
    });

    // --- Theme Toggle ---
    themeToggleBtn.addEventListener("click", () => {
        const html = document.documentElement;
        const currentTheme = html.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        html.setAttribute("data-theme", newTheme);
    });

    // --- History Drawer ---
    historyToggleBtn.addEventListener("click", () => {
        historyDrawer.classList.toggle("visible");
        if (historyDrawer.classList.contains("visible")) {
            fetchHistory();
        }
    });

    closeHistoryBtn.addEventListener("click", () => {
        historyDrawer.classList.remove("visible");
    });

    async function fetchHistory() {
        try {
            const res = await fetch("/api/history");
            const data = await res.json();

            if (data.success && data.history) {
                renderHistory(data.history);
            }
        } catch (err) {
            console.error("Failed to fetch history:", err);
        }
    }

    function renderHistory(items) {
        if (items.length === 0) {
            historyList.innerHTML = '<div class="empty-history">No history yet</div>';
            return;
        }

        historyList.innerHTML = items.map(item => `
            <div class="history-item" data-expr="${escapeHtml(item.expression)}" data-res="${escapeHtml(item.result)}">
                <div class="hist-expr">${escapeHtml(item.expression)} =</div>
                <div class="hist-res">${escapeHtml(item.result)}</div>
            </div>
        `).join("");

        // Add restore event listener
        document.querySelectorAll(".history-item").forEach(item => {
            item.addEventListener("click", () => {
                currentExpression = item.dataset.expr;
                resultDisplay.textContent = item.dataset.res;
                updateDisplay();
                isCalculated = false;
            });
        });
    }

    clearHistoryBtn.addEventListener("click", async () => {
        try {
            const res = await fetch("/api/history", { method: "DELETE" });
            const data = await res.json();
            if (data.success) {
                renderHistory([]);
            }
        } catch (err) {
            showError("Failed to clear history");
        }
    });

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }

    // --- Keyboard Navigation ---
    document.addEventListener("keydown", (e) => {
        if (e.key >= "0" && e.key <= "9") {
            handleAction("input", e.key);
        } else if (e.key === ".") {
            handleAction("input", ".");
        } else if (["+", "-", "*", "/", "%", "(", ")"].includes(e.key)) {
            handleAction("input", e.key);
        } else if (e.key === "^") {
            handleAction("input", "^");
        } else if (e.key === "Enter" || e.key === "=") {
            e.preventDefault();
            handleAction("calculate");
        } else if (e.key === "Backspace") {
            handleAction("backspace");
        } else if (e.key === "Escape" || e.key.toLowerCase() === "c") {
            handleAction("clear");
        }
    });
});