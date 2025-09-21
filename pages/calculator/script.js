const ctx = document.getElementById('retirement-chart').getContext('2d');
let investmentChart;

function calculateRetirement() {
    // Reset backgrounds
    document.getElementById('inflation-rate').style.backgroundColor = '';
    document.getElementById('fund-growth-rate').style.backgroundColor = '';
    document.getElementById('age-at-retirement').style.backgroundColor = '';
    document.getElementById('age-at-expiration').style.backgroundColor = '';
    document.getElementById('age-at-reduced-mobility').style.backgroundColor = '';
    document.getElementById('reduced-mobility-expenses').style.backgroundColor = '';

    let inflationRateValue = parseFloat(document.getElementById('inflation-rate').value);
    let growthRateValue = parseFloat(document.getElementById('fund-growth-rate').value);

    if (isNaN(inflationRateValue) || inflationRateValue < 0 || inflationRateValue > 20) {
        document.getElementById('inflation-rate').style.backgroundColor = '#ffcccc';
        return;
    }

    if (isNaN(growthRateValue) || growthRateValue < 0 || growthRateValue > 100) {
        document.getElementById('fund-growth-rate').style.backgroundColor = '#ffcccc';
        return;
    }

    // Round to two decimal places
    inflationRateValue = Math.round(inflationRateValue * 100) / 100;
    growthRateValue = Math.round(growthRateValue * 100) / 100;

    // Update input fields to show rounded values
    document.getElementById('inflation-rate').value = inflationRateValue.toFixed(2);
    document.getElementById('fund-growth-rate').value = growthRateValue.toFixed(2);

    // Now use in calculation
    const inflationRate = inflationRateValue / 100;
    const growthRate = growthRateValue / 100;
    let ageAtRetirementValue = document.getElementById('age-at-retirement').value;
    let ageAtExpirationValue = document.getElementById('age-at-expiration').value;
    const ageAtRetirement = parseInt(ageAtRetirementValue);
    const ageAtExpiration = parseInt(ageAtExpirationValue);
    const annualExpenses = parseFloat(document.getElementById('annual-expenses').value);

    if (isNaN(ageAtRetirement) || ageAtRetirement < 20 || ageAtRetirement > 85 || parseFloat(ageAtRetirementValue) !== ageAtRetirement) {
        document.getElementById('age-at-retirement').style.backgroundColor = '#ffcccc';
        return;
    }

    if (isNaN(ageAtExpiration) || ageAtExpiration < 65 || ageAtExpiration > 100 || parseFloat(ageAtExpirationValue) !== ageAtExpiration) {
        document.getElementById('age-at-expiration').style.backgroundColor = '#ffcccc';
        return;
    }
    
    let reducedMobilityAgeValue = document.getElementById('age-at-reduced-mobility').value;
    const reducedMobilityAge = parseInt(reducedMobilityAgeValue);
    if (isNaN(reducedMobilityAge) || reducedMobilityAge < 50 || reducedMobilityAge > 100 || parseFloat(reducedMobilityAgeValue) !== reducedMobilityAge) {
        document.getElementById('age-at-reduced-mobility').style.backgroundColor = '#ffcccc';
        return;
    }
    
    let reducedMobilityExpensesValue = document.getElementById('reduced-mobility-expenses').value;
    const reducedMobilityExpenses = parseInt(reducedMobilityExpensesValue);
    if (isNaN(reducedMobilityExpenses) || reducedMobilityExpenses < -100 || reducedMobilityExpenses > 100 || parseFloat(reducedMobilityExpensesValue) !== reducedMobilityExpenses) {
        document.getElementById('reduced-mobility-expenses').style.backgroundColor = '#ffcccc';
        return;
    }
    
    const reducedMobilityExpensesPercent = reducedMobilityExpenses / 100;
    
    const years = ageAtExpiration - ageAtRetirement;
    const r = 1 + growthRate - inflationRate;
    
    // Calculate required initial investment by working backwards
    let balance = 0; // Balance at expiration
    for (let yearFromRetirement = years - 1; yearFromRetirement >= 0; yearFromRetirement--) {
        const currentAge = ageAtRetirement + yearFromRetirement;
        const expensesForYear = (currentAge >= reducedMobilityAge) ? annualExpenses * (1 + reducedMobilityExpensesPercent) : annualExpenses;
        balance = (balance + expensesForYear) / r;
    }
    const requiredInitialInvestment = balance;
    
    // Display the required initial investment as integer with thousands separator
    document.getElementById('required-investment').textContent = `$${Math.round(requiredInitialInvestment).toLocaleString()}`;
    
    // Now simulate forward to plot the chart
    const balances = [];
    const labels = [];
    let currentBalance = requiredInitialInvestment;
    let currentAge = ageAtRetirement;

    for (let year = 0; year <= years; year++) {
        balances.push(currentBalance.toFixed(2));
        labels.push(currentAge);
        // Apply growth and subtract expenses for the next year
        if (year < years) {
            const expensesThisYear = (currentAge >= reducedMobilityAge) ? annualExpenses * (1 + reducedMobilityExpensesPercent) : annualExpenses;
            currentBalance = currentBalance * r - expensesThisYear;
            if (currentBalance < 0) currentBalance = 0; // Prevent negative balance
            currentAge++;
        }
    }

    updateChart(labels, balances, annualExpenses);
}

function updateChart(labels, balances, annualExpenses) {
    if (investmentChart) {
        investmentChart.destroy();
    }

    // Define expense buttons with RGB values
    const expenseButtons = [
        {value: 50000, rgb: [178, 0, 0]}, // red
        {value: 75000, rgb: [178, 115, 0]}, // orange
        {value: 100000, rgb: [0, 89, 0]}, // green
        {value: 150000, rgb: [0, 0, 178]}, // blue
        {value: 250000, rgb: [103, 0, 147]} // darkviolet
    ];

    let values = expenseButtons.map(b => b.value);
    let rgbs = expenseButtons.map(b => b.rgb);

    // Find the interval for interpolation
    let index = 0;
    if (annualExpenses < values[0]) {
        // use index = 0
    } else if (annualExpenses >= values[values.length - 1]) {
        index = values.length - 2;
    } else {
        for (let i = 0; i < values.length - 1; i++) {
            if (annualExpenses >= values[i] && annualExpenses < values[i + 1]) {
                index = i;
                break;
            }
        }
    }

    let val1 = values[index];
    let val2 = values[index + 1];
    let rgb1 = rgbs[index];
    let rgb2 = rgbs[index + 1];

    let factor = (annualExpenses - val1) / (val2 - val1);
    if (isNaN(factor) || !isFinite(factor)) factor = 0;

    let newRgb = [
        Math.round(rgb1[0] + factor * (rgb2[0] - rgb1[0])),
        Math.round(rgb1[1] + factor * (rgb2[1] - rgb1[1])),
        Math.round(rgb1[2] + factor * (rgb2[2] - rgb1[2]))
    ];

    let rgba = `rgba(${newRgb[0]}, ${newRgb[1]}, ${newRgb[2]}, 1)`;
    let rgbaBg = `rgba(${newRgb[0]}, ${newRgb[1]}, ${newRgb[2]}, 0.2)`;

    investmentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: '',
                data: balances,
                borderColor: rgba,
                backgroundColor: rgbaBg,
                borderWidth: 2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Net Fund Balance ($)'
                    },
                    ticks: {
                        callback: function(value) {
                            if (value >= 1000000) {
                                return (value / 1000000).toFixed(1) + 'm';
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(0) + 'k';
                            } else {
                                return value;
                            }
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Age'
                    }
                }
            }
        }
    });
}

function resetToDefaults() {
    document.getElementById('inflation-rate').value = '2.5';
    document.getElementById('fund-growth-rate').value = '7';
    document.getElementById('age-at-retirement').value = '65';
    document.getElementById('age-at-expiration').value = '92';
    document.getElementById('age-at-reduced-mobility').value = '85';
    document.getElementById('reduced-mobility-expenses').value = '-7';
    document.getElementById('annual-expenses').value = '75000';
    calculateRetirement();
}

document.getElementById('resetButton').addEventListener('click', resetToDefaults);

// Add event listener for calculate button
document.getElementById('calculateButton').addEventListener('click', calculateRetirement);

// Calculate and generate chart on page load
window.addEventListener('load', calculateRetirement);

// Trigger calculation on field focus changes
document.getElementById('inflation-rate').addEventListener('blur', calculateRetirement);
document.getElementById('fund-growth-rate').addEventListener('blur', calculateRetirement);
document.getElementById('age-at-retirement').addEventListener('blur', calculateRetirement);
document.getElementById('age-at-expiration').addEventListener('blur', calculateRetirement);
document.getElementById('age-at-reduced-mobility').addEventListener('blur', calculateRetirement);
document.getElementById('reduced-mobility-expenses').addEventListener('blur', calculateRetirement);
document.getElementById('annual-expenses').addEventListener('blur', calculateRetirement);