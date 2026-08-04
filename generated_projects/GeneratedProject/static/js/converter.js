document.addEventListener("DOMContentLoaded", () => {
    const categorySelect = document.getElementById("conv-category");
    const fromUnitSelect = document.getElementById("conv-from-unit");
    const toUnitSelect = document.getElementById("conv-to-unit");
    const fromValInput = document.getElementById("conv-from-value");
    const toResultInput = document.getElementById("conv-to-result");
    const swapBtn = document.getElementById("conv-swap-btn");
    const mainTabs = document.querySelectorAll(".tab-btn");
    const viewPanels = document.querySelectorAll(".view-panel");

    let unitsMap = {};

    // Navigation Tab switching
    mainTabs.forEach(tab => {
        tab.addEventListener("click", () => {
            mainTabs.forEach(t => t.classList.remove("active"));
            viewPanels.forEach(p => p.classList.remove("active"));

            tab.classList.add("active");
            const target = tab.dataset.tab;
            document.getElementById(`${target}-view`).classList.add("active");
        });
    });

    // Fetch units map from backend
    async function initConverter() {
        try {
            const res = await fetch("/api/units");
            const data = await res.json();
            if (data.success) {
                unitsMap = data.units;
                populateUnits(categorySelect.value);
            }
        } catch (err) {
            console.error("Failed to load units structure", err);
        }
    }

    function populateUnits(category) {
        const units = unitsMap[category] || [];
        fromUnitSelect.innerHTML = units.map(u => `<option value="${u}">${formatUnitName(u)}</option>`).join("");
        toUnitSelect.innerHTML = units.map(u => `<option value="${u}">${formatUnitName(u)}</option>`).join("");
        
        if (units.length > 1) {
            toUnitSelect.selectedIndex = 1;
        }
        performConversion();
    }

    function formatUnitName(unit) {
        return unit.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
    }

    async function performConversion() {
        const category = categorySelect.value;
        const fromUnit = fromUnitSelect.value;
        const toUnit = toUnitSelect.value;
        const val = parseFloat(fromValInput.value);

        if (isNaN(val)) {
            toResultInput.value = "";
            return;
        }

        try {
            const res = await fetch("/api/convert", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    category: category,
                    from_unit: fromUnit,
                    to_unit: toUnit,
                    value: val
                })
            });

            const data = await res.json();
            if (data.success) {
                toResultInput.value = data.data.result;
            } else {
                toResultInput.value = "Error";
            }
        } catch (e) {
            toResultInput.value = "Error";
        }
    }

    categorySelect.addEventListener("change", () => populateUnits(categorySelect.value));
    fromUnitSelect.addEventListener("change", performConversion);
    toUnitSelect.addEventListener("change", performConversion);
    fromValInput.addEventListener("input", performConversion);

    swapBtn.addEventListener("click", () => {
        const temp = fromUnitSelect.value;
        fromUnitSelect.value = toUnitSelect.value;
        toUnitSelect.value = temp;
        performConversion();
    });

    initConverter();
});