document.addEventListener('DOMContentLoaded', () => {
    // --- UI Elements ---
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const toggleSciBtn = document.getElementById('toggle-scientific');
    const sciPanel = document.getElementById('scientific-panel');
    const mainDisplay = document.getElementById('main-display');
    const exprDisplay = document.getElementById('expression-display');
    const errorDisplay = document.getElementById('error-display');
    const equalsBtn = document.getElementById('equals-btn');
    const historyList = document.getElementById('history-list');
    const clearHistoryBtn = document.getElementById('clear-history-btn');

    // Converter Elements
    const convCategory = document.getElementById('conv-category');
    const convFromVal = document.getElementById('conv-from-val');
    const convToVal = document.getElementById('conv-to-val');
    const convFromUnit = document.getElementById('conv-from-unit');
    const convToUnit = document.getElementById('conv-to-unit');
    const swapUnitsBtn = document.getElementById('swap-units-btn');

    // --- State Variables ---
    let currentExpression = "";
    let unitsData = {};

    // --- Tab Navigation ---
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(`${btn.dataset.tab}-tab`).classList.add('active');
        });
    });

    // --- Scientific Mode Toggle ---
    toggleSciBtn.addEventListener('click', () => {
        sciPanel.classList.toggle('hidden');
        toggleSciBtn.classList.toggle('active');
    });

    // --- Calculator Inputs ---
    document.querySelectorAll('.keypad .btn').forEach(button => {
        button.addEventListener('click', () => {
            const action = button.dataset.action;
            const val = button.dataset.val;

            if (action === 'input' || action === 'func') {
                appendInput(val);
            } else if (action === 'clear') {
                clearAll();
            } else if (action === 'delete') {
                deleteLast();
            }
        });
    });

    equalsBtn.addEventListener('click', evaluateExpression);

    function appendInput(val) {
        errorDisplay.textContent = "";
        currentExpression += val;
        updateDisplay();
    }

    function clearAll() {
        currentExpression = "";
        errorDisplay.textContent = "";
        exprDisplay.textContent = "";
        mainDisplay.value = "0";
    }

    function deleteLast() {
        errorDisplay.textContent = "";
        currentExpression = currentExpression.slice(0, -1);
        updateDisplay();
    }

    function updateDisplay() {
        mainDisplay.value = currentExpression || "0";
    }

    // --- API Interactions ---
    async function evaluateExpression() {
        if (!currentExpression.trim()) return;

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ expression: currentExpression })
            });

            const data = await response.json();

            if (data.success) {
                exprDisplay.textContent = `${currentExpression} =`;
                mainDisplay.value = data.result;
                currentExpression = String(data.result);
                errorDisplay.textContent = "";
                fetchHistory();
            } else {
                errorDisplay.textContent = data.error || "Calculation error";
            }
        } catch (err) {
            errorDisplay.textContent = "Server communication error.";
        }
    }

    async function fetchHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            if (data.success) {
                renderHistory(data.history);
            }
        } catch (err) {
            console.error("Failed to fetch history", err);
        }
    }

    function renderHistory(items) {
        if (!items || items.length === 0) {
            historyList.innerHTML = `<p class="empty-history">No calculations yet</p>`;
            return;
        }

        historyList.innerHTML = items.map(item => `
            <div class="history-item" data-expr="${item.result}">
                <div class="history-expr">${item.expression} =</div>
                <div class="history-res">${item.result}</div>
            </div>
        `).join('');

        document.querySelectorAll('.history-item').forEach(el => {
            el.addEventListener('click', () => {
                currentExpression = el.dataset.expr;
                updateDisplay();
            });
        });
    }

    clearHistoryBtn.addEventListener('click', async () => {
        await fetch('/api/history', { method: 'DELETE' });
        fetchHistory();
    });

    // --- Keyboard Event Handler ---
    document.addEventListener('keydown', (e) => {
        const activeTab = document.querySelector('.tab-content.active').id;
        if (activeTab !== 'calculator-tab') return;

        if (e.key >= '0' && e.key <= '9') appendInput(e.key);
        else if (e.key === '.') appendInput('.');
        else if (e.key === '+') appendInput('+');
        else if (e.key === '-') appendInput('-');
        else if (e.key === '*') appendInput('×');
        else if (e.key === '/') appendInput('÷');
        else if (e.key === '(' || e.key === ')') appendInput(e.key);
        else if (e.key === '%') appendInput('%');
        else if (e.key === '^') appendInput('^');
        else if (e.key === 'Enter' || e.key === '=') { e.preventDefault(); evaluateExpression(); }
        else if (e.key === 'Backspace') deleteLast();
        else if (e.key === 'Escape') clearAll();
    });

    // --- Converter Functions ---
    async function initConverter() {
        try {
            const res = await fetch('/api/units');
            const data = await res.json();
            if (data.success) {
                unitsData = data.units;
                populateUnits(convCategory.value);
            }
        } catch (err) {
            console.error("Failed to fetch units setup.", err);
        }
    }

    function populateUnits(category) {
        const units = unitsData[category] || [];
        convFromUnit.innerHTML = units.map(u => `<option value="${u}">${u}</option>`).join('');
        convToUnit.innerHTML = units.map(u => `<option value="${u}">${u}</option>`).join('');
        
        if (units.length > 1) {
            convToUnit.selectedIndex = 1;
        }
        performConversion();
    }

    async function performConversion() {
        const val = parseFloat(convFromVal.value);
        if (isNaN(val)) {
            convToVal.value = "";
            return;
        }

        try {
            const res = await fetch('/api/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    category: convCategory.value,
                    value: val,
                    from_unit: convFromUnit.value,
                    to_unit: convToUnit.value
                })
            });
            const data = await res.json();
            if (data.success) {
                convToVal.value = data.result;
            }
        } catch (err) {
            console.error("Conversion request failed.", err);
        }
    }

    convCategory.addEventListener('change', (e) => populateUnits(e.target.value));
    convFromVal.addEventListener('input', performConversion);
    convFromUnit.addEventListener('change', performConversion);
    convToUnit.addEventListener('change', performConversion);

    swapUnitsBtn.addEventListener('click', () => {
        const temp = convFromUnit.value;
        convFromUnit.value = convToUnit.value;
        convToUnit.value = temp;
        performConversion();
    });

    // Initialize Page
    fetchHistory();
    initConverter();
});