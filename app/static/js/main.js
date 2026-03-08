(() => {
  // Enable Bootstrap tooltips if present
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map((el) => new bootstrap.Tooltip(el));

  // Small "popup" effect: if a success flash exists, also show a lightweight modal-like alert.
  // This keeps the demo dependency-free while still feeling interactive.
  const alerts = Array.from(document.querySelectorAll(".flash-stack .alert"));
  const text = alerts.map(a => a.textContent || "").join(" ").toLowerCase();
  if (text.includes("certificate minted")) {
    window.setTimeout(() => window.alert("Certificate Earned! (Soulbound)\n\nYour Certificate + Badge were added to your dashboard."), 150);
  } else if (text.includes("success! nft added")) {
    window.setTimeout(() => window.alert("Success! NFT added to wallet."), 150);
  } else if (text.includes("listed for sale")) {
    window.setTimeout(() => window.alert("Listed for sale."), 150);
  } else if (text.includes("wallet connected")) {
    window.setTimeout(() => window.alert("Wallet connected: 0x7f...3dE2"), 150);
  }
})();

