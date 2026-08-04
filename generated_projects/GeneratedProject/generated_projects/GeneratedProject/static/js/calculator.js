document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const calculatorCard = document.querySelector('.calculator-card');
    const expressionDisplay = document.getElementById('expression-display');
    const resultDisplay = document.getElementById('result-display');
    const errorToast = document.getElementById('error-toast');
    
    const modeBtns = document.querySelectorAll('.mode-btn');
    const keypadView = document.getElementById('keypad-view');
    const converterView = document.getElementById('converter-view');
    
    const toggleHistoryBtn = document.getElementById('toggle-history');
    const closeHistoryBtn = document.getElementById('close-history');
    const historySidebar = document.getElementById('history-sidebar');
    const historyList = document.getElementById('history-list');
    const clearHistoryBtn = document.getElementById('clear-history-btn');

    // Unit Converter Elements
    const converterCategory = document.getElementById('converter-category');
    const convertFromUnit = document.getElementById('convert-from-unit');
    const convertToUnit = document.getElementById('convert-to-unit');
    const convertFromVal = document.getElementById('convert-from-val');
    const convertToVal = document.getElementById('convert-to-val');
    const swapUnitsBtn = document.getElementById('swap-units');

    // Calculator State
    let currentExpression = '';
    let lastEvaluated = false;
    let currentMode = 'standard';

    // Converter Units Configuration
    const unitOptions = {
        length: [
            { id: 'm', label: 'Meters (m)' },
            { id: 'km', label: 'Kilometers (km)' },
            { id: 'cm', label: 'Centimeters (cm)' },
            { id: 'mm', label: 'Millimeters (mm)' },
            { id: 'in', label: 'Inches (in)' },
            { id: 'ft', label: 'Feet (ft)' },
            { id: 'yd', label: 'Yards (yd)' },
            { id: 'mi', label: 'Miles (mi)' }
        ],
        weight: [
            { id: 'kg', label: 'Kilograms (kg)' },
            { id: 'g', label: 'Grams (g)' },
            { id: 'mg', label: 'Milligrams (mg)' },
            { id: 'lb', label: 'Pounds (lb)' },
            { id: 'oz', label: 'Ounces (oz)' },
            { id: 'ton', label: 'Metric Tons (t)' }
        ],
        temperature: [
            { id: 'c', label: 'Celsius (°C)' },
            { id: 'f', label: 'Fahrenheit (°F)' },
            { id: 'k', label: 'Kelvin (K)' }
        ],
        area: [
            { id: 'sq_m', label: 'Square Meters (m²)' },
            { id: 'sq_km', label: 'Square Kilometers (km²)' },
            { id: 'sq_ft', label: 'Square Feet (ft²)' },
            { id: 'acre', label: 'Acres' },
            { id: 'hectare', label: 'Hectares' }
        ],
        volume: [
            { id: 'l', label: 'Liters (L)' },
            { id: 'ml', label: 'Milliliters (mL)' },
            { id: 'cu_m', label: 'Cubic Meters (m³)' },
            { id: 'gal', label: 'Gallons (gal)' },
            { id: 'cup', label: 'Cups' }
        ]
    };

    // --- Mode Switching ---
    modeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentMode = btn.dataset.mode;

            if (currentMode === 'standard') {
                calculatorCard.classList.remove('wide');
                keypadView.classList.remove('hidden');
                converterView.classList.add('hidden');
            } else if (currentMode === 'scientific') {
                calculatorCard.classList.add('wide');
                keypadView.classList.remove('hidden');
                converterView.classList.add('hidden');
            } else if (currentMode === 'converter') {
                calculatorCard.classList.remove('wide');
                keypadView.classList.add('hidden');
                converterView.classList.remove('hidden');
                updateConverterUnits();
            }
        });
    });

    // --- Calculator Keypad Handlers ---
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', () => {
            const action = button.dataset.action;
            const value = button.dataset.value;
            handleKeypadAction(action, value);
        });
    });

    function handleKeypadAction(action, value) {
        hideError();

        if (action === 'clear') {
            currentExpression = '';
            expressionDisplay.textContent = '';
            resultDisplay.textContent = '0';
            lastEvaluated = false;
        } else if (action === 'backspace') {
            if (lastEvaluated) {
                currentExpression = '';
                lastEvaluated = false;
            } else {
                currentExpression = currentExpression.slice(0, -1);
            }
            updateDisplay();
        } else if (action === 'insert' || action === 'func' || action === 'operator') {
            if (lastEvaluated) {
                // If previous computation finished, clear or append based on type
                if (action === 'operator') {
                    // Carry forward result
                    currentExpression = resultDisplay.textContent;
                } else {
                    currentExpression = '';
                }
                lastEvaluated = false;
            }
            currentExpression += value;
            updateDisplay();
        } else if (action === 'calculate') {
            performCalculation();
        }
    }

    function updateDisplay() {
        expressionDisplay.textContent = currentExpression;
        if (currentExpression === '') {
            resultDisplay.textContent = '0';
        }
    }

    async function performCalculation() {
        if (!currentExpression.trim()) return;

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ expression: currentExpression })
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                resultDisplay.textContent = data.formatted_result;
                lastEvaluated = true;
                fetchHistory();
            } else {
                showError(data.message || 'Error evaluating expression');
            }
        } catch (err) {
            showError('Network error connecting to calculation server');
        }
    }

    function showError(msg) {
        errorToast.textContent = msg;
        errorToast.classList.remove('hidden');
        setTimeout(() => {
            hideError();
        }, 3500);
    }

    function hideError() {
        errorToast.classList.add('hidden');
    }

    // --- Keyboard Accessibility Support ---
    document.addEventListener('keydown', (e) => {
        if (currentMode === 'converter') return; // Disable standard keyboard shortcuts when converting

        if ((e.key >= '0' && e.key <= '9') || e.key === '.') {
            handleKeypadAction('insert', e.key);
        } else if (['+', '-', '*', '/'].includes(e.key)) {
            const map = { '*': '×', '/': '÷' };
            handleKeypadAction('operator', map[e.key] || e.key);
        } else if (e.key === 'Enter' || e.key === '=') {
            e.preventDefault();
            handleKeypadAction('calculate');
        } else if (e.key === 'Backspace') {
            handleKeypadAction('backspace');
        } else if (e.key === 'Escape') {
            handleKeypadAction('clear');
        } else if (e.key === '(' || e.key === ')') {
            handleKeypadAction('insert', e.key);
        } else if (e.key === '^') {
            handleKeypadAction('operator', '^');
        }
    });

    // --- Converter Functionality ---
    function updateConverterUnits() {
        const cat = converterCategory.value;
        const options = unitOptions[cat] || [];

        convertFromUnit.innerHTML = '';
        convertToUnit.innerHTML = '';

        options.forEach((opt, idx) => {
            const opt1 = new Option(opt.label, opt.id);
            const opt2 = new Option(opt.label, opt.id);
            convertFromUnit.add(opt1);
            convertToUnit.add(opt2);
        });

        if (options.length > 1) {
            convertToUnit.selectedIndex = 1;
        }

        executeConversion();
    }

    async function executeConversion() {
        const category = converterCategory.value;
        const fromUnit = convertFromUnit.value;
        const toUnit = convertToUnit.value;
        const val = parseFloat(convertFromVal.value);

        if (isNaN(val)) {
            convertToVal.textContent = '0';
            return;
        }

        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    category: category,
                    from_unit: fromUnit,
                    to_unit: toUnit,
                    value: val
                })
            });

            const data = await response.json();
            if (response.ok && data.status === 'success') {
                convertToVal.textContent = data.formatted_result;
            } else {
                convertToVal.textContent = 'Error';
            }
        } catch (e) {
            convertToVal.textContent = 'Error';
        }
    }

    converterCategory.addEventListener('change', updateConverterUnits);
    convertFromUnit.addEventListener('change', executeConversion);
    convertToUnit.addEventListener('change', executeConversion);
    convertFromVal.addEventListener('input', executeConversion);

    swapUnitsBtn.addEventListener('click', () => {
        const temp = convertFromUnit.value;
        convertFromUnit.value = convertToUnit.value;
        convertToUnit.value = temp;
        executeConversion();
    });

    // --- History Sidebar Management ---
    toggleHistoryBtn.addEventListener('click', () => {
        historySidebar.classList.toggle('closed');
        if (!historySidebar.classList.contains('closed')) {
            fetchHistory();
        }
    });

    closeHistoryBtn.addEventListener('click', () => {
        historySidebar.classList.add('closed');
    });

    async function fetchHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();

            if (data.status === 'success') {
                renderHistory(data.history);
            }
        } catch (e) {
            console.error('Failed to load history', e);
        }
    }

    function renderHistory(items) {
        if (!items || items.length === 0) {
            historyList.innerHTML = '<div class="history-empty">No calculations yet</div>';
            return;
        }

        historyList.innerHTML = '';
        items.forEach(item => {
            const el = document.createElement('div');
            el.className = 'history-item';
            el.innerHTML = `
                <div class="history-expr">${escapeHtml(item.expression)}</div>
                <div class="history-res">= ${escapeHtml(item.result)}</div>
            `;
            el.addEventListener('click', () => {
                currentExpression = item.result;
                expressionDisplay.textContent = item.expression;
                resultDisplay.textContent = item.result;
                lastEvaluated = true;
            });
            historyList.appendChild(el);
        });
    }

    clearHistoryBtn.addEventListener('click', async () => {
        try {
            await fetch('/api/history/clear', { method: 'POST' });
            fetchHistory();
        } catch (e) {
            console.error('Failed to clear history', e);
        }
    });

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    // Initial state load
    fetchHistory();
});