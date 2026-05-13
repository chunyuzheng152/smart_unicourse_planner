fetch("/api/charts")
    .then(response => response.json())
    .then(data => {
        const popularMajorCanvas = document.getElementById("popularMajorChart");
        const choiceReasonCanvas = document.getElementById("choiceReasonChart");

        if (popularMajorCanvas) {
            new Chart(popularMajorCanvas, {
                type: "bar",
                data: {
                    labels: data.popular_majors.labels,
                    datasets: [{
                        label: "Popular Majors",
                        data: data.popular_majors.values
                    }]
                },
                options:{
                    responsive: true,
                    scales:{
                        y:{
                           beginAtZero: true     
                        }
                    }
                }
            });
        }

        if (choiceReasonCanvas) {
            new Chart(choiceReasonCanvas, {
                type: "pie",
                data: {
                    labels: data.choice_reasons.labels,
                    datasets: [{
                        label: "Major Choice Reasons",
                        data: data.choice_reasons.values
                    }]
                },
                options:{
                    responsive:true
                }
            });
        }
    })

    .catch(error => {
        console.error("Errir loading chart data:", error);

    });