function addBlock() {
    const transactions = document.getElementById("transactions").value.trim();
    
    if (transactions === "") {
        showNotification("⚠️ Please enter transactions!", true);
        return;
    }
    
    fetch("/add_block", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transactions: transactions.split(",") })
    }).then(response => response.json())
    .then(data => {
        console.log("✅ Block Added:", data);
        showNotification("✅ " + data.message);
        fetchBlockchain();
    }).catch(() => {
        console.error("❌ Failed to add block!");
        showNotification("❌ Failed to add block!", true);
    });

    document.getElementById("transactions").value = ""; 
}

function tamperBlock() {
    const blockIndex = document.getElementById("blockIndex").value.trim();
    const newTransactions = document.getElementById("newTransactions").value.trim();
    
    if (blockIndex === "" || newTransactions === "") {
        showNotification("⚠️ Please enter valid block index & transactions!", true);
        return;
    }
    
    fetch("/tamper_block", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index: parseInt(blockIndex), transactions: newTransactions.split(",") })
    }).then(response => response.json())
    .then(data => {
        console.warn("⚠️ Block Tampered:", data);
        showNotification("⚠️ " + data.message, true);
        fetchBlockchain();
    }).catch(() => {
        console.error("❌ Failed to tamper block!");
        showNotification("❌ Failed to tamper block!", true);
    });

    document.getElementById("blockIndex").value = "";
    document.getElementById("newTransactions").value = "";
}

function validateBlockchain() {
    fetch("/validate_chain")
    .then(response => response.json())
    .then(data => {
        console.log("🔍 Blockchain Validation Result:", data);
        showNotification(data.valid ? "✅ Blockchain is valid!" : "❌ Blockchain is tampered!", !data.valid);
    }).catch(() => {
        console.error("❌ Failed to validate blockchain!");
        showNotification("❌ Failed to validate blockchain!", true);
    });
}

function fetchBlockchain() {
    fetch("/get_chain")
    .then(response => response.json())
    .then(data => {
        console.log("📜 Current Blockchain:", data);
        
        const blockchainDiv = document.getElementById("blockchain");
        blockchainDiv.innerHTML = ""; 

        data.chain.forEach((block, index) => {
            if (index > 0) {
                const arrowDiv = document.createElement("div");
                arrowDiv.classList.add("arrow");
                arrowDiv.innerHTML = "→";
                blockchainDiv.appendChild(arrowDiv);
            }

            const blockDiv = document.createElement("div");
            blockDiv.classList.add("block");
            blockDiv.innerHTML = `
                <p><strong>Index:</strong> ${block.index}</p>
                <p><strong>Timestamp:</strong> ${block.timestamp}</p>
                <p><strong>Transactions:</strong> ${JSON.stringify(block.transactions)}</p>
                <p><strong>Previous Hash:</strong> ${block.previous_hash}</p>
                <p><strong>Hash:</strong> ${block.hash}</p>
            `;
            blockchainDiv.appendChild(blockDiv);
        });
    }).catch(() => {
        console.error("❌ Failed to fetch blockchain!");
        showNotification("❌ Failed to fetch blockchain!", true);
    });
}

function resetBlockchain() {
    fetch('/reset_chain', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log("🔄 Blockchain Reset:", data);
            showNotification("🔄 " + data.message);
            fetchBlockchain();
        })
        .catch(() => {
            console.error("❌ Failed to reset blockchain!");
            showNotification("❌ Failed to reset blockchain!", true);
        });
}

// Fetch logs from the server and print them to the console
function fetchLogs() {
    fetch('/get_logs')
        .then(response => response.json())
        .then(data => {
            console.log("📝 Server Logs:", data.logs);
        })
        .catch(() => {
            console.error("❌ Failed to fetch logs!");
        });
}

// Show notifications on UI
function showNotification(message, isError = false) {
    const notification = document.getElementById("notification");
    notification.textContent = message;
    notification.classList.add("show");
    if (isError) {
        notification.classList.add("error");
    } else {
        notification.classList.remove("error");
    }
    setTimeout(() => {
        notification.classList.remove("show");
    }, 3000);
}

// Auto-update blockchain and logs every 5s
setInterval(() => {
    fetchBlockchain();
    fetchLogs();
}, 5000);
