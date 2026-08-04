document.addEventListener('DOMContentLoaded', () => {
    // State management
    let state = {
        expression: '',
        currentInput: '0',
        subDisplay: '',
        angleMode: 'DEG', // DEG or RAD
        memoryValue: 0,
        activeTab: 'standard', // standard, scientific, converter
        historyOpen: true,
        lastEvaluated: false
    };

    // DOM Elements
    const mainDisplay = document.getElementById('main-display');
    const subDisplay = document.getElementById('sub-display');
    const angleIndicator = document.getElementById('angle-mode-indicator');
    const memoryIndicator = document.getElementById('memory-indicator');
    const scientificKeypad = document.getElementById('scientific-keypad');
    const converterPanel = document.getElementById('converter-panel');
    const calcPanel = document.querySelector('.calc-panel');
    const historyDrawer = document.getElementById('history-drawer');
    const historyList = document.getElementById('history-list');
    const themeToggleBtn = document.getElementById('theme-toggle');
    const historyToggleBtn = document.getElementById('history-toggle');
    const clearHistoryBtn = document.getElementById('clear-history-btn');
    const btnDegRad = document.getElementById('btn-deg-rad');

    // Unit Converter Elements
    const convCategory = document.getElementById('conv-category');
    const convFromUnit = document.getElementById('conv-from-unit');
    const convToUnit = document.getElementById('conv-to-unit');
    const convFromVal = document.getElementById('conv-from-value');
    const convToVal = document.getElementById('conv-to-value');
    const convSwapBtn = document.getElementById('conv-swap-btn');

    let unitData = {};

    // Initialize application
    init();

    function init() {
        bindEvents();
        fetchHistory();
        loadConverterUnits();
        updateDisplay();
    }

    function bindEvents() {
        // Tab switching
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.target.getAttribute('data-tab');
                switchTab(tab);
            });
        });

        // Keypad button presses
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', handleButtonClick);
        });

        // Theme Toggle
        themeToggleBtn.addEventListener('click', () => {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            themeToggleBtn.querySelector('.theme-icon').textContent = newTheme === 'dark' ? '🌙' : '☀️';
        });

        // History Toggle
        historyToggleBtn.addEventListener('click', () => {
            state.historyOpen = !state.historyOpen;
            historyDrawer.classList.toggle('closed', !state.historyOpen);
        });

        // Clear History Button
        clearHistoryBtn.addEventListener('click', clearHistory);

        // Keyboard Support
        window.addEventListener('keydown', handleKeyboardInput);

        // Unit Converter Inputs
        if (convCategory) {
            convCategory.addEventListener('change', updateConverterUnits);
            convFromUnit.addEventListener('change', performConversion);
            convToUnit.addEventListener('change', performConversion);
            convFromVal.addEventListener('input', performConversion);
            convSwapBtn.addEventListener('click', swapUnits);
        }
    }

    function switchTab(tab) {
        state.activeTab = tab;
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-tab') === tab);
        });

        if (tab === 'converter') {
            calcPanel.style.display = 'none';
            converterPanel.classList.remove('hidden');
        } else {
            converterPanel.classList.add('hidden');
            calcPanel.style.display = 'flex';
            if (tab === 'scientific') {
                scientificKeypad.classList.remove('hidden');
            } else {
                scientificKeypad.classList.add('hidden');
            }
        }
    }

    function handleButtonClick(e) {
        const btn = e.currentTarget;
        const val = btn.getAttribute('data-value');
        const action = btn.getAttribute('data-action');

        if (val !== null) {
            appendValue(val);
        } else if (action !== null) {
            handleAction(action);
        }
    }

    function appendValue(val) {
        if (state.lastEvaluated) {
            if (['+', '-', '×', '÷', '^'].includes(val)) {
                state.expression = state.currentInput + val;
            } else {
                state.expression = val;
            }
            state.lastEvaluated = false;
        } else {
            if (state.expression === '0' && val !== '.') {
                state.expression = val;
            } else {
                state.expression += val;
            }
        }
        updateDisplay();
    }

    function handleAction(action) {
        switch (action) {
            case 'clear':
                state.expression = '';
                state.currentInput = '0';
                state.subDisplay = '';
                state.lastEvaluated = false;
                break;
            case 'backspace':
                if (state.lastEvaluated) {
                    state.expression = '';
                    state.lastEvaluated = false;
                } else if (state.expression.length > 0) {
                    state.expression = state.expression.slice(0, -1);
                }
                break;
            case 'equals':
                evaluateExpression();
                break;
            case 'angle-toggle':
                state.angleMode = state.angleMode === 'DEG' ? 'RAD' : 'DEG';
                angleIndicator.textContent = state.angleMode;
                btnDegRad.textContent = state.angleMode;
                break;
            case 'percent':
                if (state.expression) {
                    state.expression += '/100';
                    evaluateExpression();
                }
                break;
            case 'negate':
                if (state.expression) {
                    if (state.expression.startsWith('-')) {
                        state.expression = state.expression.substring(1);
                    } else {
                        state.expression = '-(' + state.expression + ')';
                    }
                }
                break;
            // Memory Operations
            case 'mc':
                state.memoryValue = 0;
                memoryIndicator.classList.add('hidden');
                break;
            case 'mr':
                appendValue(state.memoryValue.toString());
                break;
            case 'ms':
                state.memoryValue = parseFloat(state.currentInput) || 0;
                memoryIndicator.classList.remove('hidden');
                break;
            case 'm-add':
                state.memoryValue += parseFloat(state.currentInput) || 0;
                memoryIndicator.classList.remove('hidden');
                break;
            case 'm-sub':
                state.memoryValue -= parseFloat(state.currentInput) || 0;
                memoryIndicator.classList.remove('hidden');
                break;
        }
        updateDisplay();
    }

    function updateDisplay() {
        mainDisplay.textContent = state.expression || '0';
        subDisplay.textContent = state.subDisplay;
    }

    async function evaluateExpression() {
        if (!state.expression) return;

        state.subDisplay = state.expression + ' =';

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    expression: state.expression,
                    angle_mode: state.angleMode
                })
            });

            const data = await response.json();

            if (data.status === 'success') {
                state.currentInput = data.formatted_result;
                state.expression = data.formatted_result;
                state.lastEvaluated = true;
                updateDisplay();
                fetchHistory(); // Refresh history
            } else {
                mainDisplay.textContent = 'Error';
                subDisplay.textContent = data.message || 'Invalid Expression';
            }
        } catch (err) {
            mainDisplay.textContent = 'Error';
            subDisplay.textContent = 'Network or Server Error';
        }
    }

    function handleKeyboardInput(e) {
        if (state.activeTab === 'converter') return;

        const key = e.key;

        if (key >= '0' && key <= '9') appendValue(key);
        else if (key === '.') appendValue('.');
        else if (key === '+') appendValue('+');
        else if (key === '-') appendValue('-');
        else if (key === '*') appendValue('×');
        else if (key === '/') {
            e.preventDefault();
            appendValue('÷');
        }
        else if (key === '^') appendValue('^');
        else if (key === '(') appendValue('(');
        else if (key === ')') appendValue(')');
        else if (key === 'Enter' || key === '=') {
            e.preventDefault();
            evaluateExpression();
        }
        else if (key === 'Backspace') handleAction('backspace');
        else if (key === 'Escape') handleAction('clear');
    }

    // History Functions
    async function fetchHistory() {
        try {
            const res = await fetch('/api/history?limit=20');
            const data = await res.json();
            if (data.status === 'success') {
                renderHistory(data.history);
            }
        } catch (err) {
            console.error("Failed to load history:", err);
        }
    }

    function renderHistory(items) {
        if (!items || items.length === 0) {
            historyList.innerHTML = '<div class="empty-history">No history records found</div>';
            return;
        }

        historyList.innerHTML = items.map(item => `
            <div class="history-item" data-expr="${item.expression}" data-res="${item.result}">
                <div class="history-expr">${escapeHtml(item.expression)}</div>
                <div class="history-res">= ${escapeHtml(item.result)}</div>
            </div>
        `).join('');

        // Bind click on history items
        document.querySelectorAll('.history-item').forEach(el => {
            el.addEventListener('click', () => {
                const expr = el.getAttribute('data-res');
                state.expression = expr;
                state.lastEvaluated = false;
                updateDisplay();
            });
        });
    }

    async function clearHistory() {
        try {
            await fetch('/api/history', { method: 'DELETE' });
            renderHistory([]);
        } catch (err) {
            console.error("Failed to clear history:", err);
        }
    }

    // Unit Converter Logic
    async function loadConverterUnits() {
        try {
            const res = await fetch('/api/converter/units');
            const data = await res.json();
            if (data.status === 'success') {
                unitData = data.categories;
                updateConverterUnits();
            }
        } catch (err) {
            console.error("Failed to fetch unit metadata:", err);
        }
    }

    function updateConverterUnits() {
        const cat = convCategory.value;
        const units = unitData[cat] || [];

        convFromUnit.innerHTML = units.map(u => `<option value="${u}">${formatUnitName(u)}</option>`).join('');
        convToUnit.innerHTML = units.map(u => `<option value="${u}">${formatUnitName(u)}</option>`).join('');

        if (units.length > 1) {
            convToUnit.selectedIndex = 1;
        }

        performConversion();
    }

    async function performConversion() {
        const category = convCategory.value;
        const from_unit = convFromUnit.value;
        const to_unit = convToUnit.value;
        const value = parseFloat(convFromVal.value);

        if (isNaN(value)) {
            convToVal.value = '';
            return;
        }

        try {
            const res = await fetch('/api/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category, from_unit, to_unit, value })
            });

            const data = await res.json();
            if (data.status === 'success') {
                convToVal.value = data.formatted_result;
                fetchHistory(); // Refresh history
            } else {
                convToVal.value = 'Error';
            }
        } catch (err) {
            convToVal.value = 'Error';
        }
    }

    function swapUnits() {
        const temp = convFromUnit.value;
        convFromUnit.value = convToUnit.value;
        convToUnit.value = temp;
        performConversion();
    }

    function formatUnitName(unit) {
        return unit.replace(/_/g, ' ').toUpperCase();
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;")
                  .replace(/</g, "&lt;")
                  .replace(/>/g, "&gt;")
                  .replace(/"/g, "&quot;")
                  .replace(/'/g, "&#039;");
    }
});
</script>