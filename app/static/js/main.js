// QueryLens Interactive Client UI
document.addEventListener("DOMContentLoaded", () => {
    console.log("QueryLens Bootstrap frontend client loaded.");
    
    const queryForm = document.getElementById("query-form");
    const submitBtn = document.getElementById("submit-btn");
    const statusContainer = document.getElementById("status-container");
    const resultsCard = document.getElementById("results-card");
    const generatedSql = document.getElementById("generated-sql");
    const explanationContainer = document.getElementById("explanation-container");
    const queryExplanation = document.getElementById("query-explanation");
    
    const nlQueryInput = document.getElementById("nl-query");
    
    // Support keyboard shortcuts: Enter submits, Shift+Enter adds a newline
    if (nlQueryInput && queryForm) {
        nlQueryInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                queryForm.requestSubmit(); // Triggers the form's submit handler
            }
        });
    }

    if (queryForm) {
        queryForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const nlQuery = document.getElementById("nl-query").value.trim();
            if (!nlQuery) return;
            
            // Show loading indicators
            submitBtn.disabled = true;
            statusContainer.classList.remove("d-none");
            resultsCard.classList.add("d-none");
            
            try {
                // Fetch dynamic query pipeline
                const response = await fetch("/api/query", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: nlQuery })
                });
                const data = await response.json();
                
                if (data.status === "success") {
                    generatedSql.textContent = data.sql;
                    
                    if (data.explanation) {
                        queryExplanation.textContent = data.explanation;
                        explanationContainer.classList.remove("d-none");
                    } else {
                        explanationContainer.classList.add("d-none");
                    }
                    
                    resultsCard.classList.remove("d-none");
                } else {
                    alert("Query failed: " + data.message);
                }
            } catch (err) {
                console.error("Pipeline request error:", err);
                alert("An error occurred during query evaluation.");
            } finally {
                submitBtn.disabled = false;
                statusContainer.classList.add("d-none");
            }
        });
    }

    // Fetch and render database schema info
    const schemaAccordion = document.getElementById("schema-accordion");
    const schemaLoading = document.getElementById("schema-loading");
    
    async function loadSchema() {
        try {
            const response = await fetch("/api/schema");
            const data = await response.json();
            
            if (data.status === "success" && schemaAccordion) {
                // Remove loading indicator
                if (schemaLoading) schemaLoading.remove();
                
                const tables = data.tables;
                const tableNames = Object.keys(tables);
                
                if (tableNames.length === 0) {
                    schemaAccordion.innerHTML = `
                        <div class="text-center py-3 text-muted">
                            No tables found. Please configure the olist.db database.
                        </div>
                    `;
                    return;
                }
                
                schemaAccordion.innerHTML = ""; // Clear
                
                tableNames.forEach((tableName, index) => {
                    const columns = tables[tableName];
                    const columnsList = columns.map(col => {
                        const pkBadge = col.primary_key ? '<span class="badge bg-warning text-dark float-end" style="font-size: 0.65rem;">PK</span>' : '';
                        return `
                            <li class="list-group-item d-flex justify-content-between align-items-center py-1 bg-transparent border-0">
                                <code>${col.name}</code>
                                <div>
                                    <span class="text-muted small">${col.type}</span>
                                    ${pkBadge}
                                </div>
                            </li>
                        `;
                    }).join("");
                    
                    const accordionItem = `
                        <div class="accordion-item bg-transparent">
                            <h2 class="accordion-header" id="heading-${index}">
                                <button class="accordion-button collapsed py-2 px-3 fw-semibold bg-transparent" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${index}" aria-expanded="false" aria-controls="collapse-${index}">
                                    📊 ${tableName}
                                </button>
                            </h2>
                            <div id="collapse-${index}" class="accordion-collapse collapse" aria-labelledby="heading-${index}" data-bs-parent="#schema-accordion">
                                <div class="accordion-body p-0">
                                    <ul class="list-group list-group-flush small bg-transparent">
                                        ${columnsList}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    `;
                    schemaAccordion.insertAdjacentHTML("beforeend", accordionItem);
                });
            }
        } catch (err) {
            console.error("Failed to load schema details:", err);
            if (schemaLoading) {
                schemaLoading.innerHTML = '<span class="text-danger">Failed to load schema details.</span>';
            }
        }
    }
    
    loadSchema();
});
