// QueryLens main JavaScript file
document.addEventListener("DOMContentLoaded", () => {
    console.log("QueryLens client initialized with Bootstrap styling.");
    
    const queryForm = document.getElementById("query-form");
    if (queryForm) {
        queryForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const nlQuery = document.getElementById("nl-query").value;
            console.log("Submitted query:", nlQuery);
            // Dynamic fetch implementation will go here
        });
    }
});
