async function copyText(elementId, button) {
    const element = document.getElementById(elementId);
    if (!element) return;

    try {
        await navigator.clipboard.writeText(element.value);
    } catch (e) {
        element.select();
        document.execCommand("copy");
    }

    const oldText = button.innerText;
    button.innerText = "Copied ✓";
    button.disabled = true;

    setTimeout(() => {
        button.innerText = oldText;
        button.disabled = false;
    }, 1400);
}
