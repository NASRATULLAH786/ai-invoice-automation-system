async function extractInvoice() {

    const invoiceText = document.getElementById("invoiceText").value;

    const response = await fetch(
        "http://127.0.0.1:8080/extract-invoice",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                invoice_text: invoiceText
            })
        }
    );

    const data = await response.json();

    console.log(data);

    const invoice = data.invoice || data;

    document.getElementById("result").innerHTML = `
        <h3>Extracted Invoice</h3>

        <div class="invoice-card">
            <p><strong>Company:</strong> ${invoice.company_name}</p>
            <p><strong>Invoice Number:</strong> ${invoice.invoice_number}</p>
            <p><strong>Date:</strong> ${invoice.date}</p>
            <p><strong>Total:</strong> ${invoice.total_amount}</p>
        </div>
    `;
}


async function loadInvoices() {

    const response = await fetch(
        "http://127.0.0.1:8080/invoices"
    );

    const data = await response.json();

    let html = "<h3>Stored Invoices</h3>";

    data.forEach(invoice => {

        html += `
            <div class="invoice-card">
                <p><strong>Company:</strong> ${invoice.company_name}</p>
                <p><strong>Invoice Number:</strong> ${invoice.invoice_number}</p>
                <p><strong>Date:</strong> ${invoice.date}</p>
                <p><strong>Total:</strong> ${invoice.total_amount}</p>
            </div>
        `;
    });

    document.getElementById("invoiceList").innerHTML = html;
}