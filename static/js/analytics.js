// Function to fetch enrollment data and update the graph
function fetchEnrollmentsDataAndUpdateGraph() {
    fetch('/api/enrollments')
        .then(response => response.json())
        .then(data => {
            if (enrollmentsGraph) {
                enrollmentsGraph.data.labels = data.labels;
                enrollmentsGraph.data.datasets[0].data = data.datasets[0].data;
                enrollmentsGraph.update();
            }
        });
}

// Function to fetch grades data and update the graph
function fetchGradesDataAndUpdateGraph() {
    fetch('/api/grades')
        .then(response => response.json())
        .then(data => {
            if (gradesGraph) {
                gradesGraph.data.labels = data.labels;
                gradesGraph.data.datasets[0].data = data.datasets[0].data;
                gradesGraph.update();
            }
        });
}

// Function to show toast messages
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toastContainer');
    const toastId = `toast-${Date.now()}`;
    const toast = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-delay="3000">
            <div class="toast-header ${type === 'success' ? 'toast-success' : 'toast-error'}">
                <strong class="mr-auto">Notification</strong>
                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="toast-body">${message}</div>
        </div>
    `;
    toastContainer.insertAdjacentHTML('beforeend', toast);
    $(`#${toastId}`).toast('show').on('hidden.bs.toast', function () {
        $(this).remove();
    });
}


document.getElementById('addStudentForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const studentName = document.getElementById('studentName').value;
    const studentEmail = document.getElementById('studentEmail').value;

    fetch('/api/add_student', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: studentName,
            email: studentEmail
        })
    })
    .then(response => response.json())
    .then(data => {
        showToast(data.message);; // Replace with a more user-friendly message or modal
        // Optionally clear the form or update the UI
    })
    .catch(error => {
        alert('An error occurred.');
        console.error('Error:', error);
    });
});


function populateSelectOptions() {
    // Fetch students and populate the student select dropdown
    fetch('/api/students')
        .then(response => response.json())
        .then(students => {
            const studentSelect = document.getElementById('enrollmentStudent');
            students.forEach(student => {
                let option = new Option(student.name, student.id);
                studentSelect.add(option);
            });
        });

    // Fetch courses and populate the course select dropdown
    fetch('/api/courses')
        .then(response => response.json())
        .then(courses => {
            const courseSelect = document.getElementById('enrollmentCourse');
            courses.forEach(course => {
                let option = new Option(course.title, course.id);
                courseSelect.add(option);
            });
        });

    fetch('/api/times')
    .then(response => response.json())
    .then(courses => {
        const courseSelect = document.getElementById('enrollmentTime');
        courses.forEach(time => {
            let option = new Option(time.semester, time.id);
            courseSelect.add(option);
        });
    });

}

document.getElementById('addEnrollmentForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const enrollmentStudent = document.getElementById('enrollmentStudent').value;
    const enrollmentCourse = document.getElementById('enrollmentCourse').value;
    const enrollmentTime = document.getElementById("enrollmentTime").value;
    const enrollmentGrade = document.getElementById("enrollmentGrade").value;
    const enrollmentAttendace = document.getElementById("enrollmentAttendance").value;

    // Add additional fields like grade and attendance as needed

    fetch('/api/add_enrollment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            student_id: enrollmentStudent,
            course_id: enrollmentCourse,
            time_id: enrollmentTime,
            grade: enrollmentGrade,
            attendance_percentage: enrollmentAttendace
            // Other fields...
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Display success message
        // Optionally clear the form and refresh the graphs
    })
    .catch(error => {
        alert('An error occurred.');
        console.error('Error:', error);
    });
});

// Call this function when the page loads to populate select elements
document.addEventListener('DOMContentLoaded', function() {
    populateSelectOptions();
    // Existing code to render and fetch graph data...
});


// Define global variables for the graphs
let enrollmentsGraph;
let gradesGraph;

// Function to render the graphs
function renderGraphs() {
    const ctxEnrollments = document.getElementById('enrollmentsGraph').getContext('2d');
    enrollmentsGraph = new Chart(ctxEnrollments, {
        type: 'bar',
        data: {
            labels: [], // Placeholder for dynamic labels from the backend
            datasets: [{
                label: 'Number of Enrollments',
                data: [], // Placeholder for dynamic data from the backend
                backgroundColor: 'rgba(0, 123, 255, 0.5)', // Customize color as needed
                borderColor: 'rgba(0, 123, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    const ctxGrades = document.getElementById('gradesGraph').getContext('2d');
    gradesGraph = new Chart(ctxGrades, {
        type: 'pie',
        data: {
            labels: [], // Placeholder for dynamic labels from the backend
            datasets: [{
                label: 'Grades Distribution',
                data: [], // Placeholder for dynamic data from the backend
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
    });
}

// Call these functions when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    renderGraphs();
    fetchEnrollmentsDataAndUpdateGraph();
    fetchGradesDataAndUpdateGraph();

    // Set up intervals for real-time updates
    setInterval(fetchEnrollmentsDataAndUpdateGraph, 5000); // Every 5 seconds
    setInterval(fetchGradesDataAndUpdateGraph, 5000); // Every 5 seconds
});