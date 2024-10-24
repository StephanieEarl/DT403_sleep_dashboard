async function fetchDataAndRenderChart(
    apiEndpoint,
    chartElementId,
    chartConfig
) {
    try {
        let response = await fetch(apiEndpoint);
        let data = await response.json();
        console.log("Data received from API:", data); // Add this line
        const ctx = document.getElementById(chartElementId).getContext("2d");
        new Chart(ctx, chartConfig(data)); // Corrected this line from new chartConfig(ctx, chartConfig(data));
    }   catch (error) {
        console.error("Error fetching or rendering chart:", error);
    }
}

fetchDataAndRenderChart("/api/sessions_attended", "sessionsAttendedChart", (data) => ({
    type: "line",
    data: {
        labels: data.dates,
        datasets: [
            {
                label: "Sessions Attended Over Time",
                data: data.attended,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false

            },

        ],
    },
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'month'
                }
            },
            y: {
                beginAtZero: true
            }
        }
    }
}));

fetchDataAndRenderChart("/api/sessions_dna", "sessionsDnaChart", (data) => ({
    type: "line",
    data: {
        labels: data.dates,
        datasets: [
            {
                    label: "Sessions DNA Over Time",
                    data: data.dna,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: false
            },

        ],
    },
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'month'
                }
            },
            y: {
                beginAtZero: true
            }
        }
    }
}));


fetchDataAndRenderChart("/api/participants_per_age", "participantAgeChart", (data) => ({
    type: "bar",
    data: {
        labels: data.age,
        datasets: [
            {
                label: "participants",
                data: data.num_participants,
            },

        ],
    },
    // not sure whether I need this chart to be responsive nor to start at zero so have removed
  

        
}));

fetchDataAndRenderChart("/api/course_status", "courseStatusChart", (data) => ({
    type: "pie",
    data: {
        labels: data.status,
        datasets: [
            {
                label: "Number of participants",
                data: data.counts,
            },

        ],
    },
    
}));

fetchDataAndRenderChart("/api/sleep_disorder", "sleepDisorderChart", (data) => ({
    type: "pie",
    data: {
        labels: data.disorders,
        datasets: [
            {
                label: "Number of participants",
                data: data.counts,
            },

        ],
    },
    
}))