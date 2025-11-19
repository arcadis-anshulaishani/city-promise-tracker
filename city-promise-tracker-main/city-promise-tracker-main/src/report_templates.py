"""
This module contains HTML/CSS/JS templates for generating reports.
"""

# --- HTML Report Styles ---
REPORT_CSS = """
<style>
    body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }
    .report-container { max-width: 800px; margin: 20px auto; background: white; padding: 40px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    .cover-page { text-align: center; padding: 50px 20px; border-bottom: 2px solid #004085; margin-bottom: 40px; }
    .cover-page h1 { font-size: 3em; color: #004085; margin: 0; }
    .cover-page p { font-size: 1.2em; color: #555; }
    .report-content h2 { color: #004085; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
    .report-content { line-height: 1.6; }
    .report-item { margin-bottom: 20px; padding: 20px; border: 1px solid #eee; border-radius: 5px; }
    .search-bar { margin-bottom: 20px; }
    .search-bar input { width: 70%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
    .search-bar button { padding: 10px 15px; border: none; background: #004085; color: white; border-radius: 5px; cursor: pointer; }
    hr { border: 0; height: 1px; background: #ddd; margin: 40px 0; }
    mark { background-color: yellow; padding: 0; }
</style>
"""

# --- HTML Report Search Script ---
REPORT_SEARCH_SCRIPT = """
<script>
    function searchReport() {
        let input = document.getElementById('searchInput');
        let filter = input.value.toUpperCase();
        let content = document.getElementById('report-content-items');
        let items = content.getElementsByClassName('report-item');
        let found = false;

        for (let i = 0; i < items.length; i++) {
            let item = items[i];
            let text = item.textContent || item.innerText;
            
            // Clear previous highlighting
            item.innerHTML = item.innerHTML.replace(/<mark>/g, "").replace(/<\/mark>/g, "");

            if (text.toUpperCase().indexOf(filter) > -1) {
                item.style.display = "";
                found = true;
                
                // Add new highlighting
                if (filter) {
                    let regex = new RegExp(filter, "gi");
                    item.innerHTML = item.innerHTML.replace(regex, function(match) {
                        return "<mark>" + match + "</mark>";
                    });
                }
            } else {
                item.style.display = "none";
            }
        }
    }
</script>
"""
