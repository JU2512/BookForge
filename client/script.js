// ======================================================
// BOOKFORGE - Multi-Section Dashboard
// Main JavaScript
// ======================================================

// ------------------------------
// Load HTML Sections
// ------------------------------

async function loadSection(id, file) {
    const response = await fetch(file);
    const html = await response.text();

    document.getElementById(id).innerHTML = html;
}

// ------------------------------
// App Initialization
// ------------------------------

window.onload = async () => {
    await loadSection("uploadPage", "sections/upload.html");
    await loadSection("dashboard", "sections/dashboard.html");

    initializeEvents();
    initializeDashboardNavigation();
};

// ------------------------------
// Global Variables
// ------------------------------

let uploadedFile = null;
let analysisResult = null;

// ------------------------------
// Initialize Events
// ------------------------------

function initializeEvents() {
    const startBtn = document.getElementById("startBtn");
    const analyzeNav = document.querySelector(".nav-links a:nth-child(2)");
    const uploadSection = document.getElementById("uploadPage");
    const fileInput = document.getElementById("epubFile");
    const selectedFile = document.getElementById("selectedFile");
    const dropZone = document.getElementById("dropZone");
    const analyzeBtn = document.getElementById("analyzeBtn");

    startBtn.addEventListener("click", () => {
        uploadSection.scrollIntoView({
            behavior: "smooth"
        });
    });

    analyzeNav.addEventListener("click", (e) => {
        e.preventDefault();

        uploadSection.scrollIntoView({
            behavior: "smooth"
        });
    });

    fileInput.addEventListener("change", () => {
        if (!fileInput.files.length) return;

        const file = fileInput.files[0];

        if (!file.name.toLowerCase().endsWith(".epub")) {
            alert("Please upload an EPUB file.");
            fileInput.value = "";
            return;
        }

        uploadedFile = file;
        selectedFile.innerHTML =
            '<i class="fa-solid fa-file"></i> ' + uploadedFile.name;
    });

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("dragging");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragging");
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragging");

        const file = e.dataTransfer.files[0];

        if (!file) return;

        if (!file.name.toLowerCase().endsWith(".epub")) {
            alert("Please upload an EPUB file.");
            return;
        }

        uploadedFile = file;
        selectedFile.innerHTML =
            '<i class="fa-solid fa-file"></i> ' + uploadedFile.name;
    });

    analyzeBtn.addEventListener("click", () => {
        if (!uploadedFile) {
            alert("Please select an EPUB file.");
            return;
        }

        startAnalysis(uploadedFile);
    });
}

// ======================================================
// Dashboard Navigation & Multi-Section Support
// ======================================================

function initializeDashboardNavigation() {
    const menuItems = document.querySelectorAll(".menu-item");

    menuItems.forEach((item) => {
        item.addEventListener("click", (e) => {
            e.preventDefault();

            const sectionName = item.getAttribute("data-section");
            switchSection(sectionName);

            menuItems.forEach((menuItem) => {
                menuItem.classList.remove("active");
            });

            item.classList.add("active");
        });
    });

    const analyzeAnotherBtn = document.getElementById("analyzeAnother");

    if (analyzeAnotherBtn) {
        analyzeAnotherBtn.addEventListener("click", () => {
            const uploadSection = document.getElementById("uploadPage");
            const dashboard = document.getElementById("dashboard");

            uploadSection.style.display = "block";
            dashboard.style.display = "none";
        });
    }
}

function switchSection(sectionName) {
    const sections = document.querySelectorAll(".dashboard-section");

    sections.forEach((section) => {
        section.classList.remove("active");
    });

    const targetSection = document.getElementById(sectionName + "Section");

    if (targetSection) {
        targetSection.classList.add("active");
    }
}

// ======================================================
// Start EPUB Analysis
// ======================================================

async function startAnalysis(file) {
    const uploadSection = document.getElementById("uploadPage");
    const loadingPage = document.getElementById("loadingPage");
    const dashboard = document.getElementById("dashboard");

    uploadSection.style.display = "none";
    dashboard.style.display = "none";
    loadingPage.style.display = "flex";

    const progress = document.getElementById("progress");
    const loadingText = document.getElementById("loadingText");

    const steps = [
        "Reading EPUB...",
        "Validating Metadata...",
        "Checking Manifest...",
        "Analyzing HTML...",
        "Analyzing CSS...",
        "Checking Images...",
        "Validating Hyperlinks...",
        "Generating Report..."
    ];

    for (let i = 0; i < steps.length; i++) {
        loadingText.innerHTML = steps[i];
        progress.style.width = ((i + 1) * 12.5) + "%";

        const currentStep = document.getElementById("step" + (i + 1));

        if (currentStep) {
            currentStep.classList.add("completed");
        }

        await new Promise((resolve) => setTimeout(resolve, 400));
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("https://bookforge-api.onrender.com/analyze", {
            method: "POST",
            body: formData
        });

        console.log("Status:", response.status);
        console.log("OK:", response.ok);
        console.log("URL:", response.url);

        if (!response.ok) {

            const errorText = await response.text();

            alert(
                `Status: ${response.status}\n\n${errorText}`
            );

            return;
        }
        analysisResult = await response.json();

        console.log("===== JSON RECEIVED =====");
        console.log(analysisResult);

        console.log(
            "overallScore:",
            document.getElementById("overallScore")
        );
        console.log(
            "bookTitle:",
            document.getElementById("bookTitle")
        );
        console.log(
            "chaptersContainer:",
            document.getElementById("chaptersContainer")
        );

        console.log("Starting dashboard population...");

        populateMultiSectionDashboard(analysisResult);

        

        console.log("Dashboard populated successfully.");

        loadingPage.style.display = "none";
        uploadSection.style.display = "none";
        dashboard.style.display = "block";

        dashboard.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    } catch (error) {
        console.error("ERROR:", error);
        console.error("STACK:", error.stack);

        loadingPage.style.display = "none";
        uploadSection.style.display = "block";

        alert(error.message);
    }
}

// ======================================================
// Populate Multi-Section Dashboard
// ======================================================

function populateMultiSectionDashboard(data) {
    populateOverviewSection(data);
    populateQualitySection(data);
    populateChaptersSection(data);
    populateIssuesSection(data);
    populateRecommendationsSection(data);

    populateExportSection(data);
    setupDownloadHandler();
}

// ======================================================
// OVERVIEW SECTION
// ======================================================

function populateOverviewSection(data) {
    if (!data) return;

    setTextSafe(
        "overallScore",
        data.summary && typeof data.summary.overall_score !== "undefined"
            ? data.summary.overall_score
            : "-"
    );

    setTextSafe(
        "grade",
        data.summary && data.summary.grade
            ? data.summary.grade
            : "-"
    );

    setTextSafe(
        "status",
        data.summary && data.summary.status
            ? data.summary.status
            : "-"
    );

    setTextSafe(
        "chapterCount",
        data.statistics && typeof data.statistics.chapters !== "undefined"
            ? data.statistics.chapters
            : "0"
    );

    const score =
        data.summary && typeof data.summary.overall_score !== "undefined"
            ? data.summary.overall_score
            : 0;

    setTextSafe("gradeDesc", getGradeDescription(score));

    setTextSafe(
        "bookTitle",
        data.book && data.book.title
            ? data.book.title
            : "-"
    );

    setTextSafe(
        "bookAuthor",
        data.book && data.book.author
            ? data.book.author
            : "-"
    );

    setTextSafe(
        "ov-infoTitle",
        data.book && data.book.title
            ? data.book.title
            : "-"
    );

    setTextSafe(
        "ov-infoAuthor",
        data.book && data.book.author
            ? data.book.author
            : "-"
    );

    const bookInfo = data.book || {};
    const language = bookInfo.language || bookInfo.lang || "N/A";
    const epubVersion = bookInfo.epub_version || bookInfo.version || "N/A";
    const sizeVal =
        bookInfo.size ||
        bookInfo.file_size ||
        bookInfo.filesize ||
        null;

    setTextSafe("ov-infoLanguage", language);
    setTextSafe("bookLanguage", language);
    setTextSafe("ov-epubVersionTable", epubVersion);
    setTextSafe("epubVersion", epubVersion);
    setTextSafe("bookSize", sizeVal ? formatBytes(sizeVal) : "--");

    setTextSafe(
        "ov-chapterCountTable",
        data.statistics && typeof data.statistics.chapters !== "undefined"
            ? data.statistics.chapters
            : "0"
    );

    setTextSafe(
        "ov-imageCount",
        data.statistics && typeof data.statistics.images !== "undefined"
            ? data.statistics.images
            : "0"
    );

    setTextSafe(
        "ov-cssCount",
        data.statistics && typeof data.statistics.stylesheets !== "undefined"
            ? data.statistics.stylesheets
            : "0"
    );

    const hyperlinkCount = countHyperlinks(data);

    const criticalCount =
        data.issues && Array.isArray(data.issues.critical)
            ? data.issues.critical.length
            : 0;

    setTextSafe(
        "statImageCount",
        data.statistics && typeof data.statistics.images !== "undefined"
            ? data.statistics.images
            : "0"
    );

    setTextSafe(
        "statCssCount",
        data.statistics && typeof data.statistics.stylesheets !== "undefined"
            ? data.statistics.stylesheets
            : "0"
    );

    setTextSafe("statHyperlinkCount", hyperlinkCount);
    setTextSafe("statCriticalCount", criticalCount);

    setQualityBar(
        "ov-metadataScore",
        "ov-metadataBar",
        "ov-metadataQuality",
        data.quality && typeof data.quality.metadata !== "undefined"
            ? data.quality.metadata
            : 0
    );

    setQualityBar(
        "ov-htmlScore",
        "ov-htmlBar",
        "ov-htmlQuality",
        data.quality && typeof data.quality.html !== "undefined"
            ? data.quality.html
            : 0
    );

    setQualityBar(
        "ov-cssScore",
        "ov-cssBar",
        "ov-cssQuality",
        data.quality && typeof data.quality.css !== "undefined"
            ? data.quality.css
            : 0
    );

    setQualityBar(
        "ov-imageScore",
        "ov-imageBar",
        "ov-imagesQuality",
        data.quality && typeof data.quality.images !== "undefined"
            ? data.quality.images
            : 0
    );

    setQualityBar(
        "ov-hyperlinkScore",
        "ov-hyperlinkBar",
        "ov-hyperlinksQuality",
        data.quality && typeof data.quality.hyperlinks !== "undefined"
            ? data.quality.hyperlinks
            : 0
    );
}

// ======================================================
// QUALITY REPORT SECTION
// ======================================================

function populateQualitySection(data) {
    if (!data) return;

    setQualityBar(
        "qr-metadataScore",
        "qr-metadataBar",
        "qr-metadataQuality",
        data.quality && typeof data.quality.metadata !== "undefined"
            ? data.quality.metadata
            : 0
    );

    setQualityBar(
        "qr-htmlScore",
        "qr-htmlBar",
        "qr-htmlQuality",
        data.quality && typeof data.quality.html !== "undefined"
            ? data.quality.html
            : 0
    );

    setQualityBar(
        "qr-cssScore",
        "qr-cssBar",
        "qr-cssQuality",
        data.quality && typeof data.quality.css !== "undefined"
            ? data.quality.css
            : 0
    );

    setQualityBar(
        "qr-imageScore",
        "qr-imageBar",
        "qr-imagesQuality",
        data.quality && typeof data.quality.images !== "undefined"
            ? data.quality.images
            : 0
    );

    setQualityBar(
        "qr-hyperlinkScore",
        "qr-hyperlinkBar",
        "qr-hyperlinksQuality",
        data.quality && typeof data.quality.hyperlinks !== "undefined"
            ? data.quality.hyperlinks
            : 0
    );
}

// ======================================================
// CHAPTER ANALYSIS SECTION
// ======================================================

function populateChaptersSection(data) {
    if (!data) return;

    const container = getEl("chaptersContainer");

    if (!container) return;

    container.innerHTML = "";

    const chapters = Array.isArray(data.chapters)
        ? data.chapters
        : [];

    if (chapters.length === 0) {
        container.innerHTML =
            '<div class="empty-state">No chapter analysis available.</div>';

        const ids = [
            "totalChapters",
            "passChapters",
            "warningChapters",
            "errorChapters",
            "avgChapterScore"
        ];

        ids.forEach((id) => {
            const element = document.getElementById(id);

            if (element) {
                element.textContent =
                    id === "avgChapterScore" ? "0%" : "0";
            }
        });

        return;
    }

    const total = chapters.length;

    let passCount = 0;
    let warningCount = 0;
    let errorCount = 0;
    let scoreSum = 0;

    chapters.forEach((chapter) => {
        const status = (chapter.status || "")
            .toString()
            .toLowerCase();

        if (status === "pass") passCount++;
        else if (status === "warning") warningCount++;
        else if (status === "error") errorCount++;

        scoreSum += Number(chapter.score) || 0;
    });

    const averageScore = total
        ? Math.round(scoreSum / total)
        : 0;

    setTextSafe("totalChapters", total);
    setTextSafe("passChapters", passCount);
    setTextSafe("warningChapters", warningCount);
    setTextSafe("errorChapters", errorCount);
    setTextSafe("avgChapterScore", averageScore + "%");

    const fragment = document.createDocumentFragment();

    chapters.forEach((chapterObj, index) => {
        const chapterCard = document.createElement("div");
        chapterCard.className = "chapter-card";

        const chapterName =
            chapterObj.chapter ||
            chapterObj.name ||
            `Chapter ${index + 1}`;

        const score =
            typeof chapterObj.score !== "undefined"
                ? chapterObj.score
                : 0;

        const status = chapterObj.status || "N/A";

        const issues = Array.isArray(chapterObj.issues)
            ? chapterObj.issues
            : [];

        const issueCount = issues.length;

        const statusLower = status.toString().toLowerCase();

        const badgeClass =
            "issue-severity " +
            (statusLower === "pass"
                ? "pass"
                : statusLower === "warning"
                    ? "warning"
                    : statusLower === "error"
                        ? "critical"
                        : "information");

        chapterCard.innerHTML = `
            <div class="chapter-header">
                <div class="chapter-info">
                    <h3>${escapeHtml(chapterName)}</h3>
                    <p class="chapter-meta">
                        Score: ${score}% | Issues: ${issueCount}
                    </p>
                </div>

                <div class="chapter-status">
                    <span class="${badgeClass}">
                        ${escapeHtml(status)}
                    </span>
                    <i class="fa-solid fa-chevron-down"></i>
                </div>
            </div>

            <div class="chapter-details">
                <div class="chapter-progress">
                    <div class="progress-bar">
                        <div
                            class="progress-fill"
                            style="width: ${score}%"
                        ></div>
                    </div>

                    <span class="progress-text">
                        ${score}% Complete
                    </span>
                </div>

                <div class="chapter-issues">
                    ${renderChapterIssues(issues)}
                </div>
            </div>
        `;

        fragment.appendChild(chapterCard);
    });

    container.appendChild(fragment);

    if (!container._hasClickListener) {
        container.addEventListener("click", (e) => {
            const header = e.target.closest(".chapter-header");

            if (!header) return;

            const card = header.closest(".chapter-card");

            if (!card) return;

            const currentlyExpanded = container.querySelector(
                ".chapter-card.expanded"
            );

            if (currentlyExpanded && currentlyExpanded !== card) {
                currentlyExpanded.classList.remove("expanded");
            }

            card.classList.toggle("expanded");
        });

        container._hasClickListener = true;
    }
}

function renderChapterIssues(issues) {
    if (!issues || issues.length === 0) {
        return '<p class="no-issues">No issues found in this chapter</p>';
    }

    return issues.map((issue) => {
        const severity = (issue.severity || "")
            .toString()
            .toLowerCase();

        const severityText = issue.severity || "";
        const fieldOrRule = issue.field || issue.rule || "-";
        const message = issue.message || "";

        return `
            <div class="chapter-issue">
                <div class="issue-severity ${severity}">
                    ${escapeHtml(severityText)}
                </div>

                <div class="issue-content">
                    <strong>${escapeHtml(fieldOrRule)}</strong>
                    <p>${escapeHtml(message)}</p>
                </div>
            </div>
        `;
    }).join("");
}

// ======================================================
// ISSUES SECTION
// ======================================================

function populateIssuesSection(data) {
    if (!data) return;

    const issuesRoot = data.issues || {};

    const criticalIssues = Array.isArray(issuesRoot.critical)
        ? issuesRoot.critical
        : [];

    const warningIssues = Array.isArray(issuesRoot.warnings)
        ? issuesRoot.warnings
        : [];

    const infoIssues = Array.isArray(issuesRoot.information)
        ? issuesRoot.information
        : [];

    setTextSafe("critical-count", criticalIssues.length);
    setTextSafe("warning-count", warningIssues.length);
    setTextSafe("info-count", infoIssues.length);

    renderIssueGroup(
        criticalIssues,
        "criticalIssuesContainer",
        "critical"
    );

    renderIssueGroup(
        warningIssues,
        "warningIssuesContainer",
        "warning"
    );

    renderIssueGroup(
        infoIssues,
        "infoIssuesContainer",
        "info"
    );
}

function renderIssueGroup(issues, containerId, type) {
    const container = getEl(containerId);

    if (!container) return;

    container.innerHTML = "";

    if (!issues || issues.length === 0) {
        let message = "No issues found";

        if (type === "critical") {
            message = "No critical issues found.";
        } else if (type === "warning") {
            message = "No warnings found.";
        } else if (type === "info") {
            message = "No informational messages.";
        }

        setInnerHtmlSafe(
            containerId,
            `<div class="empty-state">${message}</div>`
        );

        return;
    }

    issues.forEach((issue) => {
        const issueCard = document.createElement("div");
        issueCard.className = "issue-card";

        const fieldOrRule = issue.field || issue.rule || "-";
        const message = issue.message || "";

        const severity = (issue.severity || "")
            .toString()
            .toLowerCase();

        let badgeClass = "severity-badge info";
        let badgeText = "INFO";

        if (severity === "error" || severity === "critical") {
            badgeClass = "severity-badge critical";
            badgeText = "ERROR";
        } else if (severity === "warning") {
            badgeClass = "severity-badge warning";
            badgeText = "WARNING";
        }

        issueCard.innerHTML = `
            <div class="issue-header"
                 style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
                <strong>${escapeHtml(fieldOrRule)}</strong>
                <span class="${badgeClass}">${badgeText}</span>
            </div>

            <p class="issue-message">
                ${escapeHtml(message)}
            </p>
        `;

        container.appendChild(issueCard);
    });
}

// ======================================================
// RECOMMENDATIONS SECTION
// ======================================================

function populateRecommendationsSection(data) {
    if (!data) return;

    const container = getEl("recommendationsContainer");

    if (!container) return;

    container.innerHTML = "";

    if (
        !Array.isArray(data.recommendations) ||
        data.recommendations.length === 0
    ) {
        setInnerHtmlSafe(
            "recommendationsContainer",
            '<div class="empty-state">No recommendations available.</div>'
        );

        return;
    }

    data.recommendations.forEach((recommendation, index) => {
        const recommendationCard = document.createElement("div");
        recommendationCard.className = "recommendation-card";

        recommendationCard.innerHTML = `
            <div class="rec-header">
                <span class="rec-number">${index + 1}</span>
                <h3>Recommendation</h3>
            </div>

            <p class="rec-text">
                ${escapeHtml(recommendation)}
            </p>
        `;

        container.appendChild(recommendationCard);
    });
}

// ======================================================
// EXPORT SECTION
// ======================================================

function populateExportSection(data) {
    // Static section. The button event is assigned below.
}

// ======================================================
// Helper Functions
// ======================================================

function getGradeDescription(score) {
    if (score >= 90) return "Excellent";
    if (score >= 80) return "Very Good";
    if (score >= 70) return "Good";
    if (score >= 60) return "Fair";

    return "Needs Improvement";
}

function getStatusClass(score) {
    if (score >= 90) return "status-excellent";
    if (score >= 80) return "status-good";
    if (score >= 70) return "status-fair";

    return "status-poor";
}

function countHyperlinks(data) {
    if (
        data &&
        data.statistics &&
        typeof data.statistics.hyperlinks !== "undefined"
    ) {
        return data.statistics.hyperlinks;
    }

    return 0;
}

function getEl(id) {
    return document.getElementById(id);
}

function setTextSafe(id, text) {
    const element = getEl(id);

    if (element) {
        element.textContent = text;
    }
}

function setInnerHtmlSafe(id, html) {
    const element = getEl(id);

    if (element) {
        element.innerHTML = html;
    }
}

function setQualityBar(scoreId, barId, statusId, value) {
    const scoreElement = getEl(scoreId);
    const barElement = getEl(barId);
    const statusElement = getEl(statusId);

    if (scoreElement) {
        scoreElement.textContent = value + "%";
    }

    if (barElement) {
        barElement.style.width = value + "%";
    }

    if (statusElement) {
        statusElement.textContent = getQualityStatus(value);
    }
}

function getQualityStatus(score) {
    if (score >= 90) return "Excellent";
    if (score >= 80) return "Very Good";
    if (score >= 70) return "Good";
    if (score >= 60) return "Fair";

    return "Needs Improvement";
}

// ======================================================
// Download Handler
// ======================================================

function setupDownloadHandler() {

    const pdfButton = document.getElementById("downloadPdf");

    if (!pdfButton) return;

    pdfButton.onclick = async () => {

        try {

            pdfButton.disabled = true;
            pdfButton.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i> Generating PDF...';

            const response = await fetch(
                "https://bookforge-api.onrender.com/export/pdf"
            );

            if (!response.ok) {
                throw new Error("Failed to generate PDF.");
            }

            const blob = await response.blob();

            const url = window.URL.createObjectURL(blob);

            const link = document.createElement("a");

            link.href = url;
            link.download = "BookForge_Report.pdf";

            document.body.appendChild(link);

            link.click();

            link.remove();

            window.URL.revokeObjectURL(url);

        } catch (error) {

            console.error(error);

            alert("Unable to download PDF.");

        } finally {

            pdfButton.disabled = false;

            pdfButton.innerHTML =
                '<i class="fa-solid fa-file-pdf"></i> Download PDF';

        }

    };

}

// ======================================================
// Formatting and Security Helpers
// ======================================================

function formatBytes(bytes, decimals = 1) {
    if (bytes === 0) return "0 B";
    if (!bytes) return null;

    const unit = 1024;
    const decimalPlaces = decimals < 0 ? 0 : decimals;
    const sizes = ["B", "KB", "MB", "GB", "TB"];

    const index = Math.floor(Math.log(bytes) / Math.log(unit));

    return (
        parseFloat(
            (bytes / Math.pow(unit, index)).toFixed(decimalPlaces)
        ) +
        " " +
        sizes[index]
    );
}

function escapeHtml(text) {
    if (text === null || text === undefined) return "";

    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}